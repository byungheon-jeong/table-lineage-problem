import json
from unittest import TestCase
from srv.job_node import JobNode
class NodeTest(TestCase):

    @classmethod
    def setUp(self):
        with open("tests/jobs.json", "r") as file:
            self.database = json.load(file)

    def test_node_creation(self):
        job_entry = self.database[0]
        keys = {"_".join(key.split(" ")).lower(): job_info for key,job_info in job_entry.items()}
        job_entry = keys        

        test = JobNode(**job_entry)
        self.assertEqual(test.get_height(),1)
        self.assertEqual(test.get_job_id(), job_entry["job_id"])
        self.assertEqual(test.get_source_tables(), job_entry["source_tables"])

        

