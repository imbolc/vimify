"""
Vimification of an linux environment

wget -O - https://raw.github.com/imbolc/vimify/master/vimify.py | python3
"""
from pathlib import Path

UPDATES = [
    [
        "~/.bashrc",
        [
            "set -o vi",
            "export VISUAL=vim",
            "export EDITOR=vim",
            "complete -cf sudo",
        ],
    ],
    ["~/.inputrc", ["set editing-mode vi"]],
]
VIM_CONFIG = """
set nocompatible
let mapleader=","

" do not create backups
set nobackup
set noswapfile
set nowritebackup

set nowrap
set novisualbell
set t_vb=
set backspace=indent,eol,start whichwrap+=<,>,[,]

syntax on
set ttyfast
set ruler               " show the cursor position all the time
set history=50          " history of commands
set undolevels=500      " history of undos

set showcmd             " display incomplete commands
set autowrite           " automatically :write before running commands
set nonumber
set foldmethod=syntax
set foldlevelstart=200  " open all folds when opening a file

" indent
set smarttab
set tabstop=4
set softtabstop=4
set expandtab
set shiftwidth=4
set autoindent

" encoding
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8,cp1251,koi8-r,cp866,ucs-bom,ascii
set fileformat=unix
set fileformats=unix,dos,mac

" search
set ignorecase
set smartcase
set incsearch
set showmatch
set hlsearch
set gdefault

" reselect visual block after indent/outdent
vnoremap < <gv
vnoremap > >gv
"""


def update_files():
    for path, updates in UPDATES:
        path = Path(path).expanduser()
        if not path.exists():
            print("touch", path)
            path.touch()
        text = path.read_text()
        for update in updates:
            if update not in text:
                print(str(path) + " << " + update)
                with path.open("a") as f:
                    if text and not text.endswith("\n"):
                        f.write("\n")
                        text += "\n"
                    f.write(update + "\n")


def is_vim_config_exists():
    paths = ["~/.vimrc", "~/.config/nvim"]
    for path in paths:
        if Path(path).expanduser().exists():
            return True


def create_vim_config():
    if is_vim_config_exists():
        return
    print("creating a base vim config")
    path = Path("~/.vimrc").expanduser()
    with path.open("w") as f:
        f.write(VIM_CONFIG)
    nvim = Path("~/.config/nvim/init.vim").expanduser()
    nvim.parent.mkdir(parents=True, exist_ok=True)
    nvim.symlink_to(path)


if __name__ == "__main__":
    update_files()
    create_vim_config()
