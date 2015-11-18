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

LINE_NUMBER = 0
SPACER = " " * 40 # can use any character, empty seems to be best

def numbered_spacer():
    global LINE_NUMBER
    LINE_NUMBER += 1
    return "-{} (Page # {})".format(SPACER, str(LINE_NUMBER))

def construct_input_statement(*args):
    """ dead simple statement to keep control flow clean.

    This is broken out so that more interesting things
    can be done with the 'standard information' given to
    the user in the future.

    One such idea is to hide some commands unless a 'help'
    command is performed. Or something.
    """

    INPUT_STATEMENT = ""
    for statement in args:
        INPUT_STATEMENT += statement
        

    return INPUT_STATEMENT

# toggle this in-console, not here. hyperscan turns off barcode confirmations.
HYPERSCAN_TOGGLE = False

def sqlite_save(barcodes):
    """ Accept a list of barcodes and dump it to the sqlite database.
    """

    # quick and dirty - don't save if there is no data.
    if not len(barcodes):
        # skip this if there are no barcodes
        return "No data to save... continue..."

    # reformat each list item to a tuple for sqlite3 executemany
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

    Commands all follow the same template. This could be easily
    refactored but the original purpose of this code is one-time use.
    """
    SAVE_STATEMENT = "Type 'save' to save and continue.\n"
    SHOW_STATEMENT = "Type 'show' to see the barcodes ready to be saved\n"
    HYPERSCAN_STATEMENT = "Type 'hyperscan' to enter fast mode.\n"
    UNDO_STATEMENT = "Type 'undo' to undo the last entry.\n"
    QUIT_STATEMENT = "Type 'quit' to exit.\n"
    INSTRUCTION_STATEMENT = "Please scan the NEXT BOOK:"

    INPUT_STATEMENT = construct_input_statement(SAVE_STATEMENT, 
            SHOW_STATEMENT, HYPERSCAN_STATEMENT, UNDO_STATEMENT, 
            QUIT_STATEMENT, INSTRUCTION_STATEMENT)


    print numbered_spacer()
    print "Please SAVE your work OFTEN, there is no error handling."
    print numbered_spacer()


    barcodes = list()
    _inputline = "" # sentinel value (no do while in python)
    while _inputline != "quit":

        _inputline = raw_input(INPUT_STATEMENT)

        # capture empty values, for good UX
        if _inputline == "":
            print numbered_spacer()
            continue

        if _inputline == "hyperscan":
            if HYPERSCAN_TOGGLE:
                HYPERSCAN_TOGGLE = False
                print("hyperscan mode is now OFF.")
            else:
                HYPERSCAN_TOGGLE = True
                print("hyperscan mode is now ON!!")
            _inputline = ""
            print numbered_spacer()
            continue

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
            print numbered_spacer()
            continue

        # capture 'quit'
        if _inputline == "quit":
            continue
        if _inputline == "show":
            print numbered_spacer()
            print "Current barcodes NOT YET SAVED:"
            for barcode in barcodes:
                print barcode
            print numbered_spacer()
            _inputline = ""
            continue
        if _inputline == "save":
            print sqlite_save(barcodes)
            barcodes = list() # start fresh
            print numbered_spacer()
            print "There are now {} unsaved barcodes.".format(len(barcodes))
            print numbered_spacer()
            _inputline = ""
            continue

        print numbered_spacer()
        print
        print "Barcode has {} numbers.".format(len(_inputline))
        print

        if HYPERSCAN_TOGGLE == False:
            print "accept: Press ENTER.  |  discard: type anything THEN press enter."
            _accept_inputline = raw_input("ACCEPT scan?")
        else:
            # skip confirmation if hyperscan is on/True
            _accept_inputline = ""

        if _accept_inputline == "":
            barcodes.append(_inputline)
            print numbered_spacer()
            print "Barcode: STORED."
            print "There are now {} unsaved barcodes.".format(len(barcodes))
            print numbered_spacer()
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
            print numbered_spacer()

