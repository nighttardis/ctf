SecDSM Mini-CFT

### Project: AlienFS - 2020/05
TL;DR Description: Find a flag in an attached file

#### Solution code
[alien_fs.py](alien_fs.py)

#### Write-Up

When reviewing the data file with hexdump a pattern emerged with how the file was formatted. There where 6 lines that 
would makeup an "entry". The first 5 lines were broken up to a key/value pair, using the new line character as the delimiter.

Here is an example of the I mean.

```
00001080  42 4c 4b 48 44 52 0a 0a  41 4c 49 45 4e 76 31 0a  |BLKHDR..ALIENv1.|
00001090  42 4c 4b 4e 55 4d 0a 0a  2c 00 00 00 00 00 00 00  |BLKNUM..,.......|
000010a0  42 4c 4b 50 41 52 0a 0a  1f 00 00 00 00 00 00 00  |BLKPAR..........|
000010b0  42 4c 4b 4e 45 58 54 0a  2d 00 00 00 00 00 00 00  |BLKNEXT.-.......|
000010c0  42 4c 4b 54 59 50 45 0a  20 20 20 20 20 20 66 0a  |BLKTYPE.      f.|
000010d0  64 46 39 68 62 47 6c 6c  62 6c 39 30 5a 57 4e 6f  |dF9hbGllbl90ZWNo|
```

Depending on how wide the "key" is determined if there would be one or two new line characters that split the key from the value.

Through some trial and error the important parts seemed to be "BLKNUM" and "BLKNEXT". Best I could tell if "BLKNUM" was 
nothing, it was the start of a new entry, and "BLKNEXT" was the pointer to the next piece. Armed with that knowledge I wrote
a small python script hat would read through the file 16 bytes at a time to and build a dictionary for each set of entries in
the file. Splitting the entries into two separated containers, first there was a list for all entries that were the "start"
of a new chain. The second was a dictionary indexed by 'BLKNUM' to make it easier to put things together later.

Once this list and dictionary were built, a another simple loop to run through and put the "data" together following "BLKNEXT"
until it was blank. After this, the strings that were left were base64 decoding so the next step was to covert the strings.


Then, there was the flag.

If you made it this far, thanks for reading. If you aren't a great coder don't worry about it, the code I've uploaded wasn't
perfect when I started working on it and had other errors that I had to fix, and I'm sure it still isn't perfect, but it works
and for a CTF sometimes that's all you want.