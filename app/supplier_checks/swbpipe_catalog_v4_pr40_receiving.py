"""Explicit PR40 source and hash-boundary binding; preserved PR27/PR30 profiles."""
from swbpipe_catalog_v4_receiving import (
    CATALOG_BYTES, CATALOG_SHA256, CATALOG_SNAPSHOT, CATALOG_SOURCES, HERE,
    checked_selection, read_catalog)

FIXTURES = HERE / 'fixtures'
# The supplier's PR40 edition, with the supplier sources read at it. The host
# contract and the shared formatter are byte-identical to PR30 and keep its snapshots.
SELECTION = {
    'repository': 'sgttomas/SWBPIPE',
    'commit': 'cc91aadc9822c5c1d8ba3d883a3ee220dddc1b65',
    'checked_head': '57f5028328bfa50b0a525b7186926a9da88979dc',
    'pull_request': 'https://github.com/sgttomas/SWBPIPE/pull/40',
    'catalog_version': 'swbpipe-catalog/4',
    'snapshot': CATALOG_SNAPSHOT,
    'predecessor_commit': 'a659523a75dbbf2cdfcccdf8a667b6fb482e10ea',
    'sources': CATALOG_SOURCES + [
        {'path': 'execution/PKG-16/DEL-16-06/Work/embedded-agent-host.md',
         'snapshot': 'swbpipe-catalog-v4-pr30/embedded-agent-host.source.md',
         'bytes': 53811,
         'sha256': '40b64f0544431c16b10645d0ad69adf0b7f81522be6e82e7dbc78eb190a2766c'},
        {'path': 'apps/desktop/src/features/model-tree/removalIntents.ts',
         'snapshot': 'swbpipe-catalog-v4-pr30/removalIntents.source.ts.txt',
         'bytes': 7889,
         'sha256': 'd7b2f9927daa1a4701655be9185919cc1ea062567f9f0b1b90377f9f4b8f5c5f'},
        {'path': 'apps/desktop/src/services/embeddedAgentSession.ts',
         'snapshot': 'swbpipe-catalog-v4-pr40/embeddedAgentSession.source.ts.txt',
         'bytes': 33980,
         'sha256': '732dba10c224b102e8da9ffb43476a2d0067d778edc7dc47f12305ad11227a1e'},
        {'path': 'apps/desktop/src/features/workspace/workspaceSession.ts',
         'snapshot': 'swbpipe-catalog-v4-pr40/workspaceSession.source.ts.txt',
         'bytes': 205070,
         'sha256': '97dd3f1908ed733d99498a921b2be37d6513f048122db980eb8db5b95f90d009'},
        {'path': 'execution/PKG-16/DEL-16-06/Work/agent-live-session.md',
         'snapshot': 'swbpipe-catalog-v4-pr40/agent-live-session.source.md',
         'bytes': 16928,
         'sha256': '334689dd04ebafececedadee45fc343258831c3f05f190976727070007523c1b'},
        {'path': 'apps/desktop/src/features/workspace/agentWorkspaceSnapshot.session.test.tsx',
         'snapshot': 'swbpipe-catalog-v4-pr40/agentWorkspaceSnapshot.session.test.source.tsx.txt',
         'bytes': 5230,
         'sha256': '271f5e9075581af815a1c28b3d6e42045466ffd31164f4364764770fdf834bd9'},
        {'path': 'apps/desktop/src/services/embeddedAgentSession.test.ts',
         'snapshot': 'swbpipe-catalog-v4-pr40/embeddedAgentSession.test.source.ts.txt',
         'bytes': 24930,
         'sha256': '7b9ebc151459edb3915585443b4aea79b588780d53281c8e380621dd89a78601'},
    ],
}


def selection():
    return checked_selection(SELECTION, FIXTURES, 'v4 PR40')


def load_catalog(path=None):
    pins = selection()
    return read_catalog(FIXTURES / pins['snapshot'] if path is None else path)
