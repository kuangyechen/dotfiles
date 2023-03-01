import os
import platform


class Config:
    os_type = platform.system().upper()
    verbose = False
    dry_run = True
    home_dir = os.path.expanduser('~')
    dotfiles_dir = None
    yes = False
