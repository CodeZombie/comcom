How muting works:
When you mute a node, comfy will re-link all the outputs to the inputs.

For Example, imagine this workflow:

Node 1:
    Load Image
    Outputs:
        links: [4]

Node 2:
    Merge Images
    Input:
        image_a 4
        image_b: None
    Outputs:
        output_a: [5]
        output_b: [6]

Node 3:
    Preview Image
    Input:
        image: 6

When you disable Node 2,
Every output node is mapped exclusively with an input of the same type, in order.
1. output_a looks for the first INPUT node of the same type. in this case, `image_a`
2. output_b looks for the first INPUT node of the same type that hasn't already been assigned. In this case, `image_b.
Neither of these processes check to see if the inputs are even connected. It just naively links them up.

To link them up, we should just find the output node for each of node_2's inputs and add all the output links into that. This should effectively bypass the node.
Once this is all done, we just delete node 2.
We dont need to clean up any of the input links manually, when we construct the API prompt we should just omit any non-resolved Links.