from collections import deque


class JobNode():
    def __init__(self, job_id:int, output_table:str, source_tables:list[str]=[], inheritors:set[str]=set([])):
        self.job_id = job_id    
        self.height = 1
        self.source_tables = source_tables
        self.output_name = output_table
        self.inheritors_tables = inheritors


    def add_inheritors(self, node_inheritor):
        self.inheritors_tables.add(node_inheritor)

    def get_inheritors(self):
        return self.inheritors_tables   

    def get_output_name(self):
        return self.output_name


    def get_job_id(self):
        return self.job_id
        

    def get_source_tables(self):
        return self.source_tables
    

    def get_height(self):
        return self.height


    def set_height(self, set_height:int) -> None:
        self.height = set_height

    

