import re

def parse_url(url):
    manifest_url_prefix = 'http://manifests.ydc2.yale.edu'
    image_url_prefix = 'http://iiif-dev-10kr-1728262279.us-east-1.elb.amazonaws.com/iiif'
    pattern = r'^%s/(\w+)-C(\d+)-P(\d\d\w)-tif/full/full/0.native.jpg$' % image_url_prefix

    m = re.match(pattern, url)
    ident = m.group(1)
    chapter = _unpad(m.group(2))
    page = _unpad(m.group(3))

    padded_name = '%s-C%s-P%s' % (ident, _pad(chapter), _pad(page))

    info_url = re.sub(r'/full/full/.*$', '/info.json', url)
    canvas_id = '%s/%s/canvas/%s' % (manifest_url_prefix, ident, padded_name)
    canvas_label = 'Chapter %s, Page %s' % (chapter, page)
    image_id = '%s/%s/annotation/%s-tif' % (manifest_url_prefix, ident, padded_name)
    image_resource_id = '%s/%s-tif/full/full/0/native.jpg' % (image_url_prefix, padded_name)
    service_id = '%s/%s-tif/' % (image_url_prefix, padded_name)

    result = dict()
    result['info_url'] = info_url
    result['canvas_id'] = canvas_id
    result['canvas_label'] = canvas_label
    result['image_id'] = image_id
    result['image_resource_id'] = image_resource_id
    result['service_id'] = service_id
    return result

def _pad(s):
  if len(s) == 1:
      return '00' + s
  if len(s) == 2:
      return '0' + s
  return s

def _unpad(s):
    unpadded = re.sub(r'^0*([^0]*)', r'\1', s);
    if re.match('\d', unpadded) == None:
        unpadded = '0%s' % unpadded
    return unpadded

