from setuptools import setup, find_packages
from os import path
from typing import List


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()


def read_requirements(requirements_file: str) -> List[str]:
  requirements = []
  with open(requirements_file, 'rt') as infile:
    for line in infile:
      line = line.strip()
      if line.startswith('#') or not line:
        continue
      requirements.append(line)
  return requirements


setup(
  name='pvdtalks',
  version='0.0.1',
  description='An uploader and processor for PVD Talks information',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/thepolicylab/pvdtalks-randomizer',
  author='The Policy Lab',
  author_email='thepolicylab@brown.edu',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],

  packages=find_packages(),

  python_requires='>=3.6, <4',

  install_requires=read_requirements('requirements.txt'),

  # entry_points={  # Optional
  #   'console_scripts': [
  #     'tplcovid=tplcovid.cli:cli',
  #   ],
  # },

  project_urls={
    'Bug Reports': 'https://github.com/thepolicylab/pvdtalks-randomizer/issues',
    'Source': 'https://github.com/thepolicylab/pvdtalks-randomizer'
  },
)
