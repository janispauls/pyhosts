import platform

from host import Host


class PlatformNotSupportedException(Exception):
    pass


class DuplicateEntryError(Exception):
    pass


class Hosts(object):
    def __init__(self, file_path=None):
        self._lines = None  # Temp storage for read file lines
        self._hosts = None

        self.file_path = file_path or self._file_path()

    def __str__(self):
        return "Hosts file: %s" % self.file_path

    def __getattr__(self, name):
        for host in self._rows():
            if name == host.hostname:
                return host
            elif name in host.aliases:
                return host
            elif name == str(host.ipaddress):
                return host
            else:
                return None

    def __index__(self):
        self._rows()
        return self._hosts

    def __iter__(self):
        self._rows()
        return self._hosts.__iter__()

    def _file_path(self):
        system_name = platform.system()
        if system_name == "Linux":
            return "/etc/hosts"
        elif system_name == "Windows":
            return r"c:/windows/system32/drivers/etc/hosts"
        elif system_name == "Darwin":
            return "/private/etc/hosts"
        else:
            raise PlatformNotSupportedException

    def _readlines(self, path):
        if not self._lines:
            with open(path, 'r') as f:
                self._lines = f.readlines()
            return self._lines
        else:
            return self._lines

    def _rows(self):
        self._hosts = []
        for row in self._readlines(self.file_path):
            if row.startswith(r'#'):
                continue  # skip comments for now
            if len(row.split()) < 2:
                continue  # skip invalid rows
            ipaddress, hostname, aliases, comments = Hosts._process_row(row)
            host = Host(ipaddress, hostname, aliases, comments)
            self._hosts.append(host)
        return self._hosts

    @staticmethod
    def _process_row(row):
        ipaddress, hostname, aliases, comments = None, None, None, None

        split_row = row.split()
        if len(split_row) == 4:
            ipaddress, hostname, aliases, comments = split_row
        elif len(split_row) == 3:
            ipaddress, hostname, aliases = split_row
            comments = None
        elif len(split_row) == 2:
            ipaddress, hostname = split_row
            aliases, comments = None, None

        return ipaddress, hostname, aliases, comments

    def persist(self, path=None):
        """Persists current hosts collections to path"""
        path = path if path else self.file_path

        with open(path, "w") as hosts_file:
            hosts_file.write("# Written by Pyhosts\n\n")
            hosts_file.writelines([str(i) for i in self])
