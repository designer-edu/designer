from os import path

import setuptools

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]


setuptools.setup(
    name='designer',
    version='0.3.5',
    python_requires='>=3.6',
    author='krishols, acbart',
    packages=['designer', 'designer.objects', 'designer.utilities', 'designer.core',
              'designer.tk'],
    package_data={
        'designer': ['data/colors.json', 'data/default_key_mappings.txt',
                     'data/unicode_names.json', 'data/emojis.zip']
    },
    author_email='kris@udel.edu',
    description='Student-friendly and evidence-based visual graphics library.',
    install_requires=REQUIREMENTS,
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/designer-edu/designer',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Topic :: Education',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ])