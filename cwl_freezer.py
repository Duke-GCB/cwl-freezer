import workflow_io as wf
import docker_io as dk

def load_workflow(workflow_doc):
    return wf.parse_workflow(workflow_doc)

def save_workflow(workflow, workflow_doc):
    return wf.save_workflow(workflow, workflow_doc)

# returns list of images (names+ids) and the frozen document
def freeze_workflow(workflow): # does not parse
    image_paths = wf.extract_paths_image_ids(workflow)

    # Extract the docker images named in the workflow
    paths_image_ids = wf.extract_paths_image_ids(workflow)
    image_ids = wf.extract_image_ids(paths_image_ids)

    # Consult docker API to resolve all image names/ids to ids
    client = dk.get_client()
    frozen_image_metadata = {}
    for image_id in image_ids:
        resolved_image_metadata = dk.get_image_metadata(client, image_id)
        if len(resolved_image_metadata) != 1:
            raise 'Too many images found for {}, please be more specific'.format(image_id)
        frozen_image_metadata[image_id] = resolved_image_metadata[0]

    # Replace images named in workflow with resolved (frozen) ids
    for d in paths_image_ids:
        path = d[wf.PATH]
        orig_image_id = d[wf.IMAGE_ID]
        new_image_id = frozen_image_metadata[orig_image_id]['Id']
        wf.replace_values(workflow, path, new_image_id)
    
    return frozen_image_metadata, workflow

def export_images(frozen_image_metadata, export_dir):
    # frozen_images is a dict of {'orig': 'resolved'}
    client = dk.get_client()
    for name, metadata in frozen_image_metadata.items():
        dk.write_image(client, metadata, export_dir)
