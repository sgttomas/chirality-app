import { DocKind, Finals, Triple, DS, SP, X, M, W, U, Round } from './contracts';
import { buildSystem } from './systemPrompt';
import { buildUser } from './userPrompt';
import { retrieveSummary } from './rag/retrieve';
import { callJSON } from './vendor/llm';
import { guard } from './validators';
import { compactDS, compactSP, compactX, compactM } from './compactor';

/**
 * Optionally accepts:
 *  - extraConstraints: step-scoped constraints injected into the user prompt
 *  - upstreamOverride: specific prior docs to consider for this step (used by the orchestrator)
 */
export async function runDoc(
  kind: DocKind,
  problem: { title: string; statement: string; initialVector: string[] },
  finals: Finals,
  opts?: {
    extraConstraints?: string[];
    upstreamOverride?: Partial<Record<DocKind, Triple<any>>>;
  }
): Promise<Triple<DS | SP | X | M>> {
  const upstream = (() => {
    // Prefer explicit upstream from the orchestrator (per-round), otherwise fall back to latest finals
    const o = opts?.upstreamOverride;
    if (o && Object.keys(o).length) {
      return {
        DS: o.DS ? compactDS(o.DS.text) : undefined,
        SP: o.SP ? compactSP(o.SP.text) : undefined,
        X:  o.X  ? compactX(o.X.text)   : undefined,
        M:  o.M  ? compactM(o.M.text)   : undefined,
      };
    }
    return {
      DS: finals.DS ? compactDS(finals.DS.text) : undefined,
      SP: finals.SP ? compactSP(finals.SP.text) : undefined,
      X:  finals.X  ? compactX(finals.X.text)   : undefined,
      M:  finals.M  ? compactM(finals.M.text)   : undefined,
    };
  })();
  
  const retrieved = await retrieveSummary(problem.statement, 12);
  const system = buildSystem(problem.title, finals);
  const user = buildUser(kind, {
    problemStatement: problem.statement,
    initialVector: problem.initialVector,
    upstream, 
    retrieved,
    constraints: [
      'Prefer cited evidence when available.',
      'Populate source_refs/refs/trace_back with citation IDs (CIT:src#p).',
      'No filler; keep payload fields crisp and specific.',
      ...(opts?.extraConstraints || []),
    ],
  });

  try {
    // Two-pass generation: propose then finalize
    const draft = await callJSON(system, user, { temperature: 0.7 });
    const final = await callJSON(system, user, { temperature: 0.5, prior: draft });

    // Handle extra wrapper layer that LLM sometimes adds
    let processedFinal = final;
    
    // Case 1: Wrapped in text.KIND format
    if (final?.text && typeof final.text === 'object' && final.text[kind]) {
      console.log(`Unwrapping extra ${kind} layer from text wrapper`);
      processedFinal = {
        ...final,
        text: final.text[kind]
      };
    } 
    // Case 2: Direct KIND wrapper without text layer
    else if (final && final[kind] && !final.text) {
      console.log(`Unwrapping direct ${kind} wrapper`);
      processedFinal = {
        text: final[kind],
        terms_used: final.terms_used || [],
        warnings: final.warnings || []
      };
    }

    if (!guard.triple(processedFinal)) {
      console.log('Triple validation failed for:', JSON.stringify(processedFinal, null, 2));
      throw new Error('Triple shape invalid');
    }
    // Per-kind payload validation for stronger guarantees
    const payload = (processedFinal as any).text;
    const payloadOk =
      (kind === 'DS' && guard.DS?.(payload)) ||
      (kind === 'SP' && guard.SP?.(payload)) ||
      (kind === 'X'  && guard.X?.(payload))  ||
      (kind === 'M'  && guard.M?.(payload));
    if (!payloadOk) {
      console.log(`${kind} payload validation failed for:`, JSON.stringify(payload, null, 2));
      throw new Error(`${kind} payload invalid`);
    }
    
    return processedFinal as Triple<any>;
  } catch (error) {
    console.error(`Error generating ${kind}:`, error);
    // Return a minimal valid structure on error
    return {
      text: kind === 'DS' ? { data_field: 'Error generating document' } as any :
            kind === 'SP' ? { step: 'Error generating document' } as any :
            kind === 'X' ? { heading: 'Error', narrative: 'Error generating document' } as any :
            { statement: 'Error generating document' } as any,
      terms_used: [],
      warnings: [`Generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`]
    };
  }
}

export function diffW<T extends object>(prev: T, next: T): W {
  const changed: string[] = [];
  const keys = new Set([...Object.keys(prev || {}), ...Object.keys(next || {})]);
  keys.forEach(k => {
    if (JSON.stringify((prev as any)[k]) !== JSON.stringify((next as any)[k])) {
      changed.push(k);
    }
  });
  return { 
    changed_keys: changed, 
    reason: 'Auto-diff', 
    evidence: [] 
  };
}

