from pathlib import Path

import yaml


class Convert2Yaml:
    def __init__(self, ont_path, ont):
        self.ont_path = ont_path
        self.ont = ont

    def convert2yaml(self, out_path=None):
        out = yaml.safe_dump(self.ont, allow_unicode=True)
        out = self.__group_leaf_entries(out)

        if not out_path:
            out_path = self.ont_path.parent
        out_file = Path(out_path) / (self.ont_path.stem + '.yaml')
        out_file.write_text(out)

    def __group_leaf_entries(self, out):
        start = '- -'
        legend = '- '
        processed = []
        cur_idx = 0
        lines = out.split('\n')
        while cur_idx < len(lines):
            cur_line = lines[cur_idx]
            if start not in cur_line and not cur_line.startswith(legend):
                processed.append(cur_line)

            elif cur_line.startswith(legend):
                # find legend
                group = [cur_line]
                while lines[cur_idx].startswith(legend):
                    group.append(lines[cur_idx])
                    cur_idx += 1
                cur_idx -= 1  # undo extra increment

                # convert to list
                parts = []
                for el in group[1:]:
                    parts.append(el.replace(legend, ''))
                formatted = f' [{", ".join(parts)}]'

                processed[-1] += formatted

            else:
                # find entries
                prefix = cur_line[:cur_line.find(start)]
                group = [cur_line]
                cur_idx += 1
                while lines[cur_idx].startswith(f'{prefix}  -'):
                    group.append(lines[cur_idx])
                    cur_idx += 1
                cur_idx -= 1  # undo extra increment

                # convert to list
                parts = [group[0].replace(prefix + start + ' ', '')]
                for el in group[1:]:
                    parts.append(el.replace(f'{prefix}  - ', ''))
                formatted = f'{prefix}- [{", ".join(parts)}]'

                processed.append(formatted)
            cur_idx += 1

        return '\n'.join(processed)
