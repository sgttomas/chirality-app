import { createContext, useContext, useEffect } from "react";

/**
 * Work the person has entered and not sent: a composer draft, a run form with entries. A view that holds such
 * work reports it here, so a move the App makes by itself (the first view at launch, the move after a sign-in)
 * never takes the person away from it. Reporting changes nothing the person sees.
 */
export const UnsentWork = createContext<(owner: string, unsent: boolean) => void>(() => {});
/** Report whether `owner` holds unsent work now; cleared when it unmounts. */
export function useReportUnsent(owner: string, unsent: boolean): void {
  const report = useContext(UnsentWork);
  useEffect(() => { report(owner, unsent); return () => report(owner, false); }, [report, owner, unsent]);
}
