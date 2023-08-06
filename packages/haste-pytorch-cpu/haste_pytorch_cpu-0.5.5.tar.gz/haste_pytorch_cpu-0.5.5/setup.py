# Copyright 2020 LMNT, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


VERSION = '0.5.5'
DESCRIPTION = 'Haste: a fast, simple, and open RNN library. Version that install without cuda'
AUTHOR = 'LMNT, Inc.'
AUTHOR_EMAIL = 'haste@lmnt.com'
URL = 'https://haste.lmnt.com'
LICENSE = 'Apache 2.0'
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Libraries',
]

# Copyright 2020 LMNT, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import os
import sys

from glob import glob
from platform import platform
from torch.utils import cpp_extension
from setuptools import setup
from setuptools.dist import Distribution
from subprocess import DEVNULL, call


class BuildHaste(cpp_extension.BuildExtension):
    def run(self):
        os.system('make haste')
        super().run()


def cuda_toolkit_available():
    try:
        call(["nvcc"], stdout=DEVNULL, stderr=DEVNULL)
        return True
    except FileNotFoundError:
        return False


base_path = os.path.dirname(os.path.realpath(__file__))


with open(f'frameworks/pytorch/_version.py', 'wt') as f:
    f.write(f'__version__ = "{VERSION}"')

ext_modules = []
if cuda_toolkit_available():
    if 'Windows' in platform():
        CUDA_HOME = os.environ.get('CUDA_HOME', os.environ.get('CUDA_PATH'))
        extra_args = []
    else:
        CUDA_HOME = os.environ.get('CUDA_HOME', '/usr/local/cuda')
        extra_args = ['-Wno-sign-compare']
    extension = cpp_extension.CppExtension(
        'haste_pytorch_lib',
        sources=glob('frameworks/pytorch/*.cc'),
        extra_compile_args=extra_args,
        include_dirs=[os.path.join(base_path, 'lib'), os.path.join(CUDA_HOME, 'include')],
        libraries=['haste', 'cublas', 'cudart'],
        library_dirs=['.', os.path.join(CUDA_HOME, 'lib64'), os.path.join(CUDA_HOME, 'lib', 'x64')])
    ext_modules.append(extension)

setup(name='haste_pytorch_cpu',
      version=VERSION,
      description=DESCRIPTION,
      long_description=open('README.md', 'r').read(),
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      license=LICENSE,
      keywords='pytorch machine learning rnn lstm gru custom op',
      packages=['haste_pytorch'],
      package_dir={'haste_pytorch': 'frameworks/pytorch'},
      install_requires=[],
      ext_modules=ext_modules,
      cmdclass={'build_ext': BuildHaste},
      classifiers=CLASSIFIERS)
