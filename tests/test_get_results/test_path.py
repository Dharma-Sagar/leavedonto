# coding: utf8
from pathlib import Path

from leavedonto import LeavedOnto


def test_path():
    onto_path = Path().cwd() / 'resources' / 'test_onto.yaml'
    lo = LeavedOnto(onto_path)

    found = lo.find_word('lemma')
    expected = ['category1', 'subcat2', 'subsubcat1']
    assert found[0]['path'] == expected

    found = lo.find_word('lemma2')
    expected = ['category1', 'subcat1']
    assert found[0]['path'] == expected

