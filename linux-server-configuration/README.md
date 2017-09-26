# Linux Server Configuration Project Submission
This README describes the submission of Linux Server Configuration project from FSND.

## IP address & URL
- IP address: 54.250.252.165
- URL: ec2-54-250-252-165.ap-northeast-1.compute.amazonaws.com

## Installed software
- emacs
- ntp
- apache2
- libapache2-mod-wsgi
- postgresql
- pip
- python-dev
- Flask
- flask_httpauth
- sqlalchemy
- oauth2client
- requests
- psycopg2

## Configurations
### SSH login as ubuntu from the local machine
We can login Amazon Lightsail's machine only by the browser-based terminal window.
So we need to be able to login it from our local machines.

1. Generate ssh key pair for the user `ubuntu` on the client
    - `cd ~/.ssh`
    - `ssh-keygen`
        - I name the key pair "item-catalog-ubuntu"
2. Copy the content of item-catalog-ubuntu.pub file
    - `cat ~/.ssh/item-catalog-ubuntu.pub`
3. Paste it in authorized_keys on the Amazon Lightsail machine
    - `vi ~/.ssh/authorized_keys`
4. Test we can login the remote machine by ssh from our local machines
    - `ssh ubuntu@54.250.252.165 -p 22 -i ~/.ssh/item-catalog-ubuntu`

### Firewall Configuration
The machine seems to have two firewalls, the firewall controlled on the Lightsail's console page, and ufw.

#### Amazon Lightsail's firewall
Open 123 for ntp and 2200 for ssh.
Remain 22 open temporarily so as to keep ssh connections through 22.
The table is modified like the following:

| Application | Protocol | Port range|
|:--|:--|:--|
| SSH | TCP | 22 |
| HTTP | TCP | 80 |
| Custom | TCP | 123 |
| Custom | TCP | 2200 |

#### ufw
Open 22, 80, 123, 2200.

1. Check the firewall is disabled
    - `sudo ufw status`
2. Deny all incoming data and allow all outgoing data by default
    - `sudo ufw default deny incoming`
    - `sudo ufw default allow outgoing`
3. Allow ssh to use the port 22 temporarily
    - `sudo ufw allow ssh`
4. Allow http to use the port 80
    - `sudo ufw allow www`
5. Allow ntp to use the port 123
    - `sudo ufw allow ntp`
6. Allow ssh to use the port 2200
    - `sudo ufw allow 2200/tcp`
7. Enable the firewall
    - `sudo ufw enable`
    - If the configuration is correct, ssh connection is not broken
8. Check the firewall is configured properly
    - `sudo ufw status`
        - Confirm that only 22, 80, 123, 2200 are open

#### sshd
Modify sshd configuration so that sshd observes the port 2200.

1. Modify `Port 22` to `Port 2200` in sshd_config file
    - `sudo vi /etc/ssh/sshd_config`
2. Restart sshd
    - `sudo service sshd restart`
    - The ssh connection will be broken
3. Confirm you cannot login by the old port 22
    - `ssh ubuntu@54.250.252.165 -p 22 -i ~/.ssh/item-catalog-ubuntu`
3. Re-login by new port 2200
    - `ssh ubuntu@54.250.252.165 -p 2200 -i ~/.ssh/item-catalog-ubuntu`

#### Close port 22
1. Let ufw deny port 22
    - `sudo ufw deny ssh`
2. Reload ufw configuration
    - `sudo ufw reload`
3. Check port 22 is successfully denied
    - `sudo ufw status`
4. Remove ssh/22 from the firefall on Lightsail's console page
    - After that, the table should look like the following:

| Application | Protocol | Port range|
|:--|:--|:--|
| HTTP | TCP | 80 |
| Custom | TCP | 123 |
| Custom | TCP | 2200 |


### Install software
1. Upgrade all pre-installed software
    - `sudo apt-get update && sudo apt-get upgrade`
2. Install emacs
    - `sudo apt-get install emacs`
3. Install ntp
    - `sudo apt-get install ntp`
4. Check ntp works properly
    - `sudo ntpq -p`
5. Remove software not required anymore
    - `sudo apt-get autoremove`


### User authentication
#### Disable password-based login
- Change `PasswordAuthentication` to `no`
    - `sudo emacs /etc/ssh/sshd_config`
    - `sudo service ssh restart`


#### Disable remote login of the user `root`
- Change `PermitRootLogin` to `no`
    - `sudo emacs /etc/ssh/sshd_config`
    - `sudo service ssh restart`

This configuration disables login as `root` regardless whether it's remote or local login.
We don't have to care about local login to the machine because we cannot do it for cloud instances.


#### Create new user `grader`
1. Create new user "grader"
    - `sudo adduser grader`
2. Give the user "grader" sudo access
    - `sudo emacs /etc/sudoers.d/grader`
        - The content: `grader ALL=(ALL) NOPASSWD:ALL`
3. Generate ssh key pair for `grader` **on the client-side**
    - `cd ~/.ssh`
    - `ssh-keygen`
        - I named key pair "item-catalog-grader"
