Universal Header Decoder
=================

This tool takes one or more description of a binary header and decodes the header of a given file.

# Usage

`python3 ./hdec.py <file-to-decode> <type> <header description> [<header 2 description> ...]`

# Header

Header files consist of a line-by-line description of each header field. Each line has the form
```
Name: Size in bits
```
or 
```
Name: Size in bits: display type
```

+ **Name** is displayed as field name
+ **Size in bits** determines the field size in bits. 
    It can also be a mathematical expression and can use previously parsed fields (referenced by their name)
+ **display type** (optional) defines how the value should be displayed. 
    It is a comma separated list with the following possible types: *int*, *hex*, *str*, *bin*, *intE* (int with changed endianness). 
    The default is *int, hex, bin* if this field is not given.

# Example

## IPv6 Packets

`python3 ./hdec.py sample/ipv6_icmpv6 hex header/IPv6 header/ICMPv6`
`python3 ./hdec.py sample/ipv6_udp hex header/IPv6 header/UDP`
`python3 ./hdec.py sample/6lowpan_iphc hex header/IPHC`

## Bitmap

`python3 ./hdec.py sample/bitmap.bmp raw header/BMP`
