# import os
# import urllib
# import hashlib
# import yaml
# import datetime

# from comcom.comfy_ui.server.server import ComfyServer

# def get_sha1_hex_of_data(image_data):
#     return hashlib.sha1(image_data).hexdigest()

# def create_metadata_file(local_filepath, full_remote_filepath, remote_filename, extension, image_data=None, sha1=None):
#     # Calculate the sha-1, if necessary
#     if sha1 is None:
#         if not image_data:
#             image_data = get_sha1_hex_of_data(open(local_filepath + '.' + extension.lstrip('.'), 'r').read())
#         sha1 = get_sha1_hex_of_data(image_data)
    
#     metadata = {
#         'sha1': sha1,
#         'full_remote_filepath': full_remote_filepath,
#         'remote_filename': remote_filename,
#         'upload_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     }

#     with open(local_filepath + '.cc_meta', 'w') as f:
#         f.write(yaml.dump(metadata, default_flow_style=False))

# def save_remote_image_locally(remote_url, remote_filename, local_path_without_ext, extension):
#     request = urllib.request.Request(remote_url)
#     image_data = urllib.request.urlopen(request).read()

#     # If the file already exists, read the remote url and see if its the same. if it is, return early.
#     existing_metadata_filepath = local_path_without_ext + '.cc_meta'
#     if os.path.exists(existing_metadata_filepath):
#         metadata = yaml.load(open(existing_metadata_filepath, 'r').read(), Loader=yaml.FullLoader)
#         metadata_remote_filename = metadata.get('remote_filename', None)
#         if remote_filename == metadata_remote_filename:
#             return
        
#     with open(local_path_without_ext + '.' + extension.lstrip('.'), 'wb') as f:
#         f.write(image_data)
#     create_metadata_file(local_path_without_ext, remote_url, remote_filename, extension, image_data)

# def get_remote_filename(local_path_without_ext, extension, comfy_server: ComfyServer):
#     image_path = local_path_without_ext + '.' + extension.lstrip('.')
#     if not os.path.exists(image_path):
#         raise Exception("Image {} does not exist".format(image_path))

#     metadata_path = local_path_without_ext + '.cc_meta'
#     image_data = open(image_path, 'rb').read()
#     real_image_hash = get_sha1_hex_of_data(image_data)

#     if os.path.exists(metadata_path):
#         with open(metadata_path, 'r') as f:
#             metadata = yaml.safe_load(f)
#             if 'remote_filename' in metadata.keys():
#                 if 'sha1' in metadata.keys():
#                     if metadata.get('sha1') == real_image_hash:
#                         return metadata['remote_filename']
                    
#     # if we get to this point it means the image is either modified or doesnt exist, which means it has to be (re)uploaded.
#     remote_location = comfy_server.upload_image(image_data)
#     create_metadata_file(image_path, remote_location, extension, image_data, real_image_hash)