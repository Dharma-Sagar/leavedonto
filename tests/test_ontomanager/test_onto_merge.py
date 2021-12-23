# coding: utf8
from pathlib import Path

from leavedonto import OntoManager


def test_merge():
    ref = Path().cwd() / 'resources' / 'test_onto.yaml'
    to_add = Path().cwd() / 'resources' / 'test_onto2.yaml'

    om = OntoManager(ref)
    ref_words = om.ref.list_words()
    assert 'lemma5' not in ref_words

    om.merge_to_onto(to_add)
    ref_words2 = om.ref.list_words()
    assert 'lemma5' in ref_words2
