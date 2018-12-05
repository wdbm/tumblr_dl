#!/usr/bin/env python2

"""
################################################################################
#                                                                              #
# tumblr_dl                                                                    #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program downloads the media of a Tumblr subdomain.                      #
#                                                                              #
# copyright (C) 2018 Will Breaden Madden, wbm@protonmail.ch                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

usage:
    program [options]

options:
    -h, --help                 display help message
    --version                  display version and exit
    --subdomain=STRING         subdomain                                   [default: actionfigurebody]
    --chunksize=STRING         chunk size                                  [default: 50]
    --directory_output=STRING  output directory                            [default: downloads]
    --print_media_links        just print media links without downloading
"""

import docopt
import os
import re
from six.moves.urllib.parse import urlparse
import sys
if sys.version_info[0] >= 3:
    print("Python 2 required")
    sys.exit(1)
try:
    from urllib.request import urlopen
except:
    from urllib2 import urlopen

name        = "tumblr_dl"
__version__ = "2018-12-05T1548Z"

def main():
    options           = docopt.docopt(__doc__, version = __version__)
    subdomain         =     options["--subdomain"]
    chunksize         = int(options["--chunksize"])
    directory_output  =     options["--directory_output"]
    print_media_links =     options["--print_media_links"]
    print("\n" + name + "\n")
    print("download subdomain {subdomain}\n".format(subdomain = subdomain))
    site_URL_template = "http://#subdomain#.tumblr.com/api/read?type=photo&num=#chunksize#&start=#start#".replace("#subdomain#", subdomain)
    start = 0
    while True:
        media_URLs = get_media_URLs(
            site_URL_template = site_URL_template,
            start             = start,
            chunksize         = chunksize
        )
        start = start + chunksize
        if media_URLs:
            for media_URL in media_URLs:
                if not print_media_links:
                    download_media_object(
                        media_URL        = media_URL,
                        subdomain        = subdomain,
                        directory_output = directory_output
                    )
                else:
                    print(media_URL)
        else:
            print("complete -- please assume the position")
            exit()

def get_media_URLs(
    site_URL_template = None,
    start             = None,
    chunksize         = None
    ):
    """
    Get media URLs returned by the Tumblr API.
    """
    site_URL_template = site_URL_template.replace("#chunksize#", str(chunksize)).replace("#start#", str(start))
    _site             = urlopen(site_URL_template)
    data              = _site.read()
    _site.close()
    media_URLs        = re.findall(ur"<photo-url max-width=\"1280\">(.+?)</photo-url>", data)
    return media_URLs

def download_media_object(
    media_URL        = None,
    subdomain        = None,
    directory_output = None
    ):
    """
    Download a media object to the specified subdomain directory of the output directory.
    """
    filename  = subdomain + "_" + media_URL.split("/")[-1]
    directory = directory_output + "/" + subdomain
    if not os.path.exists(directory):
         os.makedirs(directory)
    _site = urlopen(media_URL)
    # Skip the file if it is already downloaded.
    if os.path.isfile(directory + "/" + filename):
        print("already downloaded: {filename}".format(filename = filename))
        return None
    with open(directory + "/" + filename, "wb") as _file:
        metadata = _site.info()
        filesize = int(metadata.getheaders("Content-Length")[0])
        print("downloading: {filename} ({filesize} bytes)".format(filename = filename, filesize = filesize))
        filesize_downloaded = 0
        block_size          = 8192
        while True:
            _buffer = _site.read(block_size)
            if not _buffer:
                break
            _file.write(_buffer)
            filesize_downloaded += len(_buffer)
            status = r"%10d  [%3.2f % %]" % (filesize_downloaded, float(100 * filesize_downloaded) / float(filesize))
            status = status + chr(8) * (len(status) + 1)
            print status,

if __name__ == "__main__":
    main()
