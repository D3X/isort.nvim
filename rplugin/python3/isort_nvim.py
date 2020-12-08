from pathlib import Path

import pynvim

try:
    import isort
    isort_imported = True
except ImportError:
    isort_imported = False


def _count_blanks(lines):
    blanks = 0

    for i, line in enumerate(reversed(lines)):
        if line.strip():
            break

        blanks += 1

    return blanks


@pynvim.plugin
class IsortNvim:
    def __init__(self, vim):
        self.vim = vim

    @pynvim.command(
        'Isort',
        nargs='*',
        range='%',
        sync=True,
    )
    def isort_command(self, args, range):
        if not isort_imported:
            self.error('Could not import isort')
            return

        old_lines = self.vim.current.buffer[range[0] - 1:range[1]]
        blanks = _count_blanks(old_lines)

        output = isort.code(
            '\n'.join(old_lines),
            file_path=Path(self.vim.current.buffer.name)

        )
        new_lines = output.split('\n')
        new_blanks = _count_blanks(new_lines)
        if new_blanks > blanks:
            del new_lines[-(new_blanks - blanks):]

        if old_lines != new_lines:
            self.vim.current.buffer[range[0] - 1:range[1]] = new_lines

    def error(self, msg):
        self.vim.err_write('[isort] {}\n'.format(msg))
