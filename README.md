# Python scripts

## `citations.py`

Given an author identified by his/her BAI, this Python3 script counts the total number of citations and the total number of citations excluding self cites over all papers of this author in the [Inspirehep](http://inspirehep.net/) database.

Additionally, it allows saving a snapshot for later detection of changes in the number of citations of individual papers and detection of new/removed papers

Built on & inspired by [https://github.com/efranzin/python](https://github.com/efranzin/python)

**Usage:**

`python citations.py`

**Sample output:**
```
Total number of citations: 382; Excluding self cites: 227

3 new citations: "On the prospects of ultra-high energy cosmic rays "

Do you want to save a snapshot [y/n]?  n
Not saved.
```

**Parameters at the beginning of the file:**
* `AUTHOR`, specifies the author's BAI identifier (default `P.Motloch.2`)
* `MAX_NUM_PAPERS`, specifies the maximal number of papers requested from INSPIRE-HEP (default `1000`)
* `SHORT_TITLE_LENGTH`, specifies the length to which shorten long paper titles (default `50`)
* `NEED_WRITE_CONFIRM`, specifies whether the program asks the user before writing to disk (default `True`)
* `FILENAME`, specifies the snapshot file
