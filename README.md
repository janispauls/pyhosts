[![Build Status](https://travis-ci.org/janispauls/pyhosts.svg?branch=master)](https://travis-ci.org/janispauls/pyhosts)

pyhosts
=======

Python library for managing hosts file (eg. /etc/hosts) in Pythonic way:
- Is platform independent
- Uses Python objects to manage hosts entries 

Examples
========

    >>> from pyhosts import Hosts
    >>> myhosts = Hosts()
    >>> [entry for entry in myhosts]
    [{'ipaddress': IPAddress('127.0.0.1'),       'hostname': 'localhost',               'aliases': ['localhost.localdomain'], 'comments': None},
     {'ipaddress': IPAddress('::1'),             'hostname': 'localhost6.localdomain6', 'aliases': ['localhost6'],            'comments': None},
     {'ipaddress': IPAddress('172.19.29.156'),   'hostname': 'igor',                    'aliases': None,                        'comments': None},
     {'ipaddress': IPAddress('192.168.122.167'), 'hostname': 'marev3',                  'aliases': None,                        'comments': "marev3"}]
     
    >>> myhosts.igor.ipaddress 
    IPAddress('172.19.29.156')
    
    >>> myhosts.hostname.igor4.ipadress 
    ValueError: No such host entry in this hosts object.

Contribute
==========

- python setup.py test to run tests

Random notes
============

- http://en.wikipedia.org/wiki/Hosts_(file)
- http://unixhelp.ed.ac.uk/CGI/man-cgi?hosts 
- Windows hosts file: http://support.isoc.net/Page.aspx/117/hosts.html
