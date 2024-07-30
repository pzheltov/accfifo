#!/usr/bin/env python
# -*- coding: utf-8 -*-
from accfifo import cli

def main():
    """
    This needs to be a separate file to avoid circular imports. Do not move.
    """
    try:
        return cli.main()
    except UserWarning as e:
        print(e)


# NB: see entry_points in setup.py
if __name__ == '__main__':
    ret = main()
    print(f'Exiting with {ret} code.')
    exit(ret)
