FROM ubuntu:16.04
ENV PATH /:$PATH
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y libpq-dev apache2 libapache2-mod-wsgi
RUN a2enmod wsgi
COPY . /var/www/featurerequest/ 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY apache/FeatureRequest.conf /etc/apache2/sites-available/FeatureRequest.conf
COPY apache/servername.conf /etc/apache2/conf-available/servername.conf
COPY apache/apache.wsgi /var/www/featurerequest/servername.conf
run service apache2 start
RUN a2ensite FeatureRequest
RUN a2enconf servername
RUN service apache2 restart
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
EXPOSE 80
EXPOSE 443
ENTRYPOINT /docker-entrypoint.sh
