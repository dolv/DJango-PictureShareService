FROM python:3.6.5-stretch

MAINTAINER ODudchenko@gmail.com
ENV DOCKERIZE_VERSION=v0.6.1 \
	APP_DIR=/app/PictureShareService \
	APP_VIRTUALENV_PATH=/app/VirtualENV \
	DB_DIR=${APP_DIR}/DB

WORKDIR ${APP_DIR}
COPY . .

# Install required packages and remove the apt packages cache when done.
RUN mkdir -p ${APP_DIR} ${APP_VIRTUALENV_PATH} ${DB_DIR}\
    && apt-get update \
    && apt-get upgrade -y \ 	
    && apt-get install -y --no-install-recommends \
	  git \
	  wget \
	  nginx \
	  supervisor \
	  sqlite3 \
	&& pip3 install -U pip setuptools urllib3 pyopenssl ndg-httpsclient pyasn1 \
	&& pip install --upgrade pip setuptools \
    && rm -rf /var/lib/apt/lists/* \
# install uwsgi now because it takes a little while
    && pip3 install uwsgi \
# configure Python virtual environment
	&& python3 -m venv ${APP_VIRTUALENV_PATH} \
	&& chmod +x ${APP_VIRTUALENV_PATH}/bin/activate \
	&& /bin/bash -c "source ${APP_VIRTUALENV_PATH}/bin/activate \
	&& which pip3 \
	&& which python3 \
	&& pip3 install --upgrade pip \
	&& pip3 install -r ${APP_DIR}/requirements.txt" \
# install Dockerize
    && wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
# setup all the configfiles
    # && echo "daemon off;" >> /etc/nginx/nginx.conf
# COPY nginx-app.conf.tmpl /etc/nginx/sites-available/default.tmpl
# COPY supervisor-app.conf.tmpl /etc/supervisor/conf.d/supervisor-app.conf.tmpl
    
EXPOSE 8001

ENTRYPOINT [ "./run_dockerize.sh" ] 

# CMD ["dockerize", \
#      "-template", "/etc/nginx/sites-available/default.tmpl:/etc/nginx/sites-available/default", \
# 	 "-template", "/etc/supervisor/conf.d/supervisor-app.conf.tmpl:/etc/supervisor/conf.d/supervisor-app.conf", \
# 	 "-template", "$APP_DIR/settings.py.tmpl:$APP_DIR/PictureShareService/settings.py", \
#      "-template", "/app/DJango/uwsgi.ini.tmpl:/app/uwsgi.ini" \
# 	 "-stdout", "/var/log/nginx/access.log", \
# 	 "-stderr", "/var/log/nginx/error.log", \
# 	 "uwsgi --ini $APP_DIR/uwsgi.ini"]