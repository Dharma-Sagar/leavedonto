# coding: utf8
import pytest
from pathlib import Path

from leavedonto import LeavedOnto


def test_path():
    onto_path = Path().cwd() / 'test_get_entries' / 'test_onto.yaml'
    lo = LeavedOnto(onto_path)

    path, found = [], []
    lo.get_entries(lo.ont['ont'], path, 'lemma', found)
    expected = ['category1', 'subcat2', 'subsubcat1']
    assert found[0]['path'] == expected

    path, found = [], []
    lo.get_entries(lo.ont['ont'], path, 'lemma2', found)
    expected = ['category1', 'subcat1']
    assert found[0]['path'] == expected

