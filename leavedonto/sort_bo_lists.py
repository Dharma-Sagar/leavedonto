from tibetan_sort import TibetanSort


class SortBoLists(TibetanSort):
    def __init__(self):
        super().__init__()

    def sort_list_of_lists(self, list_of_lists):
        # extract first elements + append position
        first_els = []
        for n, list in enumerate(list_of_lists):
            first_els.append(f'{list[0]}—{n}')
        sorted_firsts = self.sort_list(first_els)

        # use position from sorted first elements to sort lists
        sorted = []
        for el in sorted_firsts:
            _, num = el.split('—')
            num = int(num)
            sorted.append(list_of_lists[num])

        return sorted
