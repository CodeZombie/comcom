from typing import Self, Dict, List, Tuple

from comcom.comfy_ui.models.raw.workflow.version_0_4.node import ComfyNode
from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import ComfyWorkflow
from comcom.comfy_ui.definition.node_definitions import NodeDefinitions
from comcom.comfy_ui.api_graph.input import ApiInput

from .node import ApiNode

class ApiWorkflow:
    def __init__(self, nodes: Dict[str, ApiNode] = {}):
        self.nodes: Dict[str, ApiNode] = nodes

    # TODO:
    # We need to append the 
    @classmethod
    def from_comfy_workflow(cls, comfy_workflow: ComfyWorkflow, node_definitions: NodeDefinitions) -> Self:
        api_workflow: ApiWorkflow = ApiWorkflow()

        comfy_nodes: List[ComfyNode] = comfy_workflow.nodes.copy()

        # Expand subgraphs.
        for subgraph_definition in comfy_workflow.subgraphs:
            subgraph_instances: List[ComfyNode] = [node for node in comfy_workflow.nodes if node.type == subgraph_definition.id]
            for subgraph_instance in subgraph_instances:
                comfy_nodes.extend(subgraph_definition.get_expanded_nodes(subgraph_instance, node_definitions))

        # Resolve links and create api nodes
        for node in comfy_workflow.nodes:
            api_node: ApiNode = ApiNode(node.type)
            for node_input_name, node_input in node.get_inputs(node_definitions).items():
                if node_input.is_link:
                    # Find the source of this link
                    for comfy_node in comfy_nodes:
                        source_node_id, source_node_output_index = comfy_node.get_output_location_from_link(node_input.value)
                        if source_node_id != None:
                            api_node.inputs[node_input_name] = ApiInput(node_input.value, source_node_id, source_node_output_index)
                            break
                    api_node.inputs[node_input_name] = ApiInput(node_input.value, None, None)
                        
            api_workflow.nodes[node.id] = api_node

        return api_workflow