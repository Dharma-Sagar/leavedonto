from .leavedonto import LeavedOnto


class OntoManager:
    def __init__(self, onto_ref):
        self.ref = LeavedOnto(onto_ref)

    def merge_to_onto(self, onto):
        to_merge = LeavedOnto(onto)
        if sorted(to_merge.ont.legend) != sorted(self.ref.ont.legend):
            raise SyntaxError('the two ontos need to have the same elements as legend.\nPlease retry after that.')

        legend = to_merge.ont['legend']
        to_organize, to_update = self._filter_entries(to_merge)
        for el in to_organize:
            path, entry = el['path'], el['entry']
            cur_node = self.ref.ont['ont']
            for p in path:
                if p in cur_node:
                    cur_node = cur_node[p]
                else:
                    cur_node[p] = {}
            print()
        to_organize = [self._entry_list2dict(to) for to in to_organize]
        to_update = [self._entry_list2dict(tu) for tu in to_update]

        print()

    def _entry_list2dict(self, entry):
        p, e = entry['path'], entry['entry']
        e = self.__leaf_dict2list(e)
        new = {}
        for n, el in enumerate(reversed(p)):
            if n == 0:
                new[el] = e
            else:
                new = {el: new}
        return new

    def __leaf_dict2list(self, leaf):
        return [leaf[L] for L in self.ref.ont['legend']]

    def _filter_entries(self, onto):
        def has_same_path(r):
            out = [True for rr in ref_res if rr['path'] == r['path']]
            return True if out else False

        def has_same_lemma(r):
            out = [True for rr in ref_res if rr['entry']['col1_legend'] == r['entry']['col1_legend']]
            return True if out else False

        to_update = []
        to_organize = []
        words = onto.list_words()
        for w in words:
            res = onto.find_word(w)
            ref_res = self.ref.find_word(w)
            for r in res:
                if r in ref_res:
                    continue
                elif has_same_path(r) and has_same_lemma(r):
                    to_update.append(r)
                else:
                    to_organize.append(r)
        return to_update, to_organize

    def diff_from_onto(self, onto):
        pass

    def update_ref(self, onto):
        pass
