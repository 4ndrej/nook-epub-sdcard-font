#!/usr/bin/env python

import fnmatch
import os
import shutil
import sys
import tempfile
import zipfile
from zipfile import ZipFile

extra_css = '''@font-face {
font-family: "Arial", serif;
font-weight: normal;
font-style: normal;
src: url("res:///system/media/sdcard/fonts/arial.ttf");
}
@font-face {
font-family: "Arial", serif;
font-weight: bold;
font-style: normal;
src: url("res:///system/media/sdcard/fonts/arialbd.ttf");
}
@font-face {
font-family: "Arial", serif;
font-weight: normal;
font-style: italic;
src: url("res:///system/media/sdcard/fonts/ariali.ttf");
}
@font-face {
font-family: "Arial", serif;
font-weight: bold;
font-style: italic;
src: url("res:///system/media/sdcard/fonts/arialbi.ttf");
}
body, p, div, h1, h2, h3 { font-family: "Arial", serif;}'''
css_link = '<link rel="stylesheet" type="text/css" href="extra_nook.css"/>'


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Specify a filename')
        print('eg. convert.py mybook.epub')
        sys.exit(1)

    epub = sys.argv[1]

    if not zipfile.is_zipfile(epub):
        print('EPUB file given is not a valid zip file.')
        sys.exit(1)

    dirpath = tempfile.mkdtemp()

    with ZipFile(open(epub, 'r')) as zf:
        zf.extractall(path=dirpath+'/extracted')

    shutil.copytree(dirpath+'/extracted', dirpath+'/output')

    opsPrefix = 'OPS/'
    if not os.path.isdir(dirpath+'/output/' + opsPrefix):
        opsPrefix = ''

    with open(dirpath+'/output/' + opsPrefix + 'extra_nook.css', 'w') as f:
        f.write(extra_css)

    for fname in os.listdir(dirpath+'/extracted/' + opsPrefix):
        if not fnmatch.fnmatch(fname, '*.html'):
            continue

        out = open(dirpath+'/output/' + opsPrefix + '%s' % fname, 'w')
        with open(dirpath+'/extracted/' + opsPrefix + '%s' % fname, 'r') as f:
            for line in f:
                if '</head>' in line:
                    out.write(css_link)
                out.write(line)

        out.close()

    output_fname = '%s_fonted.epub' % os.path.splitext(epub)[0]
    shutil.make_archive(output_fname, format='zip', root_dir=dirpath+'/output')
    shutil.move('%s.zip' % output_fname, output_fname)

    shutil.rmtree(dirpath)
