from os import path

import setuptools

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='designer',
    version='0.0.2',
    python_requires='>=3.6',
    author='krishols, acbart',
    author_email='kris@udel.edu',
    description='Student-friendly and evidence-based visual graphics library.',
    license='MIT',
    long_description=long_description,
    url='https://github.com/krishols/designer',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Topic :: Education',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ])