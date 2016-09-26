*********************
Full Automated Nagios
*********************

.. image:: https://img.shields.io/pypi/pyversions/Django.svg

Python script to install/configure Nagios server and Nrpe agents to all client servers.

============
Installation
============


So you can easily download it:

.. code-block:: bash

    # git clone https://github.com/jamalshahverdiev/full-automated-nagios.git
    # cd full-automated-nagios

Firstly we must install and configure Python2.7 or Python3.4 with needed libraries:

.. code-block:: bash
    
    # ./python-installer.sh


Program components are the following:

* clients.txt - This file must contain IP adress list of NRPE agents.
* nagios-clients.py - Program will install and configure NRPE agents.
* nagios-server.py - Program will install and configure Nagios server.
* run.py - Program give us menu to select install/configure Nagios or NRPE sevrer.



=====
Usage
=====

The purpose of this article is to show how to automatically install the Nagios server and the NRPE clients using the prearranged python scripts. First of all, you must activate root access on all hosts (server and clients).

After you have activated the root access and performed the system update on all machines, you must perform one additional step on FreeBSD. Install bash and copy the shell executable from /usr/local/bin/bash to /bin/bash.


In a terminal:

.. code-block:: bash
    
    # pkg install -y bash vim
    # cp /usr/local/bin/bash /bin/bash 
    # chsh -s /usr/local/bin/bash root ; reboot


.. code-block:: bash

    $ pyspeedtest
    Using server: speedtest.serv.pt
    Ping: 9 ms
    Download speed: 148.17 Mbps
    Upload speed: 18.56 Mbps

From a python script:

.. code-block:: python

    >>> import pyspeedtest
    >>> st = pyspeedtest.SpeedTest()
    >>> st.ping()
    9.306252002716064
    >>> st.download()
    42762976.92544772
    >>> st.upload()
    19425388.307319913
