#!/usr/bin/env python
"""Tests for `pyyawl` package."""

import pytest
from pyyawl import pyyawl
from pathlib import Path

PATH = Path(__file__).parent


def test_simpleworkflow():
    definition = PATH / 'test_ops.yaml'
    pyyawl.execute(definition, True)


def test_simpleworkflow_from_str():
    content = """
name: test
description: test description

steps:
  - name: echo
    arguments:
      value: yawl
  - name: echo
    arguments:
      value: world
  - name: papermill
    arguments:
      input_path: tests/notebooks/sum_test.ipynb
      output_path: tests/notebooks/sum_test_out.ipynb
      parameters:
        a: 8
        b: 4
        image_path: ./tests/notebooks/imgs/image_1.jpg
    """
    pyyawl.execute(content, True)


def test_simpleworkflow_mkdir():
    content = """
name: test
description: test description

steps:
  - name: mkdir
    arguments:
      path: test_dir
  - name: rmdir
    arguments:
      path: test_dir
  - name: ls
    arguments:
      path: .
    """
    results = pyyawl.execute(content, True)
    assert 'test_dir' not in [p.as_posix() for p in results['ls']]


@pytest.mark.xfail(raises=AssertionError)
def test_simpleworkflow_missing_ops():
    content = """
name: test
description: test description

steps:
  - name: echo2
    arguments:
      value: yawl
  - name: echo
    arguments:
      value: world
  - name: papermill
    arguments:
      input_path: tests/notebooks/sum_test.ipynb
      output_path: tests/notebooks/sum_test_out.ipynb
      parameters:
        a: 8
        b: 4
        image_path: ./tests/notebooks/imgs/image_1.jpg
    """
    pyyawl.execute(content, True)


def test_show_registry():
    assert len(pyyawl.show_registry()) > 0


def test_python_operator():
    content = """
name: test
description: test description

steps:
  - name: python
    arguments:
      value: tests/scripts/script1.py
    """
    pyyawl.execute(content, True)
