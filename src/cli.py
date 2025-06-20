#!/usr/bin/env python3

import os
from sys import exit

# os.environ["is_dev"] = "True"
os.environ["is_cli"] = "True"

import argparse
from rich.console import Console

from cli.packs import getPacksCommand, createPackCommand, deletePacksCommand

parser = argparse.ArgumentParser(
    "YAMCPACK", description="Yet Another (Minecraft) Mod Pack Downloader"
)
sub_parsers = parser.add_subparsers(help="CLI Commands", dest="command")

# ----- Packs -----

packs_parser = sub_parsers.add_parser("packs", help="Manage packs")
sub_packs_parsers = packs_parser.add_subparsers(dest="subcommand")
packs_list = sub_packs_parsers.add_parser("list", help="List all packs")
packs_new = sub_packs_parsers.add_parser("new", help="Create a new pack")
packs_delete = sub_packs_parsers.add_parser("delete", help="Delete pack")

pack_parser = sub_parsers.add_parser("pack")
sub_pack_parsers = pack_parser.add_subparsers(
    help="Manage pack commands", dest="subcommand"
)

console = Console()

if __name__ == "__main__":
    args = parser.parse_args()

    if os.getenv("is_dev"):
        console.print("--- DEBUG MODE ---", style="bold red")
        console.print("Provided arguments:", args)
        console.print(f"{'-':-<18}", style="bold red")
        console.print("\n")

    if args.command is None:
        parser.print_help()
        exit(1)

    if args.command == "packs" and args.subcommand is None:
        packs_parser.print_help()
        exit(1)

    if args.command == "packs" and args.subcommand == "list":
        getPacksCommand()

    if args.command == "packs" and args.subcommand == "new":
        createPackCommand()

    if args.command == "packs" and args.subcommand == "delete":
        deletePacksCommand()

    if args.command == "pack" and args.subcommand is None:
        pack_parser.print_help()
        exit(1)
