from typing import List

from .models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from .models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions
from .models.raw.node_definitions.version_1_0.node_definition import Comfy_v1_0_NodeDefinition
from .models.common.workflow import Workflow
from .exceptions import WorkflowParseError

class WorkflowParser:
    @classmethod
    def parse(workflow_data: dict, node_definitions_data: dict) -> Workflow:
        normalized_node_definitions: List[Comfy_v1_0_NodeDefinition] = Comfy_v1_0_NodeDefinitions.model_validate(node_definitions_data).to_normalized()

        workflow_version = workflow_data.get('version', None)
        if workflow_version == 0.4:
            return Comfy_V0_4_Workflow.model_validate(workflow_data).to_normalized(normalized_node_definitions).to_common(normalized_node_definitions)
        raise WorkflowParseError("Invalid workflow version: {}".format(workflow_version))
        
