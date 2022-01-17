from pathlib import Path
from itertools import zip_longest

import yaml

from .load_xlsx import LoadXlsx
from .triedicts import DictsToTrie
from .convert2xlsx import Convert2Xlsx
from .convert2yaml import Convert2Yaml
from .sort_bo_lists import SortBoLists
from .trie import OntTrie


class LeavedOnto:
    def __init__(self, ont, ont_path=None):
        self.ont_path = ont
        self.ont = None
        if isinstance(ont, str) or isinstance(ont, Path):
            self.ont_path = Path(ont)
            self._load()
        elif isinstance(ont, dict):
            dt = DictsToTrie(ont)
            self.ont = dt.trie
            self.ont_path = ont_path
        elif isinstance(ont, OntTrie):
            self.ont = ont
            self.ont_path = ont_path
        else:
            ValueError('either a dict or a filename or an OntTrie object')

        self._cleanup()

        self.convert2xlsx = Convert2Xlsx(self.ont_path, self.ont).convert2xlsx
        self.convert2yaml = Convert2Yaml(self.ont_path, self.ont).convert2yaml

    def find_word(self, word):
        return self.ont.find_entries(lemma=word)

    def get_field_value(self, entries, field):
        for entry in entries:
            for legend, value in zip_longest(self.ont.legend, entry):
                if legend == field:
                    return value
        return None

    def _load(self):
        if self.ont_path.suffix == '.xlsx':
            lx = LoadXlsx(self.ont_path)
            self.ont = lx.load_xlsx()
        elif self.ont_path.suffix == '.yaml':
            self._load_yaml()
        else:
            raise ValueError('only supports xlsx and yaml files.')

    def _load_yaml(self):
        ont_yaml = yaml.safe_load(self.ont_path.read_text())
        dt = DictsToTrie(ont_yaml)
        self.ont = dt.trie

    def _cleanup(self):
        queue = [self.ont.head]
        while queue:
            current_node = queue.pop()
            if current_node.leaf:
                # remove duplicates and sort in tibetan order
                no_dups = [list(L) for L in set(map(tuple, current_node.data))]
                sorted_ = SortBoLists().sort_list_of_lists(no_dups)
                current_node.data = sorted_

            queue = [node for key, node in current_node.children.items()] + queue
