"""Explicit PR30 source binding; unchanged v4 behavior and preserved PR27 profile."""
from swbpipe_catalog_v4_receiving import (
    CATALOG_BYTES, CATALOG_SHA256, CATALOG_SNAPSHOT, CATALOG_SOURCES, HERE,
    checked_selection, read_catalog)

FIXTURES = HERE / 'fixtures'
# The supplier's PR30 edition, with the supplier sources read at it. The PR27
# formatter test source was inspected at the predecessor only and is not a
# source of this edition.
SELECTION = {
    'repository': 'sgttomas/SWBPIPE',
    'commit': 'a659523a75dbbf2cdfcccdf8a667b6fb482e10ea',
    'checked_head': '0c729ce5d09636341521f117e075d1a8d07acf32',
    'pull_request': 'https://github.com/sgttomas/SWBPIPE/pull/30',
    'catalog_version': 'swbpipe-catalog/4',
    'snapshot': CATALOG_SNAPSHOT,
    'predecessor_commit': '9b6281e7eaca924e6166336b87b6d25937c1ca04',
    'sources': CATALOG_SOURCES + [
        {'path': 'execution/PKG-16/DEL-16-06/Work/embedded-agent-host.md',
         'snapshot': 'swbpipe-catalog-v4-pr30/embedded-agent-host.source.md',
         'bytes': 53811,
         'sha256': '40b64f0544431c16b10645d0ad69adf0b7f81522be6e82e7dbc78eb190a2766c'},
        {'path': 'apps/desktop/src/services/embeddedAgentSession.ts',
         'snapshot': 'swbpipe-catalog-v4-pr30/embeddedAgentSession.source.ts.txt',
         'bytes': 32813,
         'sha256': 'fa33d85e40b41d8acab10bf7d26c797449524f703eee09bdc9a960836badcf26'},
        {'path': 'apps/desktop/src/features/model-tree/removalIntents.ts',
         'snapshot': 'swbpipe-catalog-v4-pr30/removalIntents.source.ts.txt',
         'bytes': 7889,
         'sha256': 'd7b2f9927daa1a4701655be9185919cc1ea062567f9f0b1b90377f9f4b8f5c5f'},
    ],
}


def selection():
    return checked_selection(SELECTION, FIXTURES, 'v4 PR30')


def load_catalog(path=None):
    pins = selection()
    return read_catalog(FIXTURES / pins['snapshot'] if path is None else path)
