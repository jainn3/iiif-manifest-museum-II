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
        self.root_dir = os.environ['GEN_MANIFEST_HOME']
        self.file_names_file = file_names_file
        self.config = self.get_config(config_file)
        self.fileNameParser = FileNameParser(self.config)
        self.imageParser = ImageParser()

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
                'viewingDirection': "Left-to-Right",
                'canvases': []
            }
            ],
            'structures': []
        };

        if config.get('metadata'):
            m['metadata'] = config['metadata']

        old_chapter = -1

        res = downloadData.sparqlQuery()
	listOfres = []
	for mus in res:
	    for artist in mus:
		listOfres.append(artist["image"]["value"] + '\t' + artist["caption"]["value"])

	'''

        for file_name in files:
            f_name,caption = file_name.split('\t',1)
            print f_name
	    print caption
	'''

                file_info = self.fileNameParser.parse(f_name)
	    #file_info = self.fileNameParser.parse(file_name)
                if not file_info:
                    continue
                canvas = self.build_canvas(file_info, caption)
                m['sequences'][0]['canvases'].append(canvas)
	'''
            if config.get('createChapters') == 'y':
                chapter = file_info['chapter_padded']
                if chapter != old_chapter:
                    current_range = self.create_range(file_info)
                    m['structures'].append(current_range)
                    old_chapter = chapter
                current_range['canvases'].append(file_info['canvas_id'])
	'''
            
        return m

    def build_canvas(self, info, caption):
       
        image_info = self.imageParser.size(info['file_name'])
        width = image_info[1][0]
	height = image_info[1][1]
	
        c = {
            '@type': 'sc:Canvas',
            '@id': info['canvas_id'],
            'label': info['canvas_label'],
            'width': width,
            'height': height,
	    'metadata':[
                {
                    'label' : 'caption',
                    'value' : caption
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
        range_id = '%s/range/%s/ch%s' % (config['manifestServerRootUrl'], config['projectPath'], file_info['chapter_padded'])
        label = '%s %s' % (config['chapterLabel'], file_info['chapter_unpadded'])
        return {
          '@id': range_id,
          '@type': 'sc:Range',
          'label': label,
          'canvases': []
        }


if __name__ == '__main__':
    file_names_file = sys.argv[1]
    if len(sys.argv) == 3:
        config_file = sys.argv[2]
    else:
        config_file = None

    app = App(file_names_file, config_file)
    app.run()
