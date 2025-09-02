class InvalidNodeInWorkflowExceptionc(Exception):
    def __init__(self, node_name: str, workflow_name: str, node_id: str, specific_problem_description: str = ""):
        super().__init__()
        self.node_name = node_name
        self.node_id = node_id
        self.workflow_name = workflow_name
        self.specific_problem_description = specific_problem_description
    
    def __str__(self):
        return "Invalid Node \"{}\" ({}) in workflow \"{}\": {}".format(
            self.node_name,
            self.node_id,
            self.workflow_name,
            self.specific_problem_description
        )
    
class RecipeException(Exception): pass