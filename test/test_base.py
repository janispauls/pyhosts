import unittest

from pyhosts import Hosts, Host

from netaddr import IPAddress


class TestBaseCases(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.myhosts = Hosts()

    def test_content_empty(self):
        self.myhosts._readlines = lambda x: []
        entries = [i for i in self.myhosts]
        expected = []
        self.assertEquals(expected, entries)

    def test_content_one_entry(self):
        self.myhosts._readlines = lambda x: ['127.0.0.1\t\tlocalhost.'
                                             'localdomain localhost\n', ]
        entries = self.myhosts._rows()
        expected = [Host('127.0.0.1', 'localhost.localdomain', 'localhost',
                         None)]
        self.assertEquals(expected, entries)

    def test_content_many_entries(self):
        self.myhosts._readlines = lambda x: ['127.0.0.1\t\tlocalhost.'
                                             'localdomain localhost\n',
                                             '::1\t\tlocalhost6.localdomain6'
                                             ' localhost6\n', '\n',
                                             '172.19.29.156\tigor\n', '\n',
                                             '# virtual machines\n',
                                             '192.168.122.167\tmarev3\n']
        entries = [host for host in self.myhosts]
        expected = [Host('127.0.0.1', 'localhost.localdomain', 'localhost',
                         None),
                    Host('::1', 'localhost6.localdomain6', 'localhost6', None),
                    Host('172.19.29.156', 'igor', None, None),
                    Host('192.168.122.167', 'marev3', None, None)]

        self.assertEquals(expected, entries)

    def test_read_host(self):
        self.myhosts._readlines = lambda x: ['1.1.1.1\tigor', ]
        self.assertEquals(IPAddress('1.1.1.1'), self.myhosts.igor.ipaddress)
        self.assertEquals('igor', self.myhosts.igor.hostname)

    def test_format_same_as_file(self):
        _readlines = ['127.0.0.1\tlocalhost.localdomain\tlocalhost\n',
                      '::1\tlocalhost6.localdomain6\tlocalhost6\n',
                      '172.19.29.156\tigor\n',
                      '192.168.122.167\tmarev3\n']
        self.myhosts._readlines = lambda x: _readlines
        entries = [host for host in self.myhosts]

        for first, second in zip(_readlines, entries):
            self.assertEquals(first, str(second))
