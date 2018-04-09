import neovim


try:
    from isort import SortImports
    isort_imported = True
except ImportError:
    isort_imported = False


ISORT_COMMAND = 'isort'
ISORT_OPTIONS = [
    '--line-width',
    '--top',
    '--future',
    '--builtin',
    '--thirdpaty',
    '--project',
    '--virtual-env',
    '--multi-line',
    '--indent',
    '--add-import',
    '--force-adds',
    '--remove-import',
]


def _count_blanks(lines):
    for i, line in enumerate(reversed(lines)):
        if line.strip():
            return i


@neovim.plugin
class IsortNvim:
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command(
        'Isort',
        nargs='*',
        range='%',
        complete='customlist,IsortCompletions',
        sync=True,
    )
    def isort_command(self, args, range):
        if not isort_imported:
            self.error('Could not import isort')
            return

        old_lines = self.nvim.current.buffer[range[0] - 1:range[1]]
        blanks = _count_blanks(old_lines)

        output = SortImports(file_contents='\n'.join(old_lines)).output
        new_lines = output.split('\n')
        new_blanks = _count_blanks(new_lines)
        if new_blanks > blanks:
            del new_lines[-(new_blanks - blanks):]

        if old_lines != new_lines:
            self.nvim.current.buffer[range[0] - 1:range[1]] = new_lines

    def error(self, msg):
        self.nvim.err_write('[isort] {}\n'.format(msg))

    @neovim.function('IsortCompletions', sync=True)
    def isort_completions(self, args):
        arglead, cmdline, cursorpos, *_ = args
        return [
            option
            for option in ISORT_OPTIONS
            if option.startswith(arglead)
        ]
