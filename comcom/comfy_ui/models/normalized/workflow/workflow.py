from dataclasses import dataclass
from typing import List
import copy

from .node import NormalizedNode
from .subgraph_definition import NormalizedSubgraphDefinition

from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition
from comcom.comfy_ui.models.normalized.node_definition.slot_definition import NormalizedSlotDefinition

from comcom.comfy_ui.models.common.node import Node
from comcom.comfy_ui.models.common.workflow import Workflow
from comcom.comfy_ui.models.common.output import Output

@dataclass
class NormalizedWorkflow:
    id: str
    revision: int
    version: int
    nodes: list[NormalizedNode]
    subgraph_definitions: list[NormalizedSubgraphDefinition]

    def get_subgraph_definition_by_id(self, id: str) -> NormalizedSubgraphDefinition | None:
        return next((subgraph_definition for subgraph_definition in self.subgraph_definitions if subgraph_definition.id == id), None)
    
    def get_node(self, id: str) -> NormalizedNode | None:
        return next((node for node in self.nodes if node.id == id), None)

    def to_common(self, node_definitions: List[NormalizedNodeDefinition]):
        def is_node_valid(node: NormalizedNode) -> bool:
            if node.type == 'Reroute': return False
            if node.muted: return False
            if node.type in [subgraph_definition.id for subgraph_definition in self.subgraph_definitions]: 
                return False
            return True
        
        # Filter out invalid nodes
        regular_nodes: List[NormalizedNode] = [copy.deepcopy(node) for node in self.nodes if is_node_valid(node)]
        reroute_nodes = [copy.deepcopy(node) for node in self.nodes if node.type == 'Reroute']
        muted_nodes = [copy.deepcopy(node) for node in self.nodes if node.muted]

        # Find all subgraph instances
        subgraph_instance_nodes = [copy.deepcopy(node) for node in self.nodes if node.type in [subgraph_definition.id for subgraph_definition in self.subgraph_definitions]]

        for subgraph_instance_node in subgraph_instance_nodes:
            subgraph_definition = self.get_subgraph_definition_by_id(subgraph_instance_node.type)
            regular_nodes.extend(subgraph_definition.as_normalized_node_list(subgraph_instance_node, node_definitions, self.subgraph_definitions, prefix=""))
            subgraph_ext_bypasses = subgraph_definition.get_external_bypasses(subgraph_instance_node)
            for node in regular_nodes + reroute_nodes + muted_nodes + subgraph_instance_nodes:
                node.apply_bypasses(subgraph_ext_bypasses)

        # Bypass all reroutes
        for reroute_node in reroute_nodes:
            bypasses = reroute_node.get_bypasses()
            # Apply bypass map to all nodes
            for node in regular_nodes + reroute_nodes + muted_nodes + subgraph_instance_nodes:
                node.apply_bypasses(bypasses)

        # Bypass all muted nodes
        for muted_node in muted_nodes:
            bypasses = muted_node.get_bypasses()
            for node in regular_nodes + reroute_nodes + muted_nodes + subgraph_instance_nodes:
                node.apply_bypasses(bypasses)

        # Resolve all links
        resolved_nodes: List[Node] = []
        for node_to_resolve in regular_nodes:
            resolved_nodes.append(Node(
                id=node_to_resolve.id,
                type=node_to_resolve.type,
                inputs=[input.to_common(regular_nodes) for input in node_to_resolve.inputs],
                outputs=[Output(i, node_to_resolve.outputs[i].name) for i in range(len(node_to_resolve.outputs))]
            ))
        
        return Workflow(
            id=self.id,
            revision=self.revision,
            nodes=resolved_nodes,
            version=self.version
        )
