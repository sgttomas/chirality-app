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

export class AuthRegistry {
  private readonly clientsFile: string;
  private readonly tokensDirectory: string;

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
