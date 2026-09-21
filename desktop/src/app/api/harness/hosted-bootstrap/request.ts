import { readJsonBody, requireNonEmptyString } from '../../../../lib/harness/http';

type HostedBootstrapRequest = {
  projectRoot?: unknown;
};

export async function readHostedBootstrapProjectRoot(request: Request): Promise<string> {
  const body = await readJsonBody<HostedBootstrapRequest>(request);
  return requireNonEmptyString(body.projectRoot, 'projectRoot');
}
