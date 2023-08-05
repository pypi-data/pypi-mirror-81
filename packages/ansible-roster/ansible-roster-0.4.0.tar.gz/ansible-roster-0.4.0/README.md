[![documentation](https://img.shields.io/badge/documentation-html-informational)](https://ansible-kheops.gitlab.io/plugins/roster/index.html)
[![python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-informational)](https://pypi.org/project/kheops-roster/)

# Ansible Roster Plugin

This repository contains an Ansible Inventory Plugin to generate inventory from a subjectively simpler inventory description file, here within called a `roster` while having more possibilities.

It supports host ranges, _eg: "[0:9]"_, but also regex hostnames, _eg: "(dev|prd)-srv"_. It handles variables declared as lists by appending the values instead of replacing them.

This inventory plugin has been written with [*debops*](https://docs.debops.org/en/master/) in mind.

## Installation

Install latest version:

~~~bash
python3 -mpip install -U ansible-roster
~~~

## Usage

The roster is a file in yaml format and 'yml' or 'yaml' file extension.

In order for Ansible to use the plugin and parse your roster file, several conditions must be met:

* Your yaml file must contain a line indicating that the file is in the roster format.

* You must activate plugins and enable the roster inventory plugin in your `ansible.cfg`, or in your `.debops.cfg` if using *debops*

**Sample `ansible.cfg`**

~~~toml
[defaults]
# The following line prevents having to pass -i to ansible-inventory.
# Filename can be anything as long as it has a 'yml' or 'yaml' extension although
# the plugin will directly accept any file named 'roster.yml'.
inventory = roster.yml

[inventory]
# You must enable the roster plugin if 'auto' does not work for you
enable_plugins = roster
~~~

**Sample `.debops.cfg`**

~~~toml
[ansible inventory]
enabled = roster
enable_plugins = roster
~~~

### Simpler syntax

A roster inventory has a subjectively simpler syntax than a Ansible yaml inventory file. Instead of specifing *children* which have to be known in advance, you specify the *parents* of your host.

A roster inventory is, at least, a single yaml file where the plugin to be used is declared, and groups and hosts declared in yaml syntax.

A sample, commented, file named 'roster.yml.tpl' is located at the root of the git repository.

*Example:*
~~~yaml
---
# Tell ansible that this yaml file is a roster file:
plugin: roster

hosts:
  # We have a single host in this inventory:
  debian.example.com:
~~~

### File inclusion

Instead of including every file found in a inventory folder, a roster inventory will only include explicitly specified files. Globbing is supported.

~~~yaml
plugin: roster

include:
  # include an exact file match
  - distrib/debian.yml

  # include with wildcard:
  - hosts/*.yml
~~~

### Ranges and Regex support

Hosts can be declared with ranges, or with regex that will be expanded.

Ranges are specified by a integer lower and upper bound in square braces, such as `[0:9]` to expand into 10 different hostnames.

Regex must be enclosed in parentheses: `(front|back)end`

For example:

~~~yaml
plugin: roster

hosts:
  # Generate 10 hostnames: sql-0.example.com to sql-9.example.com
  sql-[0:9].example.com:

  # Generate 2 hostnames: frontend.example.com and backend.example.com
  (front|back)end.example.com:
~~~

### Labels

TODO, lorem ipsum

### Variable priority

TODO, lorem ipsum

### Variable merging

TODO, lorem ipsum

The roster inventory file is a typical yaml file.


## Development

To run unit tests, you can simply run the make target:

~~~bash
# run all tests:
make check
~~~

It's also possible to quickly check the output inventory:
~~~bash
export PYTHONPATH="$PYTHONPATH:$(pwd)"
ANSIBLE_INVENTORY_ENABLED=roster ansible-inventory --list -i roster.yml
~~~

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Locations

  * Documentation: [https://ansible-kheops.gitlab.io/plugins/roster/index.html](https://ansible-kheops.gitlab.io/plugins/roster/index.html)
  * GitLab: [https://gitlab.com/ansible-kheops/plugins/roster](https://gitlab.com/ansible-kheops/plugins/roster)
  * PyPi: [https://pypi.org/project/ansible-roster](https://pypi.org/project/ansible-roster)

