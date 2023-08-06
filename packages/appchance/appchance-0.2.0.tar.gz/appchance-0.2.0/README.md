# Appchance :: Backend Special Forces

Hacks and project automation. Toolbelt for wizards and ninjas.

#
## Installation
Install package with pip

    pip install appchance

#
### Dodos configuration
You can optionally overwrite dodos options with `doit.cfg` file in your project root directory.

    [GLOBAL]
    compose_cmd="docker-compose -f compose.yml"
    django_service="django"


#
### Usage
Initialize and start new django application boosted by docker containers.

    $ pip install appchance
    $ dodo init

And that's it! Your django application in docker is up and running!

#
## Subpackages
Tools includes

- `dodos` = project (docker & django) automation based on doit python package
- `pickup` = module for cart delivery pickup points clients
- `shop` = common models, serializers etc for django mcommerce

#
## Roadmap
Roadmap for future releases

* `0.2.0` = Cookiecutter django-appchance
* `0.3.0` = Sentry integrations
* `0.3.5` = ELK integrations
