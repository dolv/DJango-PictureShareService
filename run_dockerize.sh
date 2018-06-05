#!/usr/bin/env bash
# set -x
source ${APP_VIRTUALENV_PATH}/bin/activate
which pip3
which python3
pip3 freeze
python3 manage.py migrate
python3 manage.py collectstatic
dockerize \
-template ${APP_DIR}/settings.py.tmpl:${APP_DIR}/PictureShareService/settings.py \
-template ${APP_DIR}/uwsgi.ini.tmpl:${APP_DIR}/uwsgi.ini \
uwsgi --ini ${APP_DIR}/uwsgi.ini${UWSGI_ENV}
# set +x