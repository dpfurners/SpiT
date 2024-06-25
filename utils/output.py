from tqdm import tqdm
import sys


class MultiLineProgress:
    def __init__(self, states):
        self.states = states
        self.bars = [
            tqdm(total=state['total'], position=i, leave=True, file=sys.stdout,
                 bar_format='{l_bar:>11}{bar}| {n_fmt:>2}/{total_fmt:>2} [{postfix}]')
            for i, state in enumerate(states)
        ]
        self.update_states(states)

    def update_states(self, states):
        for bar, state in zip(self.bars, states):
            bar.set_description(state['description'])
            bar.n = state['progress']
            bar.set_postfix_str(state['info'])
            bar.refresh()

    def update_progress(self, index, progress, info=""):
        self.bars[index].n = progress
        if info:
            self.bars[index].set_postfix_str(info)
        self.bars[index].refresh()

    def update_total(self, index, new_total):
        self.bars[index].total = new_total
        self.states[index]['total'] = new_total
        self.bars[index].refresh()

    def close(self):
        for bar in self.bars:
            bar.close()
