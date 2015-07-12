#! /usr/bin/env python
import gspread
import argparse
import sys
import pdb
import json
from oauth2client.client import SignedJwtAssertionCredentials

def openSS(key, title):
  json_key = json.load(open(key))                                                                                                                        
  scope = ['https://spreadsheets.google.com/feeds']                                                                                                           
  credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)                                                       
  gc = gspread.authorize(credentials)                                                                                                                         
  return gc.open(title)


def isRectangular(tbl):
	return len(set([len(x) for x in tbl])) == 1

def getRange(ws, startRow, startCol, endRow, endCol):
  return ws.get_addr_int(startRow, startCol) + ':' + ws.get_addr_int(endRow, endCol) 

def putTblRowMajorFast(ws, start_row, start_col, tbl):
	assert isRectangular(tbl)
	rows = len(tbl)
	cols = len(tbl[0])
	end_row = start_row + rows - 1
	end_col = start_col + cols - 1
	rng = getRange(ws, start_row, start_col, end_row, end_col)

	sys.stderr.write("Uploading {0}x{1} table in range {2}...".format(rows, cols, rng))
	cell_list = ws.range(rng)

	# cell_list is in row major order. Build the value list in the same order
	values = []
	for row in xrange(0, len(tbl)):
		for col in xrange(0, len(tbl[row])):
			cell_list[row * cols + col].value = tbl[row][col]

	ws.update_cells(cell_list)
	sys.stderr.write("Done\n")

class Table:
  def __init__(self, row, col, rowNames, colNames, ws):
    self._row = row
    self._col = col
    self._rowNames = rowNames
    self._colNames = colNames
    self._rowInd = dict(zip(rowNames, range(0, len(rowNames))))
    self._colInd = dict(zip(colNames, range(0, len(colNames))))
    self._ws = ws
    self._contents = None

  def put(self):
    header = [ '' ] + self._colNames
    prepRows = [ [ x[0] ] + x[1] for x in zip(self._rowNames, self._contents)]
    try:
      putTblRowMajorFast(self._ws, self._row, self._col, [ header ] + prepRows)
    except gspread.httpsession.HTTPError as e:
      print e
      print e.code
      print e.message
      print e.response
      pdb.set_trace()
      raise e

  def cellLbl(self, rowName, colName):
    return self._ws.get_addr_int(self._row + self._rowInd[rowName] + 1, self._col + 1 + self._colInd[colName])

  def height(self):   return len(self._rowNames) + 1
  def width(self):   return len(self._colNames) + 1
  def setContents(self, c):   self._contents = c
  def colNames(self):   return self._colInd.keys()
  def rowNames(self):   return self._rowInd.keys()

