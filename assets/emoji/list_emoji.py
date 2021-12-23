# Download the latest build of twemoji: https://github.com/twitter/twemoji/releases
# Run this script to generate the archive
# python build_emoji.py path/to/twemoji.zip

from zipfile import ZipFile, ZIP_DEFLATED
import pathlib
import sys
import re
import unicodedata

try:
    from tqdm import tqdm
except ImportError:
    tqmd = list

if len(sys.argv) <= 1:
    raise Exception("Need to pass in path to twemoji archive")

# Input
twemoji = ZipFile(sys.argv[1])
base = pathlib.Path(sys.argv[1]).name

ns = "http://www.w3.org/2000/svg"

# Output
db = {}

with ZipFile('emojis.zip', 'w', compression=ZIP_DEFLATED) as dumped_zip:
    for path in twemoji.namelist():
        match = re.match(r"twemoji.*/assets/svg/(.*)\.svg", path)
        if match:
            with twemoji.open(path) as svg_file:
                unicode_name = match.group(1)
                hexed = int(unicode_name, 16)
                print(unicodedata.name(chr(hexed)))

