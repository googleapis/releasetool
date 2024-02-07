# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

name = 'gcp-releasetool'
description = ''
version = "2.0.0rc1"
release_status = 'Development Status :: 3 - Alpha'
dependencies = [
    "requests>=2.31.0",
    "attrs>=20.1.0",
    "click>=8.0.4, <8.1.0",
    "cryptography>=42",
    "google-auth>=2.22.0",
    "jinja2>=3.1.3",
    "keyring>=21.8.0",
    "packaging>=20.0",
    "protobuf>=4.21.6",
    "pyjwt>=2.0.0",
    "pyperclip>=1.8.0",
    "python-dateutil>=2.8.1",
]

packages = setuptools.find_packages()
scripts = [
    'releasetool=releasetool.__main__:main'
]


setuptools.setup(
    name=name,
    version=version,
    description=description,
    author='Google LLC',
    author_email='theaflowers@google.com',
    license='Apache 2.0',
    url='',
    classifiers=[
        release_status,
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Topic :: Internet',
    ],
    platforms='Posix; MacOS X; Windows',
    packages=packages,
    python_requires='>=3.8',
    install_requires=dependencies,
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': scripts,
    },
    package_data={
        'autorelease': ['*.j2']
    },
)
