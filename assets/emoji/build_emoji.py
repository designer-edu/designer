# Download the latest build of twemoji: https://github.com/twitter/twemoji/releases
# Run this script to generate the archive
# python build_emoji.py path/to/twemoji.zip

from zipfile import ZipFile, ZIP_DEFLATED
import pathlib
import sys
import re
import xml.etree.ElementTree as ET

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
    for path in tqdm(twemoji.namelist()):
        match = re.match(r"twemoji.*/assets/svg/(.*)\.svg", path)
        if match:
            with twemoji.open(path) as svg_file:
                unicode_name = match.group(1)
                svg_data = svg_file.read()
                ET.register_namespace('', ns)
                svg_tree = ET.fromstring(svg_data)
                svg_important_part = b"".join(ET.tostring(child) for child in svg_tree)
                # Dirty hack to remove the namespaces
                svg_important_part = svg_important_part.replace(f' xmlns="{ns}"'.encode(), b"")
                dumped_zip.writestr(unicode_name, svg_important_part)

