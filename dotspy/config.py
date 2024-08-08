import os
import platform


MACOS = "DARWIN"
LINUX = "LINUX"
DEBIAN = "DEBIAN"
UBUNTU = "UBUNTU"


def get_dist(os_type):
    if os_type == LINUX:
        dist = platform.freedesktop_os_release()
        for _, v in dist.items():
            if DEBIAN in v.upper() or UBUNTU in v.upper():
                return DEBIAN
        return None
    else:
        return None


os_type = platform.system().upper()
verbose = False
dry_run = True
home_dir = os.path.expanduser("~")
dotfiles_dir = None
yes = False
