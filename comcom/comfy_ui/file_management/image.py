import os
import urllib
import hashlib
import yaml
import datetime

def get_sha1_hex_of_data(image_data):
    return hashlib.sha1(image_data).hexdigest()

def get_sha1_hex_of_file(file_path):
    with open(file_path, 'rb') as f:
        return get_sha1_hex_of_data(f.read())

def save_remote_image_locally(remote_url, local_path_without_ext, extension):
    request = urllib.request.Request(remote_url)
    image_data = urllib.request.urlopen(request).read()
    with open(local_path_without_ext + extension, 'wb') as f:
        f.write(image_data)
    image_sha1 = get_sha1_hex_of_data(image_data)
    # Save a metadata file next to the image file
    metadata = {
        'sha1': image_sha1,
        'remote_filename': remote_url,
        'saved_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(local_path_without_ext + '.cc_meta', 'w') as f:
        f.write(yaml.dump(metadata, default_flow_style=False))

def upload_image(local_path_without_ext, extension):
    # search for the metadata file
    metadata_path = local_path_without_ext + '.cc_meta'
    if os.path.exists(metadata_path):
        # if it exists, find the image file
        image_path = local_path_without_ext + extension
        if os.path.exists(image_path):
            # if it exsts, 
        # load the metadata file, and search for a "remote_filename" key
        with open(metadata_path, 'r') as f:
            metadata = yaml.safe_load(f)
        if 'remote_filename' in metadata:
            return metadata['remote_filename']
        
    with open(metadata_path, 'r') as f:
        metadata = yaml.safe_load(f)
    # upload the image to the server