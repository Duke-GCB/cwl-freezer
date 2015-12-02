from workflow_io import parse_workflow, extract_paths_image_ids, extract_image_ids, print_names


# returns list of images (names+ids) and the frozen document
def freeze_workflow(workflow_doc, export_dir):
    # Parse the document
    workflow = parse_workflow(workflow_doc)
    image_paths = extract_paths_image_ids(workflow)
    print_names(image_paths)
    # find the image names in the document
    image_ids = extract_image_ids(workflow)
    # Now consult docker API for the image IDs
    print_names(image_ids)
    # replace with image ids
    

