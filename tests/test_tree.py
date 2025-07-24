from srv.job_tree import JobTree
from test_node import NodeTest

class TreeTest(NodeTest):
    def test_tree_gen(self):
        test_tree = JobTree(self.database)
        self.assertTrue(test_tree)