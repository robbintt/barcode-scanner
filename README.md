
### How-to

Right click on 'bookscanner.py' and choose Open With --> "Terminal Emulator"

Scan your first book at the prompt. YOU MUST PRESS ENTER TO STORE IT.

This book is not yet saved! Read on:

Keep following the pattern. Scan, press enter, scan, press enter.

When you have done about 20, type 'save' to put all 20 in the database.

If you make an error (like scanning the same stack twice), you can 'quit' and start over.

Once you save, it will flush the stored numbers so you won't lose your work.


### Missing

the system beeps aren't working! WHY??


### Goals

Use the EAN (International Article Number) to retrieve the ISBN and other book metadata.


Information:

- The barcode is an EIN, and is the ISBN for most books. Woohoo. When isn't it?
- The EAN is a 13 digit number. It must begin with 978 or 979 if it refers to an ISBN.
- isbndb.com v2 API provides metadata for up to 500 requests per token per day.


Problems:
- When isn't the barcode an isbn?


