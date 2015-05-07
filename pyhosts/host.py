from netaddr import IPAddress


class Host(object):
    def __init__(self, ipaddress, hostname, aliases, comments):
        self.ipaddress = Host._ipaddress(ipaddress)
        self.hostname = hostname
        self.aliases = aliases.split() if aliases else None
        self.comments = comments

    @staticmethod
    def _ipaddress(ipaddress):
        return IPAddress(ipaddress)

    def __repr__(self):
        return str({'ipaddress': self.ipaddress,
                    'hostname': self.hostname,
                    'aliases': self.aliases,
                    'comments': self.comments})

    def _str_aliases(self, aliases):
        return " ".join(self.aliases) if self.aliases else ""

    def _str_comments(self, comments):
        return self.comments if self.comments else ""

    def __str__(self):
        return self._format_line()

    def _format_line(self):
        line = "{ipaddress}\t{hostname}\t{aliases}\t{comments}".\
            format(ipaddress=self.ipaddress,
                   hostname=self.hostname,
                   aliases=self._str_aliases(self.aliases),
                   comments=self._str_comments(self.comments))
        line = line.strip() + "\n"
        return line

    def __bool__(self):
        if not self.ipaddress and \
                not self.hostname and \
                not self.aliases and \
                not self.comments:
            return False
        return True

    __nonzero__ = __bool__

    def __eq__(self, host):
        return (self.ipaddress == host.ipaddress and
                self.hostname == host.hostname and
                self.aliases == host.aliases)
