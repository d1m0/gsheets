import argparse
import sys
from gsheet import openSS, putTblRowMajorFast

if __name__ == '__main__':
  p = argparse.ArgumentParser(description=\
    "input a column/table read from stdin or a file");
  p.add_argument('--key', type=str, help='path to key-file used as authentication')
  p.add_argument('--title', type=str, help='Title of an existing spreadsheet in which to work')
  p.add_argument('--sheet', type=str, default='sheet1', help='Existing worksheet within the spreadsheet in which to place data')
  p.add_argument('input', type=str, help='File with the inputs (specify - to use stdin)')
  p.add_argument('--delimiter', type=str, default=',', help='Single character that separates columns')
  p.add_argument('--row', type=int, default=1, help='Row where to start inserting')
  p.add_argument('--col', type=int, default=1, help='Column where to start inserting')

  args = p.parse_args()

  inp = open(args.input) if args.input != '-' else sys.stdin

  tbl = []
  for l in inp:
    tbl.append(l.split(args.delimiter))

  ss = openSS(args.key, args.title);
  ws = ss.worksheet(args.sheet);

  putTblRowMajorFast(ws, args.row, args.col, tbl)
