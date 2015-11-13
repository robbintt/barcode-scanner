#!/usr/bin/python
"""
Goal: Dump barcodes.
"""
import sqlite3
import os
import time
import pprint


OUTPUT_DIR = "data"
SQLITE_FILE = "barcodes.sqlite"

# toggle this in-console, not here. hyperscan turns off barcode confirmations.
HYPERSCAN_TOGGLE = False

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

    SAVE_STATEMENT = "Type 'save' to save and continue.\n"
    DUMP_STATEMENT = "Type 'dump' to see the barcodes ready to be saved\n"
    QUIT_STATEMENT = "Type 'quit' to exit.\n"
    INSTRUCTION_STATEMENT = "Please scan the next book:"
    INPUT_STATEMENT = SAVE_STATEMENT + DUMP_STATEMENT + \
                        QUIT_STATEMENT + INSTRUCTION_STATEMENT


    barcodes = list()
    _inputline = "" # sentinel value (no do while in python)
    while _inputline != "quit":

        _inputline = raw_input(INPUT_STATEMENT)

        # capture empty values, for good UX
        if _inputline == "":
            print "   * * *"
            continue

        HYPERSCAN_STATEMENT = "Type 'hyperscan' to enter fast mode."
        if _inputline == "hyperscan":
            if HYPERSCAN_TOGGLE:
                HYPERSCAN_TOGGLE = False
                print("hyperscan mode is now OFF.")
            else:
                HYPERSCAN_TOGGLE = True
                print("hyperscan mode is now ON!!")
            _inputline = ""
            print "   * * *"
            continue

        UNDO_STATEMENT = "Type 'undo' to undo the last entry.\n"
        if _inputline == "undo":
            if len(barcodes) > 0:
                _undo_confirm = raw_input("{} will be removed from the queue. (y/Y) to confirm:".format(barcodes[-1]))
                if _undo_confirm.lower() == "y":
                    print("{} removed from queue.".format(barcodes.pop()))
                else:
                    print("Undo cancelled.")
            else:
                print "Nothing to undo!"
            _inputline = ""
            print "   * * *"
            continue

        # capture 'quit'
        if _inputline == "quit":
            continue
        if _inputline == "dump":
            print "Current barcodes NOT YET SAVED:"
            pprint.pprint(barcodes)
            _inputline = ""
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

        if HYPERSCAN_TOGGLE == False:
            _accept_inputline = raw_input("Accept barcode? (press enter, any nonempty value to discard):")
        else:
            # skip confirmation if hyperscan is on/True
            _accept_inputline = ""

        if _accept_inputline == "":
            barcodes.append(_inputline)
            print "Barcode: STORED. There are now {} unsaved barcodes.".format(len(barcodes))
            print "   * * *"
        else:
            print "\a"
            print "Barcode: DISCARDED DISCARDED DISCARDED."
            time.sleep(1)
            print "\a"
            print "Discard cooldown. 2 seconds remaining."
            time.sleep(1)
            print "\a"
            print "Discard cooldown. 1 second remaining."
            time.sleep(1)
            print "   * * *"

