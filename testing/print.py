from tqdm import tqdm
import time
import sys


class MultiLineProgress:
    def __init__(self, states):
        self.states = states
        self.bars = [
            tqdm(total=state['total'], position=i, leave=True, file=sys.stdout,
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{postfix}]')
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

    def close(self):
        for bar in self.bars:
            bar.close()


# Define initial states with different totals and custom info
states = [
    {'description': 'Task 1', 'progress': 0, 'total': 200, 'info': 'Init'},
    {'description': 'Task 2', 'progress': 0, 'total': 150, 'info': 'Starting'},
    {'description': 'Task 3', 'progress': 0, 'total': 100, 'info': 'Ready'},
]

if __name__ == '__main__':

    # Create multi-line progress bar
    ml_progress = MultiLineProgress(states)

    try:
        # Simulate progress
        for i in range(100):
            time.sleep(0.1)
            ml_progress.update_progress(0, i * 2, f'Iteration {i}')
            ml_progress.update_progress(1, i * 1.5, f'Phase {i // 10}')
            ml_progress.update_progress(2, i + 1, f'Step {i}')
    except KeyboardInterrupt:
        pass
    finally:
        ml_progress.close()
