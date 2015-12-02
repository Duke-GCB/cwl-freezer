import workflow_io as wf
import docker_io as dk

from workflow_io import parse_workflow, extract_paths_image_ids, extract_image_ids, print_names, replace_values
from docker_io import get_client, write_image, get_image_ids

# returns list of images (names+ids) and the frozen document
def freeze_workflow(workflow_doc, export_dir):
    # Parse the document
    workflow = wf.parse_workflow(workflow_doc)
    image_paths = wf.extract_paths_image_ids(workflow)
    # find the image names in the document
    paths_image_ids = wf.extract_paths_image_ids(workflow)
    image_ids = wf.extract_image_ids(paths_image_ids)
    # Now consult docker API for the image IDs
    client = dk.get_client()
    
    frozen_images = {}
    for image_id in image_ids:
        resolved_image_ids = dk.get_image_ids(client, image_id)
        if len(resolved_image_ids) != 1:
            raise 'Too many images found, please be more specific'
        frozen_images[image_id] = resolved_image_ids[0]
    # write docker images

    # Now replace workflow with frozen images
    for d in paths_image_ids:
        path = d[wf.PATH]
        orig_image_id = d[wf.IMAGE_ID]
        new_image_id = frozen_images[orig_image_id]
        wf.replace_values(workflow, path, new_image_id)
    
    return frozen_images, workflow
