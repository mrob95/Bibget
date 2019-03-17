# bibget

Commandline utility for downloading citations from google scholar and Google books.

default behaviour: prints the first google scholar bibTeX citation to standard output
-l: given title, list results as tab separated values in the form title, author, year, bibTeX link
-f: same as above, but only returns the first result
-u: takes the output of one of the above and returns a citation

```
bibget -l "the bible" | dmenu -i -l 10 | bibget -u > bib.bib
```