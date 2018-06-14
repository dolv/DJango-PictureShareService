#!/usr/bin/env bash
# set -x
dockerize \
-template ${APP_DIR}/settings.py.tmpl:${APP_DIR}/PictureShareService/settings.py \
-template ${APP_DIR}/uwsgi.ini.tmpl:${APP_DIR}/uwsgi.ini \
uwsgi --ini ${APP_DIR}/uwsgi.ini${UWSGI_ENV}
# set +x