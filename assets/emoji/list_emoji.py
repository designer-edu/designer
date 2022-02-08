"""
Use this script to build up the JSON mapping names to their code point

Potentially could decrease file by removing letters that aren't likely to be used... But you never know, maybe someone
wants to write their name using this? Perhaps the `text` object could support unicode if we are sneaky enough...
"""
import string
import json

emojis = {}

# Start with the official names
with open('UnicodeData.txt') as unicode_file:
    for line in unicode_file:
        code, name, rest = line.split(";", maxsplit=2)
        emojis[name.lower()] = code

# Add in some additional ones
emojis["kiss (dark skin tone person, medium-dark skin tone person)"] = "1f9d1-1f3ff-200d-2764-fe0f-200d-1f48b-200d-1f9d1-1f3fe"
emojis["car"] = "1F697"

# Provide all faces as just their names
for code, name in list(emojis.items()):
    if code.endswith(" face"):
        without_face = code[:-len(" face")]
        if without_face not in emojis:
            emojis[without_face] = name


# Normalize names
def normalize(text):
    """ Remove all punctuation for now """
    return ''.join('' if c in string.punctuation else c for c in text)


emojis = {normalize(key): value
          for key, value in emojis.items()}

# Dump file
with open('unicode_names.json', 'w') as output_file:
    json.dump(emojis, output_file, indent=2)
