# TODO
- Create an AbstractNormalizedGraph class which implements a "to_flattened_nodes(...) -> List[NormalizedNodes]"
- NormalizedWorkflow and NormalizedSubgraph should both inherit from AbstractNormalizedGraph

- NormalizedSubgraphDefinition should inherit from NodeDefinition so we can use it without converting it to first.
- Bypass logic should live inside of NormalizedNode. Maybe as a "to_flattened" method? this method should return a Bypass to be applied to other nodes.

- >>> Normalized and Comfy Workflows and SubgraphDefinitions should never be modified while generating the next level version.




Create a NormalizedSubgraphNode that inherits from NormalizedNode.
Then the init just gets passed a list of NodeDefinitions (including the NormalizedSubgraphDefinition) and everything Just Works (tm)

perhaps we should fold NormalizedLinkInput and NormalizedInput into one single format?