from collections import deque


class JobNode():
    def __init__(self, job_id:int, output_table:str, source_tables:list[str]=None, inheritors:set[str]=None):
        self.job_id = job_id    
        self.height = 1
        self.source_tables = source_tables
        self.output_name = output_table
        self.inheritors_tables = set()


    def get_inheritors(self) -> set:
        return self.inheritors_tables   


    def add_inheritors(self, new_inheritor):
        self.inheritors_tables.add(new_inheritor)

    # This is the name of the table that the job outputs. This output_name (not job id) is the actual index that we are interested in
    def get_output_name(self) -> str:
        return self.output_name


    def get_job_id(self):
        return self.job_id
        

    def get_source_tables(self) -> list:
        return self.source_tables
    

    def get_height(self) -> int:
        return self.height


    def set_height(self, set_height:int) -> None:
        self.height = set_height

    