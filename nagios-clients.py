#!/usr/bin/env python2.7

from fabric.api import *
import os, time
import getpass
import sys
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

print("")
print("   It is supposed that you have already added all IP addresses of client hosts to the  "+codepath+'/clients.txt'+" file")
print("   The password for all Nagios clients and server must be the same!!!")
print("")
env.user = raw_input("  Please enter superuser: ")
env.password = getpass.getpass("  Please enter password for superuser: ")
print("==================================================================")
nagiosrvip = raw_input("   Please enter IP address of Nagios server: ")


def print_func():
    print("   Installation and configuration of 'Nrpe' necessary plugins are in progress...")
    print("")


def nrpeconfigurator(nrpepidarg, nrpeuserarg, commandpatharg, includedirarg, disk, hostname, ipaddress):
    tempnrpeVars = { "nagiossrvip" : nagiosrvip,
            "nrpepidfile" : nrpepidarg,
            "nrpeuser" : nrpeuserarg,
            "commandpath" : commandpatharg,
            "includedir" : includedirarg,
            "disk" : disk,
            "clienthostname" : hostname,
            "clientip" : ipaddress, }

    outputnrpeText = tempnrpe.render( tempnrpeVars )
    outputngclientText = tempnagclient.render( tempnrpeVars )

    with open(outputdir+"nrpe.cfg", "wb") as nrpeout:
        nrpeout.write(outputnrpeText)

    with open(ngcloutput+hostname+".cfg", "wb") as nagclient:
        nagclient.write(outputngclientText)


if env.user != "root":
    print("  The entered user is not 'root'. ")
    print("  Sorry, this script supports only 'root' as superuser. ")
    print("  Please open 'root' user authentication over SSH. ")
    sys.exit()
else:
    pass


def ubuntunrpe(nrpepath, checkmempath):
    print_func()
    run('apt-get install -y nagios-nrpe-server nagios-plugins')
    put(tempdir+'check_mem', checkmempath)
    disk = run("df -h | grep '/$' | cut -f1 -d' '")
    nrpeconfigurator(ubnrpepidfile, bsdandubnrpeuser, ubnrpecompath, ubincludedir, disk, hostname, ip)
    put(outputdir+'nrpe.cfg', nrpepath)
    run('/etc/init.d/nagios-nrpe-server restart')


def centosnrpe(nrpepath, checkmempath):
    print_func()
    run('yum install -y gcc glibc glibc-common gd gd-devel make net-snmp openssl-devel')
    run("yum -y install `yum search nagios-plugins | grep '^nagios-plugins.' | cut -f1 -d' '`")
    put(tempdir+'check_mem', checkmempath)
    disk = run("df -h | grep root | cut -f1 -d' '")
    nrpeconfigurator(cosnrpepidfile, cosnrpeuser, cosnrpecompath, cosincludedir, disk, hostname, ip)
    put(outputdir+'nrpe.cfg', nrpepath)
    run('/etc/init.d/nrpe restart ; chkconfig --level 0123456 nrpe on')
    run('systemctl restart nrpe ; systemctl enable nrpe')


def freebsdnrpe(nrpepath, checkmempath):
    print_func()
    run('pkg install -y nrpe-ssl nagios-plugins')
    run('sysrc nrpe2_enable="YES"')
    run('mkdir /usr/local/etc/nrpe.d')
    disk = run("df -h | grep '/$' | cut -f1 -d' '")
    put(tempdir+'free', '/usr/local/bin/free')
    put(tempdir+'freebsd_check_mem', checkmempath+'check_mem')
    nrpeconfigurator(bsdnrpepidfile, bsdandubnrpeuser, bsdnrpecompath, bsdincudedir, disk, hostname, ip)
    put(outputdir+'nrpe.cfg', nrpepath)
    run('service nrpe2 restart')


with open(codepath+'/clients.txt') as iplist:
    ipler = iplist.readlines()

for ip in ipler:
    env.host_string = ip

    with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
        sysver = run('uname -s')
        lintype = run("cat /etc/issue | head -1 | cut -f1 -d' '")
        hostname = run('hostname')

        if sysver == "Linux" and lintype == "CentOS":
            print(" The remote server identified as CentOS 6 !!!")
            centosnrpe('/etc/nagios/', '/usr/lib64/nagios/plugins/')
            run('chmod +x /usr/lib64/nagios/plugins/check_mem')

        elif sysver == "Linux" and lintype == "\S":
            print("")
            print(" The remote server identified as CentOS 7 !!!")
            centosnrpe('/etc/nagios/', '/usr/lib64/nagios/plugins/')
            run('chmod +x /usr/lib64/nagios/plugins/check_mem')

        elif sysver == "Linux" and lintype == "Ubuntu":
            print("")
            print(" The remote server identified as Ubuntu !!!")
            ubuntunrpe('/etc/nagios/', '/usr/lib/nagios/plugins/')
            run('chmod +x /usr/lib/nagios/plugins/check_mem')

        elif sysver == "FreeBSD":
            print("")
            print(" The remote server identified as FreeBSD !!!")
            freebsdnrpe('/usr/local/etc/', '/usr/local/libexec/nagios/')
            run('chmod +x /usr/local/bin/free /usr/local/libexec/nagios/check_mem')


env.host_string = nagiosrvip
with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
    put(ngcloutput+'*.cfg', '/etc/nagios3/conf.d/')
    run('/etc/init.d/nagios3 restart')
