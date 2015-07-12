#! /usr/bin/env python
"""
gsheet
~~~~~~~

Convenience wrapper around gspread. Adds a "table" class that allows to reffer to
other cells within a "table" without fixing the location where the table will be
placed.

"""

__version__ = '0.1'
__author__ = 'Dimitar Bounov'

from .gsheets import openSS, Table, putRawTable
