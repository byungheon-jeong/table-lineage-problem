from srv.job_tree import JobTree
from test_node import NodeTest

class TreeTest(NodeTest):
    def test_tree_gen(self):
        # self.database is defined in the NodeTest Class
        test_tree = JobTree(self.database)
        debug = {node.get_output_name(): node.get_height() for node in test_tree.node_directory.values()} 
        self.assertTrue(test_tree)
        self.assertEqual(test_tree.get_node("B").get_height(), 3)
        self.assertEqual(test_tree.get_node("Z").get_height(), 3)
        self.assertEqual(test_tree.get_node("Q*").get_height(), 3)
        self.assertEqual(test_tree.get_node("X").get_height(), 3)
        self.assertEqual(test_tree.get_node("C").get_height(), 2)
        self.assertEqual(test_tree.get_node("D").get_height(), 2)
        self.assertEqual(test_tree.get_node("E").get_height(), 2)
        self.assertEqual(test_tree.get_node("Q").get_height(), 2)
        self.assertEqual(test_tree.get_node("AA").get_height(), 1)
        self.assertEqual(test_tree.get_node("AB").get_height(), 1)
        self.assertEqual(test_tree.get_node("AC").get_height(), 1)
        self.assertEqual(test_tree.get_node("AD").get_height(), 1)
        self.assertEqual(test_tree.get_node("AE").get_height(), 1)
        print(test_tree)


    def test_similiarty(self):
        test_tree = JobTree(self.database)

        node_a = test_tree.get_node("X")
        node_b = test_tree.get_node("D")
        self.assertEqual(test_tree.calculate_similarity(node_a, node_b), 0)

        node_a = test_tree.get_node("Z")
        node_b = test_tree.get_node("D")
        self.assertEqual(test_tree.calculate_similarity(node_a, node_b), 0.25)

        node_a = test_tree.get_node("E")
        node_b = test_tree.get_node("D")
        self.assertEqual(test_tree.calculate_similarity(node_a, node_b), 0)

        node_a = test_tree.get_node("C")
        node_b = test_tree.get_node("D")
        self.assertEqual(test_tree.calculate_similarity(node_a, node_b), 0.5)

        node_a = test_tree.get_node("Q*")
        node_b = test_tree.get_node("X")
        # This is a limitation on the current method of similarity calcuation. X has an additional source table that Q* does 
        # not have. This should be penalized. 
        self.assertEqual(test_tree.calculate_similarity(node_a, node_b), 0.75)
