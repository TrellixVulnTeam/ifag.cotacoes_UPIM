#!/usr/bin/env bash
#set -ex

export DJANGO_SETTINGS_MODULE=project.settings.dev

export BASE_DIR=`python -c "
import $DJANGO_SETTINGS_MODULE as settings
print(settings.BASE_DIR)"`

export PYTHONPATH=$BASE_DIR
$BASE_DIR/bin/dropdb.sh || exit 1;
$BASE_DIR/bin/createdb.sh || exit 1;

## Importando fixtures
python $BASE_DIR/manage.py loaddata users
python $BASE_DIR/manage.py loaddata category
python $BASE_DIR/manage.py loaddata group
python $BASE_DIR/manage.py loaddata unit
python $BASE_DIR/manage.py loaddata indicator
python $BASE_DIR/manage.py loaddata source
python $BASE_DIR/manage.py loaddata sourceindicatorcity
python $BASE_DIR/manage.py loaddata quotation
python $BASE_DIR/manage.py loaddata history