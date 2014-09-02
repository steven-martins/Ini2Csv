Ini2Csv
==========

A simple way to convert ini files to csv in Python (and the other way : csv to ini files). Python >=3.3



## Example

```python

    c = Conf2Csv("./slugs.conf")
    c.export("export.csv")


    s = Csv2Conf("./export.csv")
    s.export("result.conf")

```
