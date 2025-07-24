from srv.job_node import JobNode
from collections import deque

class JobTree(): 
    def __init__(self, list_of_jobs: list[dict]):
        self.node_directory = {}
        self.cur_head = None
        self.job_source = {job["Output Table"]: job for job in list_of_jobs}

        for job in list_of_jobs[1:]:
            self.add_job_get_height(job)


    def get_table(self, name_of_table: str) -> JobNode:
        return self.node_directory.get(name_of_table, None)


    def get_job_name_of_table(self, source_table_name: str):
        return self.job_source[source_table_name]


    def bubble_up_to_support(self, node: JobNode):
        dfs = deque()
    
        dfs.appendleft(node)

        while dfs:
            node = dfs.pop()
            inheritors = node.get_inheritors()
            height = node.get_height() + 1

            for heir in inheritors:
                heir.set_height(height)
                dfs.appendleft(heir)
            
        

            

    def add_job_get_height(self, job_info: dict):
        bfs_node = deque()
        
        node = self.node_directory.get(job_info["Output Table"], None)
        
        if node:
            return node.get_height()

        # if node does not exist
        job_info = {"_".join(key.split(" ")).lower(): info for key,info in job_info.items()}
        node = JobNode(**job_info)
        self.node_directory[node.output_name] = node

        height_tracker = []

        for source_table in node.get_source_tables():
            # BASE Case, exit
            if source_table == "SOURCE TABLES":
                return 0
            
            source_node = self.get_table(source_table)
            
            if source_node:
                source_node.add_inheritors(node)
                height_tracker.append(source_node.get_height() + 1)
            
            else:
                job_name = self.get_job_name_of_table(source_table)
                height_tracker.append(self.add_job_get_height(job_name) + 1)

        height = max(height_tracker)
        node.set_height(height)


        
        # for node.get_source_tables():
        



        return height        

    def get_similarity(self, node1:JobNode, node2:JobNode) -> float:

        bfs = deque()







            