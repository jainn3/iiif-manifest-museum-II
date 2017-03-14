#!/usr/bin/env python

import json
import os
import re
import sys

from file_name_parser import FileNameParser
from image_parser import ImageParser

import downloadData


class App(object):
    def __init__(self, file_names_file, config_file):
        #self.root_dir = '''os.environ['GEN_MANIFEST_HOME']'''
        self.root_dir = '/home/nimesh/gen-manifest'
        self.file_names_file = file_names_file
        self.config = self.get_config(config_file)
        self.fileNameParser = FileNameParser(self.config)
        self.imageParser = ImageParser()
        self.blackList = set()
        self.loadFile("blackList.txt")

        self.fob = open('blackList.txt', 'a')

    def get_config(self, config_file):
        # Read default config
        with open(os.path.join(self.root_dir, 'config.json')) as f:
            config = json.loads(f.read())

        if not config_file:
            return config

        # Read user config
        with open(config_file) as f:
            config.update(json.loads(f.read()))

        return config

    def run(self):
        files = []
        with open(self.file_names_file) as f:
            for line in f:
                file_name = line.strip()
                files.append(file_name)
        manifest = self.build_manifest(files)
        print json.dumps(manifest, indent=2)

    def build_manifest(self, files):
        config = self.config
        manifestServerRootUrl = config['manifestServerRootUrl']
        projectPath = config['projectPath']

        manifestId = '%s/manifest/%s' % (manifestServerRootUrl, projectPath)
        manifestLabel = config['manifestLabel']
        sequenceId = '%s/sequence/%s/0' % (manifestServerRootUrl, projectPath)

        m = {
            '@context': 'http://www.shared-canvas.org/ns/context.json',
            '@type': 'sc:Manifest',
            '@id': manifestId,
            'label': manifestLabel,
            'sequences': [
                {
                    '@type': "sc:Sequence",
                    '@id': sequenceId,
                    'label': 'Sequence 1',
                    'viewingDirection': "left-to-right",
                    'canvases': []
                }
            ],
            'structures': []
        };

        if config.get('metadata'):
            m['metadata'] = config['metadata']

        old_chapter = -1

        res1 = downloadData.sparqlQuery()
        print len(res1)

        for base,res in res1.iteritems():
            print base
            _filename = base + ".txt"
            self.imageParser.loadFile(_filename)
            self.imageParser.openFile(_filename)
            #for mus in res:
            for artist in res:
                    try:
                        f_name = artist["image"]["value"]
                    except:
                        f_name = "unknown"
                        pass
                    try:
                        caption = artist["caption"]["value"]
                    except:
                        caption = "unknown"
                        pass
                    file_info = self.fileNameParser.parse(f_name,base)
                    if not file_info:
                        continue
                    if file_info['file_name'] in self.blackList:
                        continue
                    canvas = self.build_canvas(file_info, caption)
                    if canvas:
                        m['sequences'][0]['canvases'].append(canvas)
                    else:
                        museum = 'unknown'
                        self.fob.write(base + '\t' + file_info['file_name'] + '\n')
            self.imageParser.close()
        return m

    def build_canvas(self, info, caption):
        license = 'http://opendatacommons.org/licenses/by/1.0/'
        try:
            image_info = self.imageParser.size(info['file_name'])
            width = int(image_info["width"])
            height = int(image_info["height"])
        except:
            width = -1
            height = -1
            return None


        c = {
            '@type': 'sc:Canvas',
            '@id': info['canvas_id'],
            'label': info['canvas_label'],
            'width': width,
            'height': height,
            'license': license,
            'metadata': [
                {
                    'label': 'caption',
                    'value': caption
                }

            ],
            'images': [
                {
                    '@type': 'oa:Annotation',
                    '@id': info['image_id'],
                    'motivation': 'sc:painting',
                    'on': info['canvas_id'],
                    'resource': {
                        '@type': 'dctypes:Image',
                        '@id': info['image_resource_id'],
                        'format': 'image/jpeg',
                        'width': width,
                        'height': height,
                        'service': {
                            '@id': info['image_service_id'],
                            'dcterms:conformsTo': 'http://library.stanford.edu/iiif/image-api/1.1/conformance.html#level1'
                        }
                    }
                }
            ]
        }
        return c

    def create_range(self, file_info):
        config = self.config
        range_id = '%s/range/%s/ch%s' % (
        config['manifestServerRootUrl'], config['projectPath'], file_info['chapter_padded'])
        label = '%s %s' % (config['chapterLabel'], file_info['chapter_unpadded'])
        return {
            '@id': range_id,
            '@type': 'sc:Range',
            'label': label,
            'canvases': []
        }

    def loadFile(self, fileName):
        if not os.path.exists(fileName):
            return

        with open(fileName, "r") as ins:
            for line in ins:
                line = line.strip('\n')
                arr = line.split('\t')
                if not self.blackList:
                    self.blackList.add(arr[1])


if __name__ == '__main__':
    '''
    file_names_file = sys.argv[1]
    if len(sys.argv) == 3:
        config_file = sys.argv[2]
    else:
        config_file = None
    '''
    app = App('files.txt', 'config.json')
    app.run()

    app.imageParser.close()
