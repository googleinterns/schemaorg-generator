# Copyright 2020 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import os
import core.schema_generator as schema_generator
import urllib.request
import time

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-s',
                   '--SRC',
                   type=str,
                   help='Path to source file')

group.add_argument('-v',
                   '--VER',
                   type=str,
                   help='Schema.org release number')

parser.add_argument('-o',
                    '--OUT',
                    type=str,
                    help='Path to output directory', required=True)

parser.add_argument('-p',
                    '--PKG',
                    type=str,
                    help='Proto package name', required=True)


def main():
    args = parser.parse_args()
    src = args.SRC
    dest = args.OUT
    pkg = args.PKG
    ver = args.VER

    if dest[-1] != '/':
        dest = dest + '/'

    if isinstance(src, str):
        schema = schema_generator.SchemaGenerator(src)
        schema.write_proto(dest, pkg)
    else:
        url = 'https://raw.githubusercontent.com/schemaorg/schemaorg/master/data/releases/' + \
            ver + '/schema.nt'
        name = './temp-' + str(int(time.time())) + '.nt'
        try:
            urllib.request.urlretrieve(url, name)
        except urllib.error.HTTPError:
            print('Invalid release number or check your internet connection.')
        else:
            schema = schema_generator.SchemaGenerator(name)
            schema.write_proto(dest, pkg)
            os.remove(name)


if __name__ == '__main__':
    """Generates protobuf code from a given schema.

    Args:
        -h, --help  Show this help message and exit
        -s, --SRC   Path to source file
        -v, --VER   Schema.org release number
        -o, --OUT   Path to out file
        -p, --PKG   Proto package name
    """
    main()
