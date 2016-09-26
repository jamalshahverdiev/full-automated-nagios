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
.. code-block:: bash
    fpyvenv fully-automated-nagios # ll
    -rw-r--r--  1 root  wheel    14B Sep 25 14:41 clients.txt
    drwxr-xr-x  2 root  wheel   512B Sep 24 21:48 jinja2temps
    -rwxr-xr-x  1 root  wheel   5.7K Sep 25 09:28 nagios-clients.py
    -rwxr-xr-x  1 root  wheel   3.9K Sep 25 01:15 nagios-server.py
    drwxr-xr-x  2 root  wheel   512B Sep 24 21:46 ngclout
    drwxr-xr-x  2 root  wheel   512B Sep 24 21:09 output
    -rwxr-xr-x  1 root  wheel   2.9K Sep 25 09:30 python-installer.sh
    -rwxr-xr-x  1 root  wheel   1.7K Sep 25 09:27 run.py
    -rwxr-xr-x  1 root  wheel   1.7K Sep 25 09:27 README.rst

clients.txt - This file must contain IP adress list of NRPE agents.
nagios-clients.py - Program will install and configure NRPE agents.
nagios-server.py - Program will install and configure Nagios server.
run.py - Program give us menu to select install/configure Nagios or NRPE sevrer.



=====
Usage
=====

In a terminal:

.. code-block:: bash

    $ pyspeedtest -h
    usage: pyspeedtest [OPTION]...

    Test your bandwidth speed using Speedtest.net servers.

    optional arguments:
      -d L, --debug L   set http connection debug level (default is 0)
      -m M, --mode M    test mode: 1 - download
                                   2 - upload
                                   4 - ping
                                   1 + 2 + 4 = 7 - all (default)
      -r N, --runs N    use N runs (default is 2)
      -s H, --server H  use specific server
      -v, --verbose     output additional information
      --version         show program's version number and exit

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
