#!/usr/bin/env python2

import fnmatch
import pprint
import os
import re
import time
import urllib
from urllib2 import urlopen, URLError, HTTPError

class ImageScraper:
    base_dir = "BASE_DIR"
    sub_dir = "post"
    output_dir = "out"
    delay = 100

    def __init__(self):
        images = self.retrieve_image_urls()
        self.retrieve_images(images)

    def retrieve_image_urls(self):
        images = []
        for root, dirnames, filenames in os.walk(os.path.join(self.base_dir, self.sub_dir)):
            for filename in fnmatch.filter(filenames, '*.html'):
                lines = open(os.path.join(root, filename), "r")
                for line in lines:
                    og_image_match = re.search(r'(<meta[^>]+property="og:image"[^>]*>)', line)

                    if not og_image_match:
                        continue

                    image_url_match = re.search(r'\scontent="([^"]+)"', og_image_match.group(1))

                    if not image_url_match:
                        continue

                    images.append(image_url_match.group(1))
        return images

    def retrieve_images(self, images):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        for image in images:
            output_image_filename = self.get_image_filename_from_url(image)
            if not output_image_filename:
                continue

            try:
                url_handle = urlopen(image)

                print "Downloading " + image

                with open(os.path.join(self.output_dir, output_image_filename), "wb") as local_file:
                    local_file.write(url_handle.read())

                time.sleep(0.1)
            except HTTPError, e:
                print "HTTP Error:", e.code, image
            except URLError, e:
                print "URL Error:", e.reason, image



    def get_image_filename_from_url(self, image):
        url_parts = image.split('://', 1)
        if len(url_parts) < 2:
            return ''
        domain_and_uri = url_parts[1]
        output_image_filename = urllib.quote(domain_and_uri, '')
        return output_image_filename



ImageScraper()
