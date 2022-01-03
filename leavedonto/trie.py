# coding: utf-8

# inspired from https://gist.github.com/nickstanisha/733c134a0171a00f66d4
# and           https://github.com/eroux/tibetan-phonetics-py


class Node:
    def __init__(self):
        self.data = {'data': []}
        self.leaf = False
        self.children = dict()

    def add_child(self, key):
        if not isinstance(key, Node):
            self.children[key] = Node()
        else:
            self.children[key.leaf] = key

    def can_walk(self):
        return self.children != dict()

    def is_match(self):
        return self.leaf

    def __getitem__(self, key):
        return self.children[key]


class BasicTrie:
    def __init__(self):
        self.head = Node()

    def __getitem__(self, key):
        return self.head.children[key]

    def add(self, o_path, data=None):
        # adding the word
        current_node = self.head
        path_finished = True

        i = 0
        for i in range(len(o_path)):
            if o_path[i] in current_node.children:
                current_node = current_node.children[o_path[i]]
            else:
                path_finished = False
                break

        if not path_finished:
            while i < len(o_path):
                current_node.add_child(o_path[i])
                current_node = current_node.children[o_path[i]]
                i += 1

        current_node.leaf = True

        # adding data to the node
        if data:
            if not isinstance(data, list):
                raise ValueError('data is not a list.')

            if current_node.data:
                raise ValueError(f'data is not empty for {o_path}')

            current_node.data['data'] = data

    def walk(self, el, current_node=None):
        # logic of walking the trie adapted to be done outside the trie class (for Tokenize)
        if not current_node:
            current_node = self.head

        if el in current_node.children:
            next_node = current_node[el]
        else:
            next_node = None

        return next_node

    def has_word(self, path):
        if not path:
            raise ValueError('"path" must be list of strings')

        # parse the path
        current_node = self.head
        exists = True
        for el in path:
            if el in current_node.children:
                current_node = current_node.children[el]
            else:
                exists = False
                break
        else:
            # reached a word like 't', not a full path in the ontology
            if exists and not current_node.leaf:
                exists = False

        if exists:
            return {"exists": exists, "data": current_node.data}
        else:
            return {"exists": exists, "data": current_node.data}

    def add_data(self, path, data):
        """Adds data to words.

        :param path: word to add
        :param data: dict of content to add
        :return: True if any content added, False otherwise
        """
        if not path:
            raise ValueError('"path" must be a list of strings')

        # parse word
        current_node = self.head
        for el in path:
            if el in current_node.children:
                current_node = current_node.children[el]
            else:
                return False

        # not a complete word
        if not current_node.leaf:
            return False

        # adding data
        current_node.data = data
        return True
