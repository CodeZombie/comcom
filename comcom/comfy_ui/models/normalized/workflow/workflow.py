from typing import List
from dataclasses import dataclass

from .node import NormalizedNode
from .subgraph_definition import NormalizedSubgraphDefinition

from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition

from comcom.comfy_ui.models.common.node import Node
from comcom.comfy_ui.models.common.workflow import Workflow

@dataclass
class NormalizedWorkflow:
    id: str
    revision: int
    nodes: list[NormalizedNode]
    version: float
    subgraph_definitions: list[NormalizedSubgraphDefinition]

    def get_subgraph_instance_by_id(self, id: str) -> NormalizedSubgraphDefinition | None:
        return next((subgraph_definition for subgraph_definition in self.subgraph_definitions if subgraph_definition.id == id), None)

    def to_common(self, node_definitions: List[NormalizedNodeDefinition]):
        def is_node_valid(node: NormalizedNode) -> bool:
            if node.type == 'Reroute': return False
            if node.muted: return False
            if node.type in [subgraph_definition.id for subgraph_definition in self.subgraph_definitions]: return False
            return True
        
        def get_node_definition(definition_type: str) -> NormalizedNodeDefinition | None:
            return next((node_definition for node_definition in node_definitions if node_definition.type == definition_type), None)
        
        # Filter out invalid nodes
        nodes: List[NormalizedNode] = [node for node in self.nodes if is_node_valid(node)]

        # Find all subgraph instances
        subgraph_instance_nodes = [node for node in self.nodes if node.type in [subgraph_definition.id for subgraph_definition in self.subgraph_definitions]]

        # Convert subgraph instances to NormalizedNode list
        for subgraph_instance_node in subgraph_instance_nodes:
            nodes.extend(self.get_subgraph_instance_by_id(subgraph_instance_node.type).as_normalized_node_list(subgraph_instance_node, node_definitions))

        # Bypass all reroutes
        reroute_nodes = [node for node in nodes if node.type == 'Reroute']
        for reroute_node in reroute_nodes:
            bypass_map = reroute_node.get_bypass_map(get_node_definition('Reroute'))
            # Apply bypass map to all nodes
            # ...

        # Bypass all muted nodes
        muted_nodes = [node for node in nodes if node.muted]
        for muted_node in muted_nodes:
            bypass_map = muted_node.get_bypass_map(get_node_definition(muted_node.type))
            # Apply bypass map to all nodes
            # ...

        # Resolve all links
        resolved_nodes: List[Node] = []
        for node_to_resolve in nodes:
            resolved_nodes.append(Node(
                id=node_to_resolve.id,
                type=node_to_resolve.type,
                inputs=[input.to_common(nodes) for input in node_to_resolve.get_inputs(get_node_definition(node_to_resolve.type)).values()],
            ))
        
        return Workflow(
            id=self.id,
            revision=self.revision,
            nodes=resolved_nodes,
            version=self.version
        )
    
    ## TODO:
    #   node.get_inputs needs to be able to work with both a NormalizedNodeDefinition AND NormalizedSubgraphDefinition. make this work,
            
