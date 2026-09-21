import { createHash, randomBytes, timingSafeEqual } from "node:crypto";
import { chmod, readFile } from "node:fs/promises";
import { join } from "node:path";
import { RuntimeError } from "@chirality/runtime-contracts";
import { atomicWriteJson, ensurePrivateDirectory, readJsonIfExists } from "./fs.js";

export type RuntimeScope =
  | "runtime:read"
  | "projects:write"
  | "sessions:read"
  | "sessions:write"
  | "models:read"
  | "models:write"
  | "credentials:read"
  | "credentials:write";

export type AccountRuntimeScope = "account:read" | "account:control";

interface ClientRecord {
  clientId: string;
  tokenHash: string;
  projectId?: string;
  scopes: readonly RuntimeScope[];
  createdAt: string;
  revokedAt?: string;
}

interface ClientRegistry {
  schemaVersion: "chirality.clients/v1";
  clients: ClientRecord[];
}

export interface IssuedClient {
  clientId: string;
  token: string;
  tokenFile: string;
}

export interface RuntimePrincipal {
  clientId: string;
  projectId?: string;
  scopes: readonly RuntimeScope[];
}

interface MemoryAccountPrincipalRecord {
  readonly clientId: string;
  readonly tokenHash: string;
  readonly generation: string;
  readonly scopes: readonly AccountRuntimeScope[];
}

export interface AccountRuntimePrincipal {
  clientId: string;
  generation: string;
  scopes: readonly AccountRuntimeScope[];
}

export class AuthRegistry {
  private readonly clientsFile: string;
  private readonly tokensDirectory: string;
  private readonly memoryAccountPrincipals = new Map<string, MemoryAccountPrincipalRecord>();

  constructor(private readonly runtimeDirectory: string) {
    this.clientsFile = join(runtimeDirectory, "auth", "clients.json");
    this.tokensDirectory = join(runtimeDirectory, "auth", "tokens");
  }

  async issueClient(
    clientId: string,
    scopes: readonly RuntimeScope[],
    projectId?: string
  ): Promise<IssuedClient> {
    const token = randomBytes(32).toString("base64url");
    const tokenHash = this.hash(token);
    const registry = await this.read();
    const retained = registry.clients.filter((client) => client.clientId !== clientId);
    const record: ClientRecord = {
      clientId,
      tokenHash,
      scopes: [...scopes],
      createdAt: new Date().toISOString(),
      ...(projectId === undefined ? {} : { projectId })
    };
    await this.write({ ...registry, clients: [...retained, record] });
    await ensurePrivateDirectory(this.tokensDirectory);
    const tokenFile = join(this.tokensDirectory, `${clientId}.token`);
    const { writeFile } = await import("node:fs/promises");
    await writeFile(tokenFile, `${token}\n`, { encoding: "utf8", mode: 0o600 });
    await chmod(tokenFile, 0o600);
    return { clientId, token, tokenFile };
  }

  async ensureClient(
    clientId: string,
    scopes: readonly RuntimeScope[],
    projectId?: string
  ): Promise<IssuedClient> {
    const registry = await this.read();
    const existing = registry.clients.find(
      (client) => client.clientId === clientId && client.revokedAt === undefined
    );
    const tokenFile = join(this.tokensDirectory, `${clientId}.token`);
    if (existing !== undefined) {
      try {
        const token = (await readFile(tokenFile, "utf8")).trim();
        if (token.length > 0 && this.hash(token) === existing.tokenHash) {
          return { clientId, token, tokenFile };
        }
      } catch {
        // Missing or mismatched plaintext client material is recovered by rotation.
      }
    }
    return this.issueClient(clientId, scopes, projectId);
  }

