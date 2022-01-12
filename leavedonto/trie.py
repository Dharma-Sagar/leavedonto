# coding: utf-8

# inspired from https://gist.github.com/nickstanisha/733c134a0171a00f66d4
# and           https://github.com/eroux/tibetan-phonetics-py


class Node:
    def __init__(self):
        self.path = []
        self.data = []
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


class OntTrie:
    def __init__(self):
        self.legend = []
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
                raise ValueError('data should be a list.')

            current_node.data.append(data)
            current_node.path = o_path

    def find_entries(self, prefix=None, lemma=None):
        """
        Returns a list of tuple(path, entry) in the trie that start with prefix.
        In case prefix == None, all results are returned
        """
        results = []

        # 1. Determine search scope by finding end-of-prefix node
        if not prefix:
            top_node = self.head
            queue = [node for key, node in top_node.children.items()]
        else:
            top_node = self.head
            for p in prefix:
                if p in top_node.children:
                    top_node = top_node.children[p]
                else:
                    # Prefix not in tree, go no further
                    return results
            queue = [top_node]

        # 2. Get search results: trie walking + find matches
        while queue:
            current_node = queue.pop()
            if current_node.leaf:
                # find matches ###########################################
                if lemma:
                    matches = []
                    for entry in current_node.data:
                        if entry[0] == lemma:
                            matches.append(lemma)
                    if matches:
                        results.append((current_node.path, matches))
                else:
                    results.append((current_node.path, current_node.data))
                ##########################################################

            queue = [node for key, node in current_node.children.items()] + queue

        return results

    def has_category(self, path):
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
            return {"path": current_node.path, "data": current_node.data}
        else:
            return False

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

        current_node.data.append(data)
        return True
