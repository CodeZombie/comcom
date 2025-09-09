# TODO
- `comcom new` should create a proper folder structure at cwd.
- implement RICH so we can print out better errors and what not. Try to use rich to implement trees to show the user what their outputs are going to look like
    if they `inspect` a solved workflow.

- confirm that 'reroutes' in the extras table in raw workflow files work.
- It appears as though link ids by default already "bypass" these kinds of reroutes, so it's unlikely we need to actually do anything.



# NOTES ABOUT IMAGE SYNC:

if we can control the saved filename on upload, we can set the filename to the UUIDv5 of the resolved workflow that generated it. This will give us a guaranteed random name that is deterministically linked to the contents of the workflow.
This way when the user wants to generate the image again, we can just generate the check to see if that file exists on the server.
WAIT NO WE CANT - Because the external input files might change. Everything about the workflow would look the same, but the external file would be different, and thus produce the same UUIDv5, and the workflow wouldn't regenerate.

We may not be able to control the names of the remote files, but we can store links to remote files in metadata files.

BUT WHAT IF:
we check the hash of the image live before loading them into workflows?
I think we have to do this anyway:
1. Calculate the hash of the image
2. Compare it against the hash in the metadata file
3. if it's not the same, upload the new image to Comfy and update the hash in the metadata file.

Now when the user wants to run a downstream workflow with an image input:
1. The input filepath is found.
2. The hash of the image on disk is calculated and compared against the hash in the metadata file.
3. If the hashes are the same, we grab the comfyui image link from the metadata file.
4. If they're not the same, upload the image to comfyui, and update the metadata file to include the new hash and the new comfyui link

# Comfyui really made everything annoying and complicated by having two different Load Image nodes.
`Load Image` can load images that are uploaded to the `input` folder, but cannot load images that were generated as """outputs""" from other workflows. If you want to use them there, you have to either:
1. Re-upload the image via `<server>/image/upload` (insane)
2. Switch the `load image` node to a `Load Image (from Outputs)` and append ` [output]` to the end of the remote filename 
option 2 is also insane, but doesn't incur a runtime cost, we we're going to do that.
For now we're including the ' [output]' string in the remote filename in the metadata, but in the future we're going to just include 'type' (which I believe is provided by the return data from the image gen) in the metadata, and just handle that in-code.
We're also going to write something to swap `Load Image` to `Load Image (from output)` nodes on the fly if the loaded image is detected as an "output" image so the exchange is totally transparent to the user.


# Big todo:
Figure out why running the same workflow twice, without changing either images or workflow data, causes it to run again if you run a different workflow in-between.

Actually, I don't need to figure this out. I already know.
It's because running a second workflow unloads the state of the last one.
We need to manage workflow state manually.
We can do this by storing a hash of the entire workflow data and all input images in a metadata file and reading that before generating.
Not sure where we're gonna store this metadata file. Maybe in a hidden folder???

I think we should do a few things:
1. Resolve all input images on `WorkflowInstance` init. This way we always have the paths available.
2. Generate a hash of the api workflow (that is, the entire resolved `CommonWorkflow.to_api_dict` dict) 
   PLUS the hashes of the input images. Store this hash in the `WorkflowInstance` object.
3. Now when we go to run a WorkflowInstance, we compare the cached hash to the current hash value. If they're the same, do the following:
    3.1. Check to see if the output files exist on disk and have metadata files AND that the metadata hashes match the actual hashes of the images.
    3.2. If any of these conditions fail, run the workflow.
   If they're not the same, run the workflow.

Workflow Instance Hash algorithm:
1. Inside the WorkflowInstance.__init__ method, generate the `CommonWorkflow.to_api_dict` dict. Store this as `a`
2. Generate a hash of all the input images (actual image hashes, not the cached hash). Store this as `b`.
3. Store `hash(a + b)` as `WorkflowInstance.hash`
Now, when we try to run the workflow:

The WorkflowInstance should also have a `is_dirty` property, which does the following:
1. If the metadata file does not exist, return `True`
2. If the hash in the metadata file does not match this instance's hash, return True.
3. For each Output Image:
    1. Check to see if the output file exists. If it does not, return `True`
    2. Check to see if the output file has a metadata file. If it does not, return `True`
    3. Check to see if the output file's hash matches the actual hash of the image. If it does not, return `True`
4. Return `False`

The WorkflowInstance should have a `.execute()` method which takes a `ComfyServer`.
The WorkflowInstance.__init__ should also recieve a path to it's future metadata file.
Note: metadata paths should be constructed as directories, not `path.to.my.workflow` because workflows can nest infinitely deep, and filenames can only be so long.


# vscode syntax highlighting for yaml recipes
The recipe yaml format is both specifically structured and includes some special non-standard features.
It would be incredibly useful to have some special syntax highlighting in vscode for editing recipe files.
At minimum, some special highlighting for the different sections (values, load, input, output) of recipes.
However, if at all possible, it would be excellent to turn this into an entire extension that resolves values on the fly to show you
what your values will look like after interpolation, AND to hightlight errors/cycles.

# NAMING
- Consider renaming the `outputs` folder to `workspace` to better reflect the fact that you will be working in there.
- This is also the place where you will be putting reference photos `outputs/references`