import cwltool
import dpath.util
import urlparse
from schema_salad import schema
from cwltool import process, update

PATH='path'
IMAGE_ID='dockerImageId'
                
# Parse is extracted from cwltool code
def parse_workflow(cwlpath):
    (document_loader, avsc_names, schema_metadata) = process.get_schema()
    fileuri = 'file://' + cwlpath
    workflowobj = document_loader.fetch(fileuri)
    # If strict is true, names are required everywhere (among other requirements)
    strict = False
    # This updates from draft2 to draft3
    workflowobj = update.update(workflowobj, document_loader, fileuri)
    document_loader.idx.clear()
    processobj, metadata = schema.load_and_validate(document_loader, avsc_names, workflowobj, strict)
    return processobj

def find_key(d, key, path=[]):
    if isinstance(d, list):
        for i, v in enumerate(d):
            for f in find_key(v, key, path + [str(i)]):
                yield f
    elif isinstance(d, dict):
        if key in d:
            pathstring = '/'.join(path + [key])
            yield pathstring
        for k, v in d.items():
            for f in find_key(v, key, path + [k]):
                yield f
def extract_paths_image_ids(workflow):
    results = []
    for x in find_key(workflow, IMAGE_ID):
        image_id = dpath.util.get(workflow, x)
        results.append({PATH: x, IMAGE_ID: image_id})
    return results

def extract_image_ids(workflow):
    all_ids = map(lambda x: x[IMAGE_ID], extract_paths_image_ids(workflow))
    return list(set(all_ids))

def print_names(image_names):
    for name in image_names:
        print name

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
    
