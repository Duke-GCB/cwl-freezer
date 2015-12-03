import cwltool
import dpath.util
import urlparse
from schema_salad import schema
from cwltool import process, update
import yaml

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

def save_workflow(workflow, workflow_file):
    with open(workflow_file, 'w') as f:
        yaml.dump(workflow, stream=f)

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

def extract_image_ids(paths_image_ids):
    all_ids = map(lambda x: x[IMAGE_ID], paths_image_ids)
    return list(set(all_ids))

def replace_values(workflow, key_path, value):
    return dpath.util.set(workflow, key_path, value)

def print_names(image_names):
    for name in image_names:
        print name