export function synthesizeU(round: Round, finals: Finals): U {
  const risks = (finals.M?.text.residual_risk || []).length;
  const convergence = risks ? (round === 3 ? 'Partial' : 'Open') : 'Closed';
  const summary = `Round ${round}: ${convergence}.`;
  return { 
    round, 
    convergence, 
    open_issues: risks ? finals.M?.text.residual_risk : [], 
    summary 
  };
}

// ---------------------------
// Iterative Orchestration API
// ---------------------------

type Version = 1 | 2 | 3;

export interface OrchestrationProgress {
  phase: 'start' | 'success' | 'error';
  kind: DocKind;
  version: Version;
  deps: string[];
  ms?: number;
  error?: string;
}

function stepConstraints(kind: DocKind, v: Version, deps: Partial<Record<DocKind, any>>) {
  const label = { DS: 'Data Sheet', SP: 'Standard Procedure', X: 'Solution Template', M: 'Guidance' }[kind];
  const depList = Object.keys(deps).length
    ? Object.keys(deps).map(k => `${k} V${v === 1 ? 1 : v - 1}`).join(', ')
    : 'none';
  return [
    `You are generating: ${label} V${v}.`,
    `Consider only these dependencies: ${depList}.`,
    `Do not regenerate other documents.`,
    `Emit strictly the Triple JSON for ${kind} (no extra fields, no prose).`
  ];
}

/**
 * Serial, three-round orchestration:
 *   Round V1: DS → SP → X → M
 *   Round V2: DS → SP → X → M (each step considers prior round outputs)
 *   Round V3: DS → SP → X → M
 *
 * Returns the final finals (latest) and a per-round history, plus U3 summary.
 */
export async function orchestrateProblem(
  problem: { title: string; statement: string; initialVector: string[] },
  options?: { onProgress?: (event: OrchestrationProgress) => void }
): Promise<{ finals: Finals; history: Record<Version, Partial<Finals>>; U3: U }> {
  const history: Record<Version, Partial<Finals>> = { 1: {}, 2: {}, 3: {} };
  let finals: Finals = {};

  const call = async <T>(kind: DocKind, v: Version, deps: Partial<Record<DocKind, Triple<any>>>): Promise<Triple<T>> => {
    const depKeys = Object.keys(deps);
    const startTime = Date.now();
    
    options?.onProgress?.({
      phase: 'start',
      kind,
      version: v,
      deps: depKeys
    });
    
    try {
      const extraConstraints = stepConstraints(kind, v, deps);
      const result = await runDoc(kind, problem, finals, {
        extraConstraints,
        upstreamOverride: deps
      }) as Triple<T>;
      
      options?.onProgress?.({
        phase: 'success',
        kind,
        version: v,
        deps: depKeys,
        ms: Date.now() - startTime
      });
      
      return result;
    } catch (error) {
      options?.onProgress?.({
        phase: 'error',
        kind,
        version: v,
        deps: depKeys,
        ms: Date.now() - startTime,
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  };

  // ----- V1
  history[1].DS = finals.DS = await call<DS>('DS', 1, {});
  history[1].SP = finals.SP = await call<SP>('SP', 1, { DS: finals.DS! });
  history[1].X  = finals.X  = await call<X>('X',  1, { DS: finals.DS!, SP: finals.SP! });
  history[1].M  = finals.M  = await call<M>('M',  1, { DS: finals.DS!, SP: finals.SP!, X: finals.X! });

  // ----- V2
  history[2].DS = finals.DS = await call<DS>('DS', 2, { SP: history[1].SP!, X: history[1].X!, M: history[1].M! });
  history[2].SP = finals.SP = await call<SP>('SP', 2, { DS: finals.DS!, X: history[1].X!, M: history[1].M! });
  history[2].X  = finals.X  = await call<X>('X',  2, { DS: finals.DS!, SP: finals.SP!, M: history[1].M! });
  history[2].M  = finals.M  = await call<M>('M',  2, { DS: finals.DS!, SP: finals.SP!, X: finals.X! });

  // ----- V3
  history[3].DS = finals.DS = await call<DS>('DS', 3, { SP: history[2].SP!, X: history[2].X!, M: history[2].M! });
  history[3].SP = finals.SP = await call<SP>('SP', 3, { DS: finals.DS!, X: history[2].X!, M: history[2].M! });
  history[3].X  = finals.X  = await call<X>('X',  3, { DS: finals.DS!, SP: finals.SP!, M: history[2].M! });
  history[3].M  = finals.M  = await call<M>('M',  3, { DS: finals.DS!, SP: finals.SP!, X: finals.X! });

  const U3 = synthesizeU(3, finals);
  return { finals, history, U3 };
}