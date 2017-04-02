#!/usr/bin/env python2.7
import os
from termcolor import colored, cprint
import jinja2

codepath = os.getcwd()
outputdir = codepath+'/output/'
ngcloutput = codepath+'/ngclout/'
tempdir = codepath+'/jinja2temps/'
templateLoader = jinja2.FileSystemLoader( searchpath=tempdir )
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPNRPE = 'nrpetemp.cfg'
TEMPNAGIOSCLIENT = 'nagiosclient.cfg'
tempnrpe = templateEnv.get_template( TEMPNRPE )
tempnagclient = templateEnv.get_template( TEMPNAGIOSCLIENT )

ipadd = colored('IP address', 'green', attrs=['bold', 'underline'])
username = colored('username', 'green', attrs=['bold', 'underline'])
password = colored('password', 'magenta', attrs=['bold', 'underline'])
successfully = colored('successfully', 'green', attrs=['bold', 'underline'])
centos = colored('CentOS', 'yellow', attrs=['bold', 'underline'])
freebsd = colored('FreeBSD', 'yellow', attrs=['bold', 'underline'])
ubuntu = colored('Ubuntu', 'yellow', attrs=['bold', 'underline'])
nrpe = colored('Nrpe', 'yellow', attrs=['bold', 'underline'])
nagios = colored('Nagios', 'yellow', attrs=['bold', 'underline'])
enter = colored('Enter', 'cyan', attrs=['bold', 'underline'])
nserver = colored('server', 'cyan', attrs=['bold', 'underline'])

cosnrpepidfile = "/var/run/nrpe/nrpe.pid"
ubnrpepidfile = "/var/run/nagios/nrpe.pid"
bsdnrpepidfile = "/var/run/nrpe2/nrpe2.pid"
cosnrpeuser = "nrpe"
bsdandubnrpeuser = "nagios"
cosnrpecompath = "/usr/lib64/nagios/plugins/"
ubnrpecompath = "/usr/lib/nagios/plugins/"
bsdnrpecompath = "/usr/local/libexec/nagios/"
cosincludedir = "/etc/nrpe.d/"
ubincludedir = "/etc/nagios/nrpe.d/"
bsdincudedir = "/usr/local/etc/nrpe.d/"

