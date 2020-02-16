#!/usr/bin/env python3
#
#  2020 February 15 - Everaldo Canuto
#
#  I dedicate any and all copyright interest in this software to the
#  public domain. I make this dedication for the benefit of the public at
#  large and to the detriment of my heirs and successors. I intend this
#  dedication to be an overt act of relinquishment in perpetuity of all
#  present and future rights to this software under copyright law.
#


import argparse
import pathlib
import json
import yaml


__prgdesc__ = "Simplified YAML Ansible inventory"
__version__ = "0.1"


class SimplifiedAnsibleInventory(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description=__prgdesc__)

        parser.add_argument("-v", "--version", action="version",
                            version="%(prog)s " + __version__)

        parser.add_argument("-l", "--list", action="store_true",
                            help="output inventory")

        parser.add_argument("-H", "--host", action="store",
                            help="output host vars")

        args = parser.parse_args()

        self.parse_yaml()

        if args.list:
            self.output_list()

        if args.host:
            self.output_host(args.host)

    def print_json(self, data):
        print(json.dumps(data or {}, indent=4, sort_keys=False))

    def parse_yaml(self):
        self.groups = {}
        self.hosts = {}

        filename = pathlib.Path(__file__).stem + ".yml"

        with open(filename) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        for entry in data:
            if entry.get("name"):
                self.groups[entry.get("name")] = entry
            if entry.get("host"):
                self.hosts[entry.get("host")] = entry

        for name, host in self.hosts.items():
            tags = host.get("tags") or ["ungrouped"]
            for tag in tags:
                if not tag in self.groups:
                    self.groups[tag] = {}

                group = self.groups[tag]
                if not "hosts" in group:
                    group["hosts"] = []

                group["hosts"].append(name)

    def output_list(self):
        inventory = {}
        for name, group in self.groups.items():
            inventory[name] = {}
            if name != "all":
                inventory[name]["hosts"] = group["hosts"]
            if "vars" in group:
                inventory[name]["vars"] = group["vars"]

        self.print_json(inventory)
        exit(0)

    def output_host(self, name):
        hostvars = {}
        if name in self.hosts:
            hostvars = self.hosts[name].get("vars")

        self.print_json(hostvars)
        exit(0)

if __name__ == "__main__":
    SimplifiedAnsibleInventory()
