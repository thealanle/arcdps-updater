#!/usr/bin/env python3

import requests
import os
import hashlib


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
    3) If local md5sum does not match, download online d3d9.dll
    4) Verify md5sum
    """

    url = 'https://www.deltaconnected.com/arcdps/x64/'
    d3d9 = 'd3d9.dll'
    md5file = 'd3d9.dll.md5sum'

    md5 = get_md5(url, md5file)
    d3d9_sum = checksum(d3d9)

    if 'd3d9.dll' in os.listdir() and d3d9_sum == md5:
        print("d3d9.dll is up to date.")
    else:
        print("d3d9.dllis out of date.")
        download_file(url, d3d9)
        d3d9_sum = checksum(d3d9)
        if d3d9_sum == md5:
            print("d3d9.dll successfully updated.")


if __name__ == '__main__':
    main()
