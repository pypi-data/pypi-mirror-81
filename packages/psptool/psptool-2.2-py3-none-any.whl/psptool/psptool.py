# PSPTool - Display, extract and manipulate PSP firmware inside UEFI images
# Copyright (C) 2019 Christian Werling, Robert Buhren
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from prettytable import PrettyTable
import json

from .entry import HeaderEntry
from .blob import Blob
from .utils import print_warning


class PSPTool:
    @classmethod
    def from_file(cls, filename, verbose=False):
        with open(filename, 'rb') as f:
            rom_bytes = bytearray(f.read())

        pt = PSPTool(rom_bytes, verbose=verbose)
        pt.filename = filename

        return pt

    def __init__(self, rom_bytes, verbose=False):
        self.print_warning = print_warning if verbose else lambda *args, **kwargs: None

        self.blob = Blob(rom_bytes, len(rom_bytes), self)
        self.filename = None

    def __repr__(self):
        if self.filename is not None:
            return f'PSPTool(filename={self.filename})'
        else:
            return f'PSPTool(len(rom_bytes)={self.blob.buffer_size}'

    def to_file(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.blob.get_buffer())

    def ls(self, verbose=False):
        for fet in self.blob.fets:
            for index, directory in enumerate(fet.directories):
                t = PrettyTable(['Directory', 'Addr', 'Type', 'Magic', 'Secondary Directory'])
                t.add_row([
                    index,
                    hex(directory.get_address()),
                    directory.type,
                    directory.magic.decode('utf-8', 'backslashreplace'),
                    hex(directory.secondary_directory_address) if directory.secondary_directory_address else '--'
                ])

                print(t)

                self.ls_dir(fet, index, verbose=verbose)
                print('\n')

    def ls_dir(self, fet,  directory_index, verbose=False):
        directory = fet.directories[directory_index]
        self.ls_entries(entries=directory.entries, verbose=verbose)

    def ls_entries(self, entries=None, verbose=False):
        # list all entries of all directories by default (sorted by their address)
        if entries is None:
            entries = sorted(self.blob.unique_entries)

        basic_fields = [' ', 'Entry', 'Address', 'Size', 'Type', 'Magic/ID', 'Version', 'Info']
        verbose_fields = ['MD5', 'size_signed', 'size_full', 'size_packed']

        t = PrettyTable(basic_fields + verbose_fields)
        t.align = 'r'

        for index, entry in enumerate(entries):
            info = []
            if entry.compressed:
                info.append('compressed')
            if entry.signed:
                info.append('signed(%s)' % entry.get_readable_signed_by())
                if entry.verify_signature():
                    info.append('verified')
            if entry.is_legacy:
                info.append('legacy Header')
            if entry.encrypted:
                info.append('encrypted')

            all_values = [
                '',
                index,
                hex(entry.get_address()),
                hex(entry.buffer_size),
                entry.get_readable_type(),
                entry.get_readable_magic(),
                entry.get_readable_version(),
                ', '.join(info),
                entry.md5()[:4].upper()
            ]

            if type(entry) is HeaderEntry:
                all_values += [hex(v) for v in [
                    entry.size_signed,
                    entry.size_uncompressed,
                    entry.rom_size
                ]]
            else:
                all_values += (3 * [''])

            t.add_row(all_values)

        fields = basic_fields

        if verbose is True:
            fields += verbose_fields

        print(t.get_string(fields=fields))

    def ls_json(self, verbose=False):
        data = []
        for fet in self.blob.fets:
            for index, directory in enumerate(fet.directories):
                t = PrettyTable(['Directory', 'Addr', 'Type', 'Magic', 'Secondary Directory'])
                d = {
                    'directory': index,
                    'address': directory.get_address(),
                    'directoryType': directory.type,
                    'magic': directory.magic.decode('utf-8', 'backslashreplace'),
                }
                if directory.secondary_directory_address:
                    d['secondaryAddress'] = directory.secondary_directory_address

                entries = self.ls_dir_dict(fet, index, verbose=verbose)
                d['entries'] = entries
                data.append(d)
        print(json.dumps(data))

    def ls_dir_dict(self, fet,  directory_index, verbose=False):
        directory = fet.directories[directory_index]
        return self.ls_entries_dict(entries=directory.entries, verbose=verbose)

    def ls_entries_dict(self, entries=None, verbose=False):
        # list all entries of all directories by default (sorted by their address)
        if entries is None:
            entries = sorted(self.blob.unique_entries)

        out = []
        for index, entry in enumerate(entries):
            info = []
            if entry.compressed:
                info.append('compressed')
            if entry.signed:
                info.append('signed(%s)' % entry.get_readable_signed_by())
                if entry.verify_signature():
                    info.append('verified')
            if entry.is_legacy:
                info.append('legacy Header')
            if entry.encrypted:
                info.append('encrypted')

            all_values = {
                'index': index,
                'address': entry.get_address(),
                'size': entry.buffer_size,
                'sectionType': entry.get_readable_type(),
                'magic': entry.get_readable_magic(),
                'version': entry.get_readable_version(),
                'info': info,
                'md5': entry.md5()[:4].upper()
            }

            if type(entry) is HeaderEntry:
                sizes = {
                    'signed': entry.size_signed,
                    'uncompressed': entry.size_uncompressed,
                    'packed': entry.rom_size
                }
                all_values['sizes'] = sizes

            out.append(all_values)

        return out
