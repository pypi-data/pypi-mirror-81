# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to embed your image dataset with
    state-of-the-art technology.

"""

import boris
__requires__ = boris._cli_requires()
if not boris.is_lightning_available():
    msg = 'Using `boris-magic` requires the following '
    msg += 'pre-requisites to be installed first: '
    msg += f'{", ".join(__requires__)}.'
    raise RuntimeError(msg)

import hydra

from boris.cli.train_cli import _train_cli
from boris.cli.embed_cli import _embed_cli
from boris.cli.upload_cli import _upload_cli
from boris.cli._helpers import fix_from_folder


def _boris_cli(cfg, is_cli_call=True):
    """Train a self-supervised model and use it to embed your dataset

    Args:
        see train_cli.py, embed_cli.py or
        https://www.notion.so/whattolabel/WhatToLabel-Documentation-28e645f5564a453e807d0a384a4e6ea7

    """

    cfg['loader']['shuffle'] = True
    cfg['loader']['drop_last'] = True
    checkpoint = _train_cli(cfg, is_cli_call)

    cfg['loader']['shuffle'] = False
    cfg['loader']['drop_last'] = False
    cfg['checkpoint'] = checkpoint

    embeddings = _embed_cli(cfg, is_cli_call)
    cfg['embeddings'] = embeddings
    if cfg['token'] and cfg['dataset_id']:
        _upload_cli(cfg)   


@hydra.main(config_path="config", config_name="config")
def boris_cli(cfg):
    """Train a self-supervised model and use it to embed your dataset

    Args:
        see train_cli.py, embed_cli.py or
        https://www.notion.so/whattolabel/WhatToLabel-Documentation-28e645f5564a453e807d0a384a4e6ea7

    """
    fix_from_folder(cfg)
    return _boris_cli(cfg)


def entry():
    boris_cli()
