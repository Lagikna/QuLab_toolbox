import platform
from codecs import open
from os import getcwd, getenv, listdir, path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This reads the __version__ variable from lab/_version.py
exec(open('qulab_toolbox/_version.py').read())

requirements = [
    'numpy>=1.13.3',
    'scipy>=1.2.0',
    'matplotlib>=2.1.0',
    # 'QuLab>=0.4.0',
]

if platform.system() == 'Windows':
    requirements.extend([
        'pywin32>=220.1'
    ])

setup(
    name="qulab_toolbox",
    version=__version__,
    author="Lagikna",
    author_email="lazy_216@outlook.com",
    url="https://github.com/Lagikna/QuLab_toolbox",
    license = "MIT",
    keywords="experiment laboratory",
    description="contral instruments and manage data: toolbox",
    long_description=long_description,
    packages = find_packages(),
    include_package_data = True,
    #data_files=[('QuLab/Drivers', driverFiles)],
    install_requires=requirements,
    extras_require={
        # 'test': ['pytest'],
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/Lagikna/QuLab_toolbox/issues',
        'Source': 'https://github.com/Lagikna/QuLab_toolbox',
    },
)
