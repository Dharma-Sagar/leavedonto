from .leavedonto import LeavedOnto


class OntoManager:
    def __init__(self, onto_ref):
        self.ref = LeavedOnto(onto_ref)

    def merge_to_onto(self, onto):
        # TODO: sanity check that both legends have same elements
        to_organize, to_update = self._filter_entries(onto)
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
        return [leaf[l] for l in self.ref.ont['legend']]

    def _filter_entries(self, onto):
        def has_same_path(r):
            out = [True for rr in ref_res if rr['path'] == r['path']]
            return True if out else False

        def has_same_lemma(r):
            out = [True for rr in ref_res if rr['entry']['col1_legend'] == r['entry']['col1_legend']]
            return True if out else False

        onto = LeavedOnto(onto)
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
