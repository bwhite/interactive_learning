from gevent import monkey
monkey.patch_all()
import bottle
import os
import random
import shutil
import argparse
import json
bottle.debug(True)
ARGS = None
import inspect
SCRIPT_ROOT = os.path.dirname(inspect.getfile(inspect.currentframe()))


@bottle.get('/images.js')
def image_list():
    images = ['/image/' + x for x in os.listdir(ARGS['image_dir'])]
    random.shuffle(images)
    return json.dumps(images)


@bottle.get('/')
def index():
    return bottle.static_file('index.html', root=SCRIPT_ROOT)


@bottle.get('/kill')
def kill():
    os.kill(os.getpid(), 9)


@bottle.get(r'/image/:fn#[a-zA-Z0-9\-_\.]+#')
def images(fn):
    return bottle.static_file(fn, root=ARGS['image_dir'])


@bottle.post('/result/')
def result():
    action = bottle.request.json['action']
    assert action in ('delete', 'positive', 'negative')
    if ARGS['%s_dir' % action] is not None:
        for url in bottle.request.json['urls']:
            name = os.path.basename(url)
            shutil.move(ARGS['image_dir'] + '/' + name,
                        ARGS['%s_dir' % action] + '/' + name)
    return {}


def main():
    parser = argparse.ArgumentParser(description="Serve a folder of images")
    # Webpy port
    parser.add_argument('--port', type=str, help='Run on this port (default 8080)',
                        default='8080')
    # Image input directory
    parser.add_argument('image_dir')
    parser.add_argument('positive_dir')
    parser.add_argument('negative_dir')
    parser.add_argument('--delete_dir')
    run(**vars(parser.parse_args()))


def run(**kw):
    global ARGS
    ARGS = kw

    def mkdir(d):
        try:
            os.makedirs(d)
        except OSError:
            pass
    mkdir(ARGS['positive_dir'])
    mkdir(ARGS['negative_dir'])
    if ARGS['delete_dir'] is not None:
        mkdir(ARGS['delete_dir'])
    bottle.run(host='0.0.0.0', port=ARGS['port'], server='gevent')

if __name__ == '__main__':
    main()
