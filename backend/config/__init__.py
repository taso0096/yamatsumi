import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-p",
    "--production",
    action="store_true",
    help="use production config")
parser.add_argument(
    "-d",
    "--development",
    action="store_true",
    help="use development config")
parser.add_argument(
    "-s",
    "--ssl",
    action="store_true",
    help="use ssl server")
args = parser.parse_args()
if args.production:
    from config.production import *
else:
    from config.development import *
