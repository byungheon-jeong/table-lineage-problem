from srv.job_node import JobNode
from collections import deque
from collections import defaultdict
class JobTree(): 
    def __init__(self, list_of_jobs: list[dict]):
        self.node_directory = {}
        self.cur_head = None
        self.job_source = {job["Output Table"]: job for job in list_of_jobs}

        for job in list_of_jobs:
            self.add_job_get_height(job)


    def get_node(self, name_of_table: str) -> JobNode:
        return self.node_directory.get(name_of_table, None)


    def get_job_name_of_table(self, source_table_name: str) -> dict:
        return self.job_source[source_table_name]


    def bubble_up_to_support(self, node: JobNode) -> None:
        dfs = deque()
    
        dfs.appendleft(node)

        while dfs:
            node = dfs.pop()
            inheritors = node.get_inheritors()
            height = node.get_height() + 1

            for heir in set(inheritors):
                heir.set_height(height)
                dfs.appendleft(heir)


    def add_job_get_height(self, job_info: dict) -> int:
        node = self.node_directory.get(job_info["Output Table"], None)
        
        if node:
            return node.get_height()

        # if node does not exist
        job_info = {"_".join(key.split(" ")).lower(): info for key,info in job_info.items()}
        node = JobNode(**job_info)
        self.node_directory[node.output_name] = node

        height_tracker = []

        for source_table in node.get_source_tables():
            # BASE Case, exit loop
            if source_table == "SOURCE TABLES":
                # We are appending 1 b/c this is base case
                height_tracker.append(1)
            
            else:
                source_node_name = self.get_job_name_of_table(source_table)
                source_node = self.get_node(source_node_name["Output Table"])
                
                if source_node:
                    source_node.add_inheritors(node)
                    height_tracker.append(source_node.get_height() + 1)
                
                else:
                    job_name = self.get_job_name_of_table(source_table)
                    height_tracker.append(self.add_job_get_height(job_name) + 1)

        height = max(height_tracker)
        node.set_height(height)

        self.bubble_up_to_support(node)
        
        # for node.get_source_tables():
        
        return height        

    def calculate_similarity(self, node1:JobNode, node2:JobNode) -> float:


        similarity_score = 0

        bfs_a = deque()
        bfs_b = deque()
        
        bfs_a.appendleft(node1)
        bfs_b.appendleft(node2)

        recursive_source_tables_a = defaultdict(set)
        recursive_source_tables_b = defaultdict(set)

        while bfs_a:
            node = bfs_a.pop()
            cur_height = node.get_height()
            output_table_name = node.get_output_name()
            recursive_source_tables_a[cur_height].add(output_table_name)
            for table in node.get_source_tables():
                source_node = self.get_node(table)
                # Control for Global Source Tables
                if source_node:
                    bfs_a.appendleft(source_node)
            
        while bfs_b:
            node = bfs_b.pop()
            cur_height = node.get_height()
            output_table_name = node.get_output_name()
            recursive_source_tables_b[cur_height].add(output_table_name)
            for table in node.get_source_tables():
                source_node = self.get_node(table)
                # Control for Global Source Tables
                if source_node:
                    bfs_b.appendleft(source_node)
            
        n1_height = node1.get_height()
        n2_height= node2.get_height()
        current_height = min(n1_height, n2_height)
        max_height = max(n1_height, n2_height)

        while current_height > 0:
            # To weigh the different "levels" of the source table graph as more distant common tables should be counted for less
            distance_multiplier = 0.5**(max_height - current_height)

            node_a_source_tables_at_cur_level = recursive_source_tables_a[current_height]
            node_b_source_tables_at_cur_level = recursive_source_tables_b[current_height]
            # We are counting the number of shared source tables of node_a and node_b at each "level"
            number_of_common_source_tables = len(node_a_source_tables_at_cur_level & node_b_source_tables_at_cur_level)
            
            similarity_score += (distance_multiplier * number_of_common_source_tables)
            current_height -= 1
        return similarity_score


        # while current_height > 0 and bfs_a and bfs_b:
        #     source_tables_at_cur_level_a = set()
        #     source_tables_at_cur_level_b = set()
            
        #     node_a = bfs_a.pop()
        #     node_b = bfs_b.pop()

        #     for source_table_names in node_a.get_source_tables():
        #         job_node = self.get_node(source_table_names)
        #         job_height = job_node.get_height()
        #         if job_node.get_height() == current_height:
        #             source_tables_at_cur_level_a.add(job_node.get_output_name())
        #         elif job_node.get_height() < current_height:
        #             bfs_a.pop()



        # while bfs_a and bfs_b:
        #     node1 = bfs_a.pop()
        #     node2 = bfs_b.pop()
        #     n1_height = node1.get_height()
        #     n2_height= node2.get_height()











            