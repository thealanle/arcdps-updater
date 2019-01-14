#!/usr/bin/env python3

import requests
import os
import hashlib
import time


def download_file(url, filename):
    """
    Download the target file and save it to the current directory
    """
    target = url + filename

    with open(filename, 'wb') as f:
        f.write(requests.get(target).content)


def get_md5(url, filename):
    """
    Download the md5sum file and return the md5 value
    """
    download_file(url, filename)
    result = ''
    with open(filename) as f:
        result = f.readline().split()[0]

    return result


def checksum(filename):
    """
    Given a file, return its md5 hash
    """
    m = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            buf = f.read(128)
            if not buf:
                break
            m.update(buf)

    return m.hexdigest()


def main():
    """
    1) Check if d3d9.dll exists locally
    2) Check if md5sum of d3d9.dll matches online md5sum
    3) If d3d9.dll is not present or if local md5sum does not match,
       download online d3d9.dll
    4) Verify md5sum
    """

    url = 'https://www.deltaconnected.com/arcdps/x64/'
    d3d9 = 'd3d9.dll'
    md5file = 'd3d9.dll.md5sum'
    cwd = os.listdir()

    md5 = get_md5(url, md5file)

    if 'd3d9.dll' in cwd and checksum(d3d9) == md5:
        print("d3d9.dll is up to date.\n")
    else:
        print("d3d9.dll is out of date.")
        download_file(url, d3d9)
        if checksum(d3d9) == md5:
            print("d3d9.dll successfully updated.\n")
        else:
            print("d3d9.dll was updated, but md5 comparison failed.\n")

    if 'd3d9_arcdps_buildtemplates.dll' in cwd:
        print("Build templates detected.")
        download_file(url + 'buildtemplates/',
                      'd3d9_arcdps_buildtemplates.dll')
        print("d3d9_arcdps_buildtemplates.dll successfully updated.\n")

    if 'd3d9_arcdps_extras.dll' in cwd:
        print("arcdps extras detected.")
        download_file(url + 'extras/',
                      'd3d9_arcdps_extras.dll')
        print("d3d9_arcdps_extras.dll successfully updated.\n")


if __name__ == '__main__':
    main()