4. Pass the server the generated public key
    - `su - grader`
    - `mkdir ~/.ssh`
    - `touch ~/.ssh/authorized_keys`
    - `cat ~/.ssh/item-catalog-grader.pub` **on the client-side**
        - Copy the content of pub file
    - `emacs ~/.ssh/authorized_keys`
        - Paste the pub's content above
    - `chmod 700 ~/.ssh`
    - `chmod 600 ~/.ssh/authorized_keys`
5. Test you can login as `grader` by ssh **on the client-side**.
    - `ssh grader@54.250.252.165 -p 2200 -i ~/.ssh/item-catalog-grader`

NOTE: A the last step, I had to add `-o IdentitiesOnly=yes` to ssh command, otherwise the attempt always failed:
```sh
$ ssh grader@54.250.252.165 -p 2200 -i ~/.ssh/item-catalog-grader     
Received disconnect from 54.250.252.165 port 2200:2: Too many authentication failures
Authentication failed.
```

However, after logging in with `-o IdentitiesOnly=yes` once, I can login without it.
```sh
$ ssh grader@54.250.252.165 -p 2200 -i ~/.ssh/item-catalog-grader -o IdentitiesOnly=yes
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-1035-aws x86_64)
...
grader@ip-172-26-7-35:~$ exit
logout
Connection to 54.250.252.165 closed.
$ ssh grader@54.250.252.165 -p 2200 -i ~/.ssh/item-catalog-grader  # I can login without the option!   
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-1035-aws x86_64)
...
```

I couldn't find the reason, but guess something related to ssh is cached.


### Add Google OAuth origin
1. Add the URL `http://ec2-54-250-252-165.ap-northeast-1.compute.amazonaws.com/` besides `localhost:5000`
2. Download new client_secrets.json and replace the old one


### Create environment for Flask app
1. Put Item Catalog app under `/var/www`
    - `cd /var/www/`
    - `sudo mkdir catalog`
    - `cd catalog/`
    - `sudo git clone https://github.com/k-mats/fullstack-nanodegree-vm.git`
    - `sudo mv fullstack-nanodegree-vm/vagrant/catalog .`
    - `sudo rm -rf fullstack-nanodegree-vm/`
2. Install Flask in virtual environment by pip
    - `cd catalog/`
    - `sudo apt-get install python-pip`
    - `sudo pip install virtualenv`
    - `sudo virtualenv venv`
    - `source venv/bin/activate`
    - `sudo pip install Flask flask_httpauth sqlalchemy oauth2client requests psycopg2`


### Add Posgresql user and DB for the Item Catalog app
Apache process controls Postgres as the user `www-data`.
Thus we need to create one under the following permissions:

- It cannot create new DB: `-D` option
- It cannot create new roles: `-R` option
- It cannot be the super user: `-S` option
- It should have the ownership of Item Catalog app's DB

So we create the user `www-data` like that:

1. Change the user to `postgres`
    - `sudo su - postgres`
2. Create the user `www-data`
    - `createuser -DRS www-data`
3. Create DB `catalog`
    - `psql -c 'create database catalog;'`
4. Load dummy data to DB
    - `cd /var/www/catalog/catalog`
    - `make reload`
5. Change DB and tables' ownership to `www-data`
    - `psql`
    - `alter database catalog owner to "www-data";`
    - `\c catalog`
    - `alter table category owner to "www-data";`
    - `alter table item owner to "www-data";`
    - `alter table "user" owner to "www-data";`


### Apache and wsgi
1. Install Apache
    - `sudo apt-get install apache2`
    - Access to http://54.250.252.165/ and check if it works
2. Set up Apache config for Item Catalog app
    - `sudo emacs /etc/apache2/sites-available/catalog.conf`
```xml
<VirtualHost *:80>
        ServerName ec2-54-250-252-165.ap-northeast-1.compute.amazonaws.com
        ServerAdmin gfeenhaftsylphid@gmail.com
        WSGIScriptAlias / /var/www/catalog/catalog.wsgi
        <Directory /var/www/catalog/catalog/>
                Order allow,deny
                Allow from all
        </Directory>
        Alias /static /var/www/catalog/catalog/static
        <Directory /var/www/catalog/catalog/static/>
                Order allow,deny
                Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
3. Enable the virtual host
    - `sudo a2ensite catalog`
4. Add __init__.py
    - `sudo touch __init__.py`
5. Install mod_wsgi
    - `sudo apt-get install libapache2-mod-wsgi python-dev`
    - `sudo a2enmod wsgi`
6. Create the wsgi file
    - `cd /var/www/catalog`
    - `sudo emacs catalog.wsgi`
```python
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/")
from catalog.application import app as application
application.secret_key = 'some_secret_key'
```
7. Restart Apache
    - `sudo service apache2 restart`
8. Done! Access to ec2-54-250-252-165.ap-northeast-1.compute.amazonaws.com and confirm it works


## Third-party references
- [How to configure UFW to allow ntp to work?](https://askubuntu.com/questions/709843/how-to-configure-ufw-to-allow-ntp-to-work)
- [Time Synchronisation with NTP](https://help.ubuntu.com/lts/serverguide/NTP.html)
- [How To Deploy a Flask Application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
- [mod_wsgi (Apache)](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/)
- [Engine Configuration¶](http://docs.sqlalchemy.org/en/latest/core/engines.html)
- [PostgreSQL](http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2)
