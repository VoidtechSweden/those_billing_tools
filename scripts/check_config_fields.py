#!/usr/bin/env python

import configparser
import sys
import os
import re

"""Script to check that all fields in template.config are present in config.py and described in docs/Configuration.md"""

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "..", "template.config")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.py")
DOC_PATH = os.path.join(os.path.dirname(__file__), "..", "docs", "Configuration.md")


def get_template_fields(template_path):
    parser = configparser.ConfigParser()
    parser.read(template_path)
    fields = set()
    for section in parser.sections():
        for option in parser.options(section):
            fields.add(option)
    return fields


def get_config_fields(config_path):
    fields = set()
    with open(config_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if ":" in line and not line.startswith("#") and not line.startswith("def "):
            parts = line.split(":")
            field = parts[0].strip()
            if field and not field.startswith("self") and not field.startswith("class"):
                fields.add(field)
    return fields


def get_doc_fields(doc_path):
    fields = set()
    pattern = re.compile(r"\*\*(\w+)\*\*\: ")
    with open(doc_path, "r", encoding="utf-8") as f:
        for line in f:
            for match in pattern.findall(line):
                fields.add(match)
    return fields


def main():
    template_fields = get_template_fields(TEMPLATE_PATH)
    config_fields = get_config_fields(CONFIG_PATH)
    doc_fields = get_doc_fields(DOC_PATH)

    missing_in_config = template_fields - config_fields
    missing_in_doc = template_fields - doc_fields

    if missing_in_config:
        print("Missing fields in config.py:", ", ".join(missing_in_config))
    if missing_in_doc:
        print("Missing fields in docs/Configuration.md:", ", ".join(missing_in_doc))
    if missing_in_config or missing_in_doc:
        sys.exit(1)
    print(
        "All template.config fields are present in config.py and docs/Configuration.md"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
