#!/usr/bin/python
"""
Goal: Dump barcodes.
"""
import sqlite3
import os
import sys
import time

OUTPUT_DIR = "data"
SQLITE_FILE = "barcodes.sqlite"

def sqlite_save(barcodes):
    """ Accept a list of barcodes and dump it to an output file.
    """

    # quick and dirty edge case
    if not len(barcodes):
        # skip this if there are no barcodes
        return "No data to save... continue..."


    barcode_tuples = [(x,) for x in barcodes]

    db_file = os.path.join(OUTPUT_DIR, SQLITE_FILE)

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.executemany("INSERT INTO barcode VALUES (?)", barcode_tuples)

    conn.commit()
    conn.close()
    
    return "Save seemed successful."


if __name__ == "__main__":
    """Save barcodes in to sqlite.

    Goal of this module is to provide some good UX doing this.
    """

    print "   * * *"
    print "Please SAVE your work OFTEN, there is no error handling."
    print "   * * *"

    INPUT_STATEMENT = "Type 'save' to save and continue.\nType 'quit' to exit.\nPlease scan the next book:"


    barcodes = list()
    _inputline = "" # sentinel value (no do while in python)
    while _inputline != "quit":

        _inputline = raw_input(INPUT_STATEMENT)

        # capture empty values, for good UX
        if _inputline == "":
            print "   * * *"
            continue
        # capture 'quit'
        if _inputline == "quit":
            continue
        if _inputline == "save":
            print "   * * *"
            print sqlite_save(barcodes)
            barcodes = list() # start fresh
            print "There are now {} unsaved barcodes.".format(len(barcodes))
            print "   * * *"
            _inputline = ""
            continue

        print "   * * *"
        print "   * * *"
        print "Barcode has {} numbers.".format(len(_inputline))

        _accept_inputline = raw_input("Accept barcode? (press enter, any key to discard):")
        if _accept_inputline.lower() == "":
            barcodes.append(_inputline)
            print "Barcode: STORED. There are now {} unsaved barcodes.".format(len(barcodes))
            print "   * * *"
        else:
            print "\a"
            print "Barcode: DISCARDED DISCARDED DISCARDED."
            time.sleep(1)
            print "\a"
            print "Barcode: DISCARDED DISCARDED DISCARDED."
            time.sleep(1)
            print "\a"
            print "Barcode: DISCARDED DISCARDED DISCARDED."
            time.sleep(1)
            print "   * * *"

