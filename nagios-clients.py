#!/usr/bin/env python2.7
import os, time
import getpass
import sys
from fabric.api import *
sys.path.insert(0, './lib')
from nagiossrvclivars import *

print("")
print('   It is supposed that you have already added '+ipadd+' list of client hosts to the '+codepath+'/clients.txt'+' file')
print('   The '+password+' for all '+nagios+' clients and '+nserver+' must be the same!!!')
print("")
env.user = raw_input('  '+enter+' superuser: ')
env.password = getpass.getpass('  '+enter+' '+password+' for superuser: ')
print("==================================================================")
nagiosrvip = raw_input('   '+enter+' '+ipadd+' of '+nagios+' '+nserver+': ')
print("")

def print_func():
    print('   Installation and configuration of '+nrpe+' necessary plugins are in progress...')
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
    run('apt-get update')
    run('apt-get install -y nagios-nrpe-server nagios-plugins')
    put(tempdir+'check_mem', checkmempath)
    disk = run("df -h | grep '/$' | cut -f1 -d' '")
    nrpeconfigurator(ubnrpepidfile, bsdandubnrpeuser, ubnrpecompath, ubincludedir, disk, hostname, ip)
    put(outputdir+'nrpe.cfg', nrpepath)
    run('/etc/init.d/nagios-nrpe-server restart')


def centosnrpe(nrpepath, checkmempath):
    print_func()
    run('yum -y install epel-release')
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
            print(' The remote '+nserver+' identified as '+centos+' 6 !!!')
            centosnrpe('/etc/nagios/', '/usr/lib64/nagios/plugins/')
            run('chmod +x /usr/lib64/nagios/plugins/check_mem')

        elif sysver == "Linux" and lintype == "\S":
            print(' The remote '+nserver+' identified as '+centos+' 7 !!!')
            centosnrpe('/etc/nagios/', '/usr/lib64/nagios/plugins/')
            run('chmod +x /usr/lib64/nagios/plugins/check_mem')

        elif sysver == "Linux" and lintype == "Ubuntu":
            print(' The remote '+nserver+' identified as '+ubuntu+' !!!')
            ubuntunrpe('/etc/nagios/', '/usr/lib/nagios/plugins/')
            run('chmod +x /usr/lib/nagios/plugins/check_mem')

        elif sysver == "FreeBSD":
            print(' The remote '+nserver+' identified as '+freebsd+' !!!')
            freebsdnrpe('/usr/local/etc/', '/usr/local/libexec/nagios/')
            run('chmod +x /usr/local/bin/free /usr/local/libexec/nagios/check_mem')


env.host_string = nagiosrvip
with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
    put(ngcloutput+'*.cfg', '/etc/nagios3/conf.d/')
    run('/etc/init.d/nagios3 restart')
