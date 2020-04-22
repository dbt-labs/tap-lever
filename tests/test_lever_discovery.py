import tap_tester.connections as connections
import tap_tester.menagerie   as menagerie
import tap_tester.runner      as runner
import os
import unittest
from functools import reduce

class LeverDiscovery(unittest.TestCase):
    def setUp(self):
        missing_envs = [x for x in [os.getenv('TAP_LEVER_TOKEN')] if x == None]
        if len(missing_envs) != 0:
            raise Exception("set TAP_LEVER_TOKEN")


    def name(self):
        return "tap_tester_lever_discovery"


    def get_type(self):
        return "platform.lever"


    def get_properties(self):
        return {'start_date' : '2020-01-01T00:00:00Z'}

    
    def get_credentials(self):
        return {'token': os.getenv('TAP_LEVER_TOKEN')}


    def tap_name(self):
        return "tap-lever"


    def expected_check_streams(self):
        return {
            'candidates',
            'opportunities',
            'candidate_applications',
            'opportunity_applications',
            'archive_reasons',
            'candidate_offers',
            'postings',
            'candidate_referrals',
            'opportunity_offers',
            'opportunity_referrals',
            'requisitions',
            'candidate_resumes',
            'opportunity_resumes',
            'sources',
            'stages',
            'users'
        }


    def test_run(self):
        conn_id = connections.ensure_connection(self)

        #run in check mode
        check_job_name = runner.run_check_mode(self, conn_id)

        #verify check  exit codes
        exit_status = menagerie.get_exit_status(conn_id, check_job_name)
        menagerie.verify_check_exit_status(self, exit_status, check_job_name)

        found_catalogs = menagerie.get_catalogs(conn_id)
        self.assertGreater(len(found_catalogs), 0, msg="unable to locate schemas for connection {}".format(conn_id))

        found_catalog_names = set(map(lambda c: c['tap_stream_id'], found_catalogs))

        diff = self.expected_check_streams().symmetric_difference( found_catalog_names )
        self.assertEqual(len(diff), 0, msg="discovered schemas do not match: {}".format(diff))
