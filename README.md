
Barcode Scanner User Guide:
===============================

**DISCLAIMER:** This is a simple interface, it requires patience and slowness.

#### Please read all text as you scan. Verify that each entry 'looks right'.


The barcode scanner script DOES:
================================
- Show you the barcodes you scanned.
- Allow you to undo errors.
- Add your barcodes to a database (once you 'save' them).


The barcode scanner script does NOT:
================================
- Teach you how barcodes work (some notes on this are below)
- Find errors
- Fix errors


Steps:
======
1. Right click on 'bookscanner.py' and choose Open With --> "Terminal Emulator"
2. Scan your first book at the prompt.
3. Press ENTER to store the barcode in your queue. The barcode is not yet saved.
4. Repeat 3 and 4 for a small stack of books.
5. When you are ready to commit your barcodes, type 'save' (without the quotes).
6. At this point there should be '0 unsaved barcodes'.
7. Use the 'quit' command to quit.


Warnings:
=========
- Some books have a sticker barcode, don't scan this. We can't trust it! Enter the barcode manually instead. The sticker barcode could be anything.
- Some books don't have a barcode and need manually entered. You can find the ISBN inside the front of the book on the left-side page soon after the title page.
- Some books do not have an ISBN at all. Put these in the grey bin, they can be manually added once we have a full book database.


Important:
==========
- You may manually enter a barcode and press enter to submit it. You will still need to verify the value by pressing enter again.
- Make sure to save before you quit.
- Use the 'help' command to see all available commands.


Commands:
=========
- help - show the help (these commands)
- save - save and continue
- show - see the barcodes in your queue
- hyperscan - enter fast mode (no confirmations required)
- undo - delete the last entry in your queue
- quit - exit/quit **WITHOUT** saving


Notes:
======
- We are collecting barcodes. Sometimes those are ISBNs, we'll sort it out later.
- The barcode is an EIN, and is the ISBN for **many** books.
- Some barcodes are 12 digits. They seem to have a 10 digit ISBN. Why?
- Before modern day: many standards.
- Modern day: The EAN is a 13 digit number. It must begin with 978 or 979 if it refers to an ISBN.
- isbndb.com v2 API provides metadata for up to 500 requests per token per day.

