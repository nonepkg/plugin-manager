from nonebot.rule import ArgumentParser

from .handle import *

parser = ArgumentParser("npm", add_help=False)
parser.add_argument(
    "-h", "--help", action="store_true", help="show this help message and exit"
)

subparsers = parser.add_subparsers()

list_parser = subparsers.add_parser("list", help="show plugin list")
list_parser.add_argument("-s", "--store", action="store_true")
list_parser.add_argument("-d", "--default", action="store_true")
list_parser.add_argument("-g", "--group", action="store", type=int)
list_parser.set_defaults(handle=handle_list)

block_parser = subparsers.add_parser("block", help="block plugin")
block_parser.add_argument("plugins", nargs="*")
block_parser.add_argument("-d", "--default", action="store_true")
block_parser.add_argument("-a", "--all", action="store_true")
block_parser.add_argument("-g", "--group", action="store", type=int)
block_parser.set_defaults(handle=handle_block)

unblock_parser = subparsers.add_parser("unblock", help="unblock plugin")
unblock_parser.add_argument("plugins", nargs="*")
unblock_parser.add_argument("-d", "--default", action="store_true")
unblock_parser.add_argument("-a", "--all", action="store_true")
unblock_parser.add_argument("-g", "--group", action="store", type=int)
unblock_parser.set_defaults(handle=handle_unblock)

install_parser = subparsers.add_parser("install", help="install plugin")
install_parser.add_argument("plugins", nargs="*")
install_parser.add_argument("-i", "--index", action="store", type=str)
install_parser.set_defaults(handle=handle_install)

update_parser = subparsers.add_parser("update", help="update plugin")
update_parser.add_argument("plugins", nargs="*")
update_parser.add_argument("-a", "--all", action="store_true")
update_parser.add_argument("-i", "--index", action="store", type=str)
update_parser.set_defaults(handle=handle_update)

uninstall_parser = subparsers.add_parser("uninstall", help="uninstall plugin")
uninstall_parser.add_argument("plugins", nargs="*")
uninstall_parser.add_argument("-a", "--all", action="store_true")
uninstall_parser.set_defaults(handle=handle_uninstall)
