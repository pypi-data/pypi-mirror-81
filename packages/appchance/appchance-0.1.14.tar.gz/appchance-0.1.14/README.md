# Appchance :: Backend Special Forces Team

Common django classes, hacks and project automation. Toolbelt for wizards and ninjas.

#
## Installation
Install package with pip

    pip install appchance
#
## Subpackages
Tools includes

- `dodos` = project (docker & django) automation based on doit python package
- `pickup` = module for cart delivery pickup points clients
- `shop` = common models, serializers etc for django mcommerce

#
## Dodos
`Appchance projects automation.`


### Django integration

1. Install required packages

    `pip install appchance`

2. Add to your project file `dodos.py`.
    ```python
    #! /usr/bin/env python3

    import sys
    import importlib
    from doit.doit_cmd import DoitMain
    from doit.cmd_base import ModuleTaskLoader

    if __name__ == "__main__":
        sys.exit(
            DoitMain(
                ModuleTaskLoader(
                    importlib.import_module(f'appchance.dodos.tasks.django'))
            ).run(sys.argv[1:]))
    ```

3. Optionally create an alias for your new command.
    ```bash
    $ echo alias d="./dodos.py" >> ~/.bash_aliases
    ```
#
### Using dodos
List available commands

    $ ./dodos.py list

Or if alias created:

    $ d list


#
## Roadmap
Roadmap for future releases

* `0.2.0` = Sentry integrations
* `0.3.0` = ELK integrations
#
