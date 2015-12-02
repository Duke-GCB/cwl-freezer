from docker import Client
from docker.utils import kwargs_from_env
import os
import errno
import json

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def get_image_metadata(docker_client, image_name):
    return docker_client.images(name=image_name)

def get_image_ids(docker_client, image_name):
    metadata = get_image_metadata(docker_client, image_name)
    return map(lambda x: x['Id'], metadata)

def write_image(docker_client, image_metadata, basedir):
    # basedir/<imageId>/image.tar
    image_id = image_metadata['Id']
    outdir = os.path.join(basedir, image_id)
    mkdir_p(outdir)
    out_tarfile = os.path.join(outdir,'image.tar')
    out_metadata = os.path.join(outdir, 'image.json')
    with open(out_metadata, 'w') as image_json:
        print "Writing image metadata to {}".format(out_metadata)
        json.dump(image_metadata, image_json, indent=2)
    with open(out_tarfile, 'w') as image_tar:
        print "Writing image tar to {}".format(out_tarfile)
        image = docker_client.get_image(image_id)
        image_tar.write(image.data)

def get_client():
    client = Client(version='auto', **kwargs_from_env(assert_hostname=False))
    return client
