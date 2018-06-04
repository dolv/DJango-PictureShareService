FROM debian:8

MAINTAINER ODudchenko@gmail.com
ENV DOCKERIZE_VERSION v0.6.1
ENV APP_DIR /app/PictureShareService
ENV APP_VIRTUALENV_PATH /app/VirtualENV

WORKDIR ${APP_DIR}
COPY . .

# Install required packages and remove the apt packages cache when done.
RUN apt-get update \
    && apt-get upgrade -y \ 	
    && apt-get install -y \
	  git \
	  python3 \
	  python3-dev \
	  python3-setuptools \
	  python3-pip \
	  nginx \
	  supervisor \
	  sqlite3 \
	&& pip3 install -U pip setuptools \
    && rm -rf /var/lib/apt/lists/* \
# install uwsgi now because it takes a little while
    && pip3 install uwsgi \
# install Dockerize
    && wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
# configure Python virtual environment
	&& python3 -m venv ${APP_VIRTUALENV_PATH} \
	&& chmod +x ${APP_VIRTUALENV_PATH}/bin/activate \
	&& source ${APP_VIRTUALENV_PATH}/bin/activate \
	&& pip install -r ${APP_DIR}/requirements.txt \
# setup all the configfiles
    && echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf.tmpl /etc/nginx/sites-available/default.tmpl
COPY supervisor-app.conf.tmpl /etc/supervisor/conf.d/
    
EXPOSE 80

CMD ["dockerize", \
     "-template", "/etc/nginx/sites-available/default.tmpl:/etc/nginx/sites-available/default", \
	 "-template", "/etc/supervisor/conf.d/nginx-app.conf.tmpl:/etc/supervisor/conf.d/nginx-app.conf", \
	 "-template", "/app/settings.py.tmpl:/app/PictureShareService/settings.py", \
	 "-stdout", "/var/log/nginx/access.log", \
	 "-stderr", "/var/log/nginx/error.log", \
	 "nginx"]