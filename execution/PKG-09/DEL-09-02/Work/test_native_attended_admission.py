import copy
import unittest
from native_attended_admission import three_row_setup_end

class Tests(unittest.TestCase):
    def rows(self):return [{'kind':'session_started','session':'invented-A','previousSessionEnd':'none'},
        {'kind':'quit_requested','session':'invented-A','liveTurns':[],'outstandingEntries':[],'activeDescendants':[]},
        {'kind':'session_ended','session':'invented-A','how':'quit','stopRequests':[]}]
    def test_only_exact_initial_clean_empty_three_rows(self):
        self.assertEqual(three_row_setup_end(self.rows(),'invented-A')['row_count'],3)
    def test_extra_wrong_end_work_or_prior_session_refused(self):
        for case in ['extra','end','work','previous','session']:
            with self.subTest(case=case):
                r=self.rows()
                if case=='extra':r.append(copy.deepcopy(r[-1]))
                if case=='end':r[-1]['how']='crash'
                if case=='work':r[1]['liveTurns']=['unexpected']
                if case=='previous':r[0]['previousSessionEnd']='clean'
                if case=='session':r[-1]['session']='other'
                with self.assertRaises(RuntimeError):three_row_setup_end(r,'invented-A')
