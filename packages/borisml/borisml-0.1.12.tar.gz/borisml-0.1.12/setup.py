import setuptools
import sys


if __name__ == '__main__':

    with open('README.md') as f:
        long_description = f.read()

    LOCAL_INSTALL = False
    if '--local' in sys.argv:
        sys.argv.remove('--local')
        LOCAL_INSTALL = True

    name = 'borisml'

    version = '0.1.12'

    author = 'Philipp Wirth & Igor Susmelj'
    author_email = 'philipp@whattolabel.com'
    description = "A deep learning package for self-supervised learning"

    entry_points = {
        "console_scripts": [
            "boris-train = boris.cli.train_cli:entry",
            "boris-embed = boris.cli.embed_cli:entry",
            "boris-magic = boris.cli.boris_cli:entry",
            "boris-upload = boris.cli.upload_cli:entry",
            "boris-download = boris.cli.download_cli:entry",
        ]
    }

    install_requires = [
        'tqdm',
        'torchvision',
        'hydra-core>=1.0.0',
        'numpy>=1.18.1',
        'requests>=2.23.0',
        'pytorch_lightning',
    ]

    if not LOCAL_INSTALL:
        exclude = ["*.sampling", "*.sampling.*", "sampling.*", "sampling"]
    else:
        exclude = []

    packages = setuptools.find_packages(
        exclude=exclude
    )

    project_urls = {
        'Documentation': 'https://www.notion.so/whattolabel/WhatToLabel-Documentation-28e645f5564a453e807d0a384a4e6ea7',
        'WhatToLabel': 'https://www.whattolabel.com'
    }

    if LOCAL_INSTALL:
        packages.append(
            'boris.sampling'
        )

    classifiers = [
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License"
    ]

    setuptools.setup(
        name=name,
        version=version,
        author=author,
        author_email=author_email,
        description=description,
        entry_points=entry_points,
        license='MIT',
        long_description=long_description,
        long_description_content_type='text/markdown',
        install_requires=install_requires,
        packages=packages,
        classifiers=classifiers,
        include_package_data=True,
        project_urls=project_urls,
    )

