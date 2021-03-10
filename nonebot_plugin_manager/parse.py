from nonebot.rule import ArgumentParser

parser = ArgumentParser("npm", add_help=False)
parser.add_argument(
    "-h", "--help", action="store_true", help="show this help message and exit"
)

subparsers = parser.add_subparsers()

block_parser = subparsers.add_parser("block", help="block plugin")
block_parser.add_argument("plugins", nargs="*")
block_parser.add_argument("-d", "--default", action="store_true")
block_parser.add_argument("-a", "--all", action="store_true")
block_parser.add_argument("-g", "--group", action="store", type=int)
block_parser.set_defaults(command="block")

unblock_parser = subparsers.add_parser("unblock", help="unblock plugin")
unblock_parser.add_argument("plugins", nargs="*")
unblock_parser.add_argument("-d", "--default", action="store_true")
unblock_parser.add_argument("-a", "--all", action="store_true")
unblock_parser.add_argument("-g", "--group", action="store", type=int)
unblock_parser.set_defaults(command="unblock")

list_parser = subparsers.add_parser("list", help="show plugin list")
list_parser.add_argument("-d", "--default", action="store_true")
list_parser.add_argument("-g", "--group", action="store", type=int)
list_parser.set_defaults(command="list")