  async authenticate(
    authorization: string | undefined,
    requiredScope: RuntimeScope,
    projectId?: string
  ): Promise<RuntimePrincipal> {
    const match = /^Bearer ([A-Za-z0-9_-]+)$/u.exec(authorization ?? "");
    if (match?.[1] === undefined) {
      throw new RuntimeError("UNAUTHORIZED", "A runtime bearer token is required", 401);
    }
    const suppliedHash = Buffer.from(this.hash(match[1]), "hex");
    const registry = await this.read();
    const client = registry.clients.find((candidate) => {
      if (candidate.revokedAt !== undefined) return false;
      const expected = Buffer.from(candidate.tokenHash, "hex");
      return expected.length === suppliedHash.length && timingSafeEqual(expected, suppliedHash);
    });
    if (client === undefined) {
      throw new RuntimeError("UNAUTHORIZED", "Invalid runtime bearer token", 401);
    }
    if (!client.scopes.includes(requiredScope)) {
      throw new RuntimeError("FORBIDDEN", `Client lacks ${requiredScope}`, 403);
    }
    if (
      projectId !== undefined &&
      client.projectId !== undefined &&
      client.projectId !== projectId
    ) {
      throw new RuntimeError("FORBIDDEN", "Client is scoped to another project", 403);
    }
    return {
      clientId: client.clientId,
      scopes: client.scopes,
      ...(client.projectId === undefined ? {} : { projectId: client.projectId })
    };
  }

  async revoke(clientId: string): Promise<void> {
    const registry = await this.read();
    const now = new Date().toISOString();
    await this.write({
      ...registry,
      clients: registry.clients.map((client) =>
        client.clientId === clientId ? { ...client, revokedAt: now } : client
      )
    });
  }

  async revokeProjectClients(projectId: string): Promise<void> {
    const registry = await this.read();
    const now = new Date().toISOString();
    await this.write({
      ...registry,
      clients: registry.clients.map((client) =>
        client.projectId === projectId && client.revokedAt === undefined
          ? { ...client, revokedAt: now }
          : client
      )
    });
  }

  /** Registers the App account host only in daemon memory. This path never writes a token file. */
  registerMemoryAccountHost(input: {
    clientId: string;
    bearer: string;
    generation: string;
    scopes: readonly AccountRuntimeScope[];
  }): AccountRuntimePrincipal {
    if (!/^[A-Za-z0-9._:-]{1,128}$/u.test(input.clientId)
      || !/^[A-Za-z0-9_-]{43}$/u.test(input.bearer)
      || !/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/u.test(input.generation)
      || input.scopes.length !== 2
      || !input.scopes.includes("account:read")
      || !input.scopes.includes("account:control")) {
      throw new RuntimeError("UNAUTHORIZED", "Invalid memory account principal", 401);
    }
    const record = Object.freeze({
      clientId: input.clientId,
      tokenHash: this.hash(input.bearer),
      generation: input.generation,
      scopes: Object.freeze([...input.scopes])
    });
    this.memoryAccountPrincipals.set(input.clientId, record);
    return { clientId: record.clientId, generation: record.generation, scopes: record.scopes };
  }

  authenticateMemoryAccountHost(
    authorization: string | undefined,
    requiredScope: AccountRuntimeScope,
    generation: string
  ): AccountRuntimePrincipal {
    const match = /^Bearer ([A-Za-z0-9_-]{43})$/u.exec(authorization ?? "");
    if (match?.[1] === undefined) throw new RuntimeError("UNAUTHORIZED", "An account host bearer is required", 401);
    const suppliedHash = Buffer.from(this.hash(match[1]), "hex");
    const record = [...this.memoryAccountPrincipals.values()].find((candidate) => {
      const expected = Buffer.from(candidate.tokenHash, "hex");
      return expected.length === suppliedHash.length && timingSafeEqual(expected, suppliedHash);
    });
    if (record === undefined || record.generation !== generation) throw new RuntimeError("UNAUTHORIZED", "Invalid account host bearer", 401);
    if (!record.scopes.includes(requiredScope)) throw new RuntimeError("FORBIDDEN", `Account host lacks ${requiredScope}`, 403);
    return { clientId: record.clientId, generation: record.generation, scopes: record.scopes };
  }

  revokeMemoryAccountHost(clientId: string): void { this.memoryAccountPrincipals.delete(clientId); }

  revokeAllMemoryAccountHosts(): void { this.memoryAccountPrincipals.clear(); }

  private hash(token: string): string {
    return createHash("sha256").update(token).digest("hex");
  }

  private read(): Promise<ClientRegistry> {
    return readJsonIfExists(this.clientsFile, {
      schemaVersion: "chirality.clients/v1",
      clients: []
    });
  }

  private write(registry: ClientRegistry): Promise<void> {
    return atomicWriteJson(this.clientsFile, registry);
  }
}
