from .trie import Node, BasicTrie


def trie_to_dicts(trie):
    pass


class DictsToTrie:
    def __init__(self, dicts):
        self.dicts = dicts
        self.words = None
        self.result_path = None
        self.found = None

    def list_words(self, ont=None, words=None):
        # initiate vars
        if not ont and not words:
            ont = self.dicts['ont']
            words = self.words = []

        self.__recursive_list(ont)
        words = sorted(list(set(words)))
        return words

    def __recursive_list(self, onto):
        for key, value in onto.items():
            if isinstance(value, dict):
                self.__recursive_list(value)
            else:
                self.words.extend([v[0] for v in value])

    def find_word(self, word):
        # initiate vars
        self.result_path = []
        self.found = []

        self.__recursive_find(self.dicts['ont'], word)
        return self.found

    def __recursive_find(self, onto, word):
        for key, value in onto.items():
            self.result_path.append(key)
            if isinstance(value, dict):
                self.__recursive_find(value, word)
            else:
                has_found = False
                for entry in value:
                    if entry[0] == word:
                        occ = {'path': self.result_path, 'entry': entry}
                        self.found.append(occ)
                        has_found = True
                if has_found:
                    self.result_path = []
                else:
                    self.result_path = self.result_path[:-1]


def dicts_to_trie(dicts):

    print()

