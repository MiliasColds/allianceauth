# Discourse

## Prepare Your Settings
In your auth project's settings file, do the following:
 - Add `'allianceauth.services.modules.discourse',` to your `INSTALLED_APPS` list 
 - Append the following to your local.py settings file:
 

    # Discourse Configuration
    DISCOURSE_URL = ''
    DISCOURSE_API_USERNAME = ''
    DISCOURSE_API_KEY = ''
    DISCOURSE_SSO_SECRET = ''


## Install Docker

    wget -qO- https://get.docker.io/ | sh

## Install Discourse

### Download Discourse

    mkdir /var/discourse
    git clone https://github.com/discourse/discourse_docker.git /var/discourse

### Configure

    cd /var/discourse
    cp samples/standalone.yml containers/app.yml
    nano containers/app.yml

Change the following:
 - `DISCOURSE_DEVELOPER_EMAILS` should be a list of admin account email addresses separated by commas.
 - `DISCOUSE_HOSTNAME` should be `discourse.example.com` or something similar.
 - Everything with `SMTP` depends on your mail settings. [There are plenty of free email services online recommended by Discourse](https://github.com/discourse/discourse/blob/master/docs/INSTALL-email.md#recommended-email-providers-for-discourse) if you haven't set one up for auth already.

To install behind apache/nginx, look for this section:

    ...
    ## which TCP/IP ports should this container expose?
    expose:
      - "80:80"   # fwd host port 80   to container port 80 (http)
    ...

Change it to this:

    ...
    ## which TCP/IP ports should this container expose?
    expose:
      - "7890:80"   # fwd host port 7890   to container port 80 (http)
    ...

Or any other port will do, if taken. Remember this number.

### Build and launch

    nano /etc/default/docker

Uncomment this line:

    DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4"

Restart docker:

    service docker restart

Now build:

    ./launcher bootstrap app
    ./launcher start app

## Web Server Configuration

***

You will need to configure your web server to proxy requests to Discourse.

A minimal apache config might look like:

    <VirtualHost *:80>
        ServerName discourse.example.com
        ProxyPass / http://0.0.0.0:7890/
        ProxyPassReverse / http://0.0.0.0:7890/
    </VirtualHost>

A minimal nginx config might look like:

    server {
        listen 80;
        server_name discourse.example.com;
        location / {
            include proxy_params;
            proxy_pass http://127.0.0.1:7890;
        }
    }

### Setting up SSL

It is 2017 and there is no reason why you should not setup a SSL certificate and enforce https. You may want to consider certbot with Let's encrypt: https://www.digitalocean.com/community/tutorials/how-to-secure-apache-with-let-s-encrypt-on-ubuntu-16-04

    sudo certbot --apache -d example.com

now adapt the apache configuration:

    sudo nano /etc/apache2/sites-enabled/discourse.conf

and adapt it followlingly:

    <VirtualHost *:80>
        ServerName discourse.example.com
        RewriteEngine on
        RewriteCond %{SERVER_NAME} =discourse.example.com
        RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
    </VirtualHost>

Then adapt change the ssl-config file:

    sudo nano /etc/apache2/sites-enabled/discourse-le-ssl.conf

and adapt it followlingly:

    <IfModule mod_ssl.c>
    <VirtualHost *:443>
      ServerName discourse.example.com
      ProxyPass / http://127.0.0.1:7890/
      ProxyPassReverse / http://127.0.0.1:7890/
      ProxyPreserveHost On
      RequestHeader set X-FORWARDED-PROTOCOL https
      RequestHeader set X-FORWARDED-SSL on
      SSLCertificateFile /etc/letsencrypt/live/discourse.example.com/fullchain.pem
      SSLCertificateKeyFile /etc/letsencrypt/live/discourse.example.com/privkey.pem
      Include /etc/letsencrypt/options-ssl-apache.conf
    </VirtualHost>
    </IfModule>

make sure that `a2enmod headers` is enabled and run:

      sudo service apache2 restart

Now you are all set-up and can even enforce https in discourse settings.





## Configure API

### Generate admin account

From the `/var/discourse` directory,

    ./launcher enter app
    rake admin:create

Follow prompts, being sure to answer `y` when asked to allow admin privileges.

### Create API key

Navigate to `discourse.example.com` and log on. Top right press the 3 lines and select `Admin`. Go to API tab and press `Generate Master API Key`.

Add the following values to your auth project's settings file:
 - `DISCOURSE_URL`: `https://discourse.example.com` (do not add a trailing slash!)
 - `DISCOURSE_API_USERNAME`: the username of the admin account you generated the API key with
 - `DISCOURSE_API_KEY`: the key you just generated

***
### Configure SSO

Navigate to `discourse.example.com` and log in. Back to the admin site, scroll down to find SSO settings and set the following:
 - `enable_sso`: True
 - `sso_url`: `http://example.com/discourse/sso`
 - `sso_secret`: some secure key

Save, now set `DISCOURSE_SSO_SECRET` in your auth project's settings file to the secure key you just put in Discourse.

Finally run migrations and restart gunicorn and celery.
