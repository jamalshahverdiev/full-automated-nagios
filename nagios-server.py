#!/usr/bin/env python2.7
import os
import getpass
import sys
sys.path.insert(0, './lib')
from nagiossrvclivars import *
from fabric.api import *

print("")
print(' Please '+enter+' the following parameters to proceed to the installation of '+nagios+' '+nserver+'.')
env.host_string = raw_input('  '+ipadd+': ')
env.user = raw_input("  Name of superuser: ")
env.password = getpass.getpass('  Superuser '+password+': ')

def dbcreds():
    global dbpasswd
    dbpasswd = getpass.getpass('  '+enter+' '+password+' for mysql "root" user: ')
    global dbpasswd1
    dbpasswd1 = getpass.getpass('  Repeat '+password+' for mysql "root" user: ')
    print("")
    while dbpasswd != dbpasswd1:
        print("")
        print(' Entered passwords must be the same. '+enter+' passwords again. ')
        dbpasswd = getpass.getpass('  '+enter+' '+password+' for mysql "root" user: ')
        dbpasswd1 = getpass.getpass('  Repeat '+password+' for mysql "root" user: ')
        if dbpasswd == dbpasswd1:
            print("")
            print(' The '+password+' set '+successfully+'!')
            break
        print(' Entered passwords must be the same. '+enter+' passwords again. ')


def nagioscreds():
    global nagiosadminpass
    nagiosadminpass = getpass.getpass('  '+enter+' '+password+' for "nagiosadmin" user: ')
    global nagiosadminpass1
    nagiosadminpass1 = getpass.getpass('  Repeat '+password+' for "nagiosadmin" user: ')
    print("")
    while nagiosadminpass != nagiosadminpass1:
        print("")
        print(' Entered passwords must be the same. '+enter+' passwords again. ')
        nagiosadminpass = getpass.getpass('  '+enter+' '+password+' for "nagiosadmin" user: ')
        nagiosadminpass1 = getpass.getpass('  Repeat '+password+' for "nagiosadmin" user: ')
        if nagiosadminpass == nagiosadminpass1:
            print("")
            print(' The '+password+' set '+successfully+'!')
            break
        print(' Entered passwords must be the same. '+enter+' passwords again. ')


if env.user != "root":
    print("")
    print("  The entered user is not 'root'. ")
    print("  Sorry, this script is support only 'root' user as superuser. ")
    print("  Please open 'root' user authentication over SSH. ")
    sys.exit()
else:
    pass


with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
    sysver = run('uname -s')
    lintype = run("cat /etc/issue | head -1 | cut -f1 -d' '")

    if sysver == "Linux" and lintype == "Ubuntu":
        print('  The remote '+nserver+' identified as '+ubuntu+'...')
        print("")
        print(" Please wait while installing 'Apache2'...")
        run('apt-get update && apt-get install -y apache2')
        print("")
        print("Please provide passwords for MySQL 'root' user and 'nagiosadmin' web user:")
        dbcreds()
        run('debconf-set-selections <<< "mysql-server mysql-server/root_password password '+dbpasswd+'"')
        run('debconf-set-selections <<< "mysql-server mysql-server/root_password_again password '+dbpasswd+'"')
        nagioscreds()
        run('debconf-set-selections <<< "postfix postfix/main_mailer_type select No configuration"')
        run('debconf-set-selections <<< "nagios3-cgi nagios3/adminpassword password '+nagiosadminpass+'"')
        run('debconf-set-selections <<< "nagios3-cgi nagios3/adminpassword-repeat password '+nagiosadminpass+'"') 
        print(" Please wait while installing 'MySQL'...")
        run('apt-get install -y mysql-server mysql-client')
        run('apt-get install -y php5 php5-mysql libapache2-mod-php5')
        print("")
        print(' Installation of '+nagios+' '+nserver+' and plugins is in progress...')
        run('apt-get install -y nagios3 nagios-nrpe-plugin')
        run('usermod -a -G nagios www-data ; chmod -R +x /var/lib/nagios3/')
        put(tempdir+'nagios-server.cfg', '/etc/nagios3/nagios.cfg')
        run('/etc/init.d/nagios3 restart')
        run('service apache2 restart')
        print(''+nagios+' '+nserver+' '+successfully+' installed and configured!!!')
        print('  http://'+env.host_string+'/nagios3/ - username: "nagiosadmin"...')

