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
db_file = os.path.join(OUTPUT_DIR, SQLITE_FILE)

PAGE_NUMBER = 0
SPACER = " " * 40 # can use any character, empty seems to be best

# toggle this in-console, not here. hyperscan True turns off barcode confirmations.
# true by default, in practice it is tough to remember to verify each scan with a keypress.
HYPERSCAN_TOGGLE = True

def pagination_spacer():
    """ A spacer that gives information about the current command 'page'
    """
    global PAGE_NUMBER
    PAGE_NUMBER += 1
    pagination =  "-{} (Page # {})".format(SPACER, str(PAGE_NUMBER))
    pagination += "\n"
    pagination += " {} type 'help' for commands".format(SPACER,)

    return pagination


def construct_statement(*args):
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

def sqlite_save(barcodes):
    """ Accept a list of barcodes and dump it to the sqlite database.
    """

    # quick and dirty - don't save if there is no data.
    if not len(barcodes):
        # skip this if there are no barcodes
        return "No data to save... continue..."

    # reformat each list item to a tuple for sqlite3 executemany
    barcode_tuples = [(x,) for x in barcodes]

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.executemany("INSERT INTO barcode VALUES (?)", barcode_tuples)

    c.execute("SELECT COUNT(*) FROM barcode")
    BOOK_COUNT = c.fetchall()

    conn.commit()
    conn.close()
    
    return "Save seemed successful. {} total books have been entered.".format(BOOK_COUNT[0][0],)


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
    HELP_STATEMENT = "Type 'help' to see this help.\n"
    QUIT_STATEMENT = "Type 'quit' to exit.\n"

    INSTRUCTION_STATEMENT = "Scan NEXT BOOK:"


    COMMAND_INFORMATION = construct_statement(SAVE_STATEMENT, 
            SHOW_STATEMENT, HYPERSCAN_STATEMENT, UNDO_STATEMENT, 
            HELP_STATEMENT, QUIT_STATEMENT)

    INPUT_STATEMENT = construct_statement(INSTRUCTION_STATEMENT)
    
    barcodes = list()

    while True:
        print pagination_spacer()

        _inputline = raw_input(INPUT_STATEMENT)
        print


        if _inputline == "quit":
            if len(barcodes) > 0:
                print "You cannot quit unless there are no items in the queue."
                print "Type show to see your queue, type undo to remove items"
                print "Use ctrl+c to quit anyways."
            else:
                break

            continue

        # capture empty values, for good UX
        if _inputline == "":
            continue

        if _inputline == "help":
            print COMMAND_INFORMATION
            continue

        if _inputline == "hyperscan":
            if HYPERSCAN_TOGGLE:
                HYPERSCAN_TOGGLE = False
                print("hyperscan mode is now OFF.")
            else:
                HYPERSCAN_TOGGLE = True
                print("hyperscan mode is now ON!!")
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
            continue

        if _inputline == "show":
            print "Current barcodes NOT YET SAVED:"
            for barcode in barcodes:
                print barcode
            continue

        if _inputline == "save":
            print sqlite_save(barcodes)
            barcodes = list() # start fresh
            print "There are now {} unsaved barcodes.".format(len(barcodes))
            continue

        # manage non-command input as a barcode:

        print "INFO: The scan has {} numbers.".format(len(_inputline))
        print

        if HYPERSCAN_TOGGLE == False:
            print "accept: Press ENTER.  |  discard: type anything THEN press enter."
            print
            _accept_inputline = raw_input("ACCEPT scan?")
        else:
            # skip confirmation if hyperscan is on/True
            _accept_inputline = ""

        if _accept_inputline == "":
            barcodes.append(_inputline)
            print "Barcode: STORED."
            print "There are now {} unsaved barcodes.".format(len(barcodes))
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

