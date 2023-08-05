#
# Copyright (c) 2018 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import unicode_literals

import ctypes
import ctypes.util
import distro
import os
import platform

from plugincode.location_provider import LocationProviderPlugin


# Modified from https://stackoverflow.com/questions/22579308/getting-the-fullpath-of-a-library-using-ctypes-util-find-library-in-python
class dl_phdr_info(ctypes.Structure):
    _fields_ = [
        ('padding0', ctypes.c_void_p),
        ('dlpi_name', ctypes.c_char_p),
    ]


callback_t = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.POINTER(dl_phdr_info),
    ctypes.POINTER(ctypes.c_size_t),
    ctypes.c_char_p
)
# Load library, set argument value types and return value type
dl_iterate_phdr = ctypes.CDLL('libc.so.6').dl_iterate_phdr
dl_iterate_phdr.argtypes = [callback_t, ctypes.c_char_p]
dl_iterate_phdr.restype = ctypes.c_char_p


class CallbackWrapper(object):
    """
    This class is a "wrapper" for the callback function from the answer to
    https://stackoverflow.com/questions/22579308/getting-the-fullpath-of-a-library-using-ctypes-util-find-library-in-python

    The callback method is placed in this class so we can save the .so path from
    the function call to dl_iterate_phdr into our class attribute `dll_path`
    """
    def __init__(self):
        self.dll_path = ''

    def callback(self, info, size, data):
        if data in info.contents.dlpi_name:
            self.dll_path = info.contents.dlpi_name
        return 0


class LibmagicPaths(LocationProviderPlugin):
    def get_locations(self):
        """
        Return a mapping of {location key: location} providing the installation
        locations of the libmagic shared library as installed on various Linux
        distros or on FreeBSD.
        """
        system_arch = platform.machine()
        mainstream_system = platform.system().lower()
        if mainstream_system == 'linux':
            distribution = distro.linux_distribution()[0].lower()
            debian_based_distro = ['ubuntu', 'mint', 'debian']
            rpm_based_distro = ['fedora', 'redhat', 'centos linux']

            if distribution in debian_based_distro:
                data_dir = '/usr/lib/file'
                lib_dir = '/usr/lib/'+system_arch+'-linux-gnu'
            elif distribution in rpm_based_distro:
                data_dir = '/usr/share/misc'
                lib_dir = '/usr/lib64'
            else:
                raise Exception('Unsupported system: {}'.format(distribution))

            lib_dll = os.path.join(lib_dir, 'libmagic.so.1.0.0')

        elif mainstream_system == 'freebsd':
            if os.path.isdir('/usr/local/'):
                lib_dir = '/usr/local'
            else:
                lib_dir = '/usr'
            lib_dll = os.path.join(lib_dir, 'lib/libmagic.so')
            data_dir = os.path.join(lib_dir,'share/file')

        else:
            raise Exception('Unsupported system: {}'.format(mainstream_system))

        if not os.path.exists(lib_dll):
            lib_dll = ctypes.util.find_library('magic')
            if not lib_dll:
                raise Exception('libmagic.so was not found on the system')
            # Load library
            _ = ctypes.CDLL(lib_dll)
            # Find loaded library
            c = CallbackWrapper()
            _ = dl_iterate_phdr(callback_t(c.callback), bytes(lib_dll.encode('utf-8')))
            lib_dll = c.dll_path

        magic_mgc_path = os.path.join(data_dir, 'magic.mgc')
        if not os.path.exists(magic_mgc_path):
            raise Exception('magic.mgc was not found on the system')

        return {
            'typecode.libmagic.libdir': lib_dir,
            'typecode.libmagic.dll': lib_dll,
            'typecode.libmagic.db': magic_mgc_path,
        }
