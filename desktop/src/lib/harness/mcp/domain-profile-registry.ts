import { HarnessError } from '@chirality/runtime-contracts/errors';

/**
 * D-APP-51 multi-engine domain profile registry (bridge-lane P1).
 *
 * Closed, ruled-registration-only registry: exactly the two ruled profileIds
 * (`open_pipe_stress` per D-APP-50, `pec` per D-APP-51) are registered. There
 * is no filesystem discovery and no dynamic registration; adding any third
 * engine is a source change under its own D-APP ruling (registration IS the
 * gate). The single read-transport binding literal in P1 is
 * `'in-process-read-evidence'`. The separately ruled D-APP-50 headless tool
 * carries its own configured-local-process binding on the open_pipe_stress
 * entry; no filesystem discovery or fallback transport exists.
 */

export type DomainEngineKind = 'deterministic-cli' | 'http-api';

/** The ONLY read-transport binding literal in P1 (D-APP-51 rider 3). */
export type DomainReadTransportBinding = 'in-process-read-evidence';

export type DomainReadToolId =
  | 'completeness_checker'
  | 'rule_check_runner'
  | 'headless_runner';

export type DomainEngineProfileRegistryEntry = {
  profileId: string;
  profileRelativePath: string;
  engineKind: DomainEngineKind;
  readTransportBinding: DomainReadTransportBinding;
  headlessPreviewTransportBinding?: 'configured-local-process';
  /** Exact live-file bytes (quoted YAML form — V-9 fix). */
  identityMarker: string;
  toolGate: Record<
    DomainReadToolId,
    {
      requiredMarker: string | null;
      declaredDeterministicToolId: string | null;
    }
  >;
  transportStatus: {
    posture: string;
    tranche: string;
    inputContract: string;
    deterministicToolExecution: string;
    resultSemantics: string;
  };
};

const NO_VERDICT_RESULT_SEMANTICS =
  'transport/evidence envelope only; no domain verdict, no live binding claim, and no professional engineering conclusion';

export const DOMAIN_ENGINE_PROFILE_REGISTRY: readonly DomainEngineProfileRegistryEntry[] = [
  {
    profileId: 'open_pipe_stress',
    profileRelativePath: '_DomainEngines/profiles/open_pipe_stress.yaml',
    engineKind: 'deterministic-cli',
    readTransportBinding: 'in-process-read-evidence',
    headlessPreviewTransportBinding: 'configured-local-process',
    identityMarker: 'id: "open_pipe_stress"',
    toolGate: {
      completeness_checker: {
        requiredMarker: '- id: "completeness_checker"',
        declaredDeterministicToolId: 'completeness_checker'
      },
      rule_check_runner: {
        requiredMarker: '- id: "rule_check_runner"',
        declaredDeterministicToolId: 'rule_check_runner'
      },
      headless_runner: {
        requiredMarker: '- id: "headless_runner"',
        declaredDeterministicToolId: 'headless_runner'
      }
    },
    transportStatus: {
      posture: 'DEC-041 in-process read transport',
      tranche: 'D-APP-50 tranche-1 read-side exposure',
      inputContract:
        'project-root-contained JSON references plus _DomainEngines/profiles/open_pipe_stress.yaml',
      deterministicToolExecution:
        'not invoked in this tranche; the authoritative Rust tool is library-only and has no stable JSON CLI transport',
      resultSemantics: NO_VERDICT_RESULT_SEMANTICS
    }
  },
  {
    profileId: 'pec',
    profileRelativePath: '_DomainEngines/profiles/pec.yaml',
    engineKind: 'http-api',
    readTransportBinding: 'in-process-read-evidence',
    identityMarker: 'id: "pec"',
    toolGate: {
      completeness_checker: {
        requiredMarker: null,
        declaredDeterministicToolId: null
      },
      rule_check_runner: {
        requiredMarker: null,
        declaredDeterministicToolId: null
      },
      headless_runner: {
        requiredMarker: null,
        declaredDeterministicToolId: null
      }
    },
    transportStatus: {
      posture: 'DEC-041 in-process read transport',
      tranche: 'D-APP-51 P1 multi-engine registry read exposure',
      inputContract:
        'project-root-contained JSON references plus _DomainEngines/profiles/pec.yaml',
      deterministicToolExecution:
        'not invoked; the pec profile declares no completeness_checker or rule_check_runner deterministic tools — this wrapper returns profile and input evidence envelopes only; engineKind http-api is registry metadata only and no HTTP transport exists or is bound in P1',
      resultSemantics: NO_VERDICT_RESULT_SEMANTICS
    }
  }
];

export function listRegisteredDomainProfileIds(): string[] {
  return DOMAIN_ENGINE_PROFILE_REGISTRY.map((entry) => entry.profileId);
}

export function resolveDomainEngineProfile(profileId: string): DomainEngineProfileRegistryEntry {
  const entry = DOMAIN_ENGINE_PROFILE_REGISTRY.find(
    (candidate) => candidate.profileId === profileId
  );
  if (!entry) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'profileId is not registered for this domain transport',
      {
        profileId,
        supportedProfileIds: listRegisteredDomainProfileIds()
      }
    );
  }
  return entry;
}
