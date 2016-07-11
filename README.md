Universal Header Decoder
=================

This tool takes one or more descriptions of a binary header and decodes the header of a given file. The main purpose of this tool is for debugging file formats.

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
or
```
Name: Size in bits: display type: condition
```
+ **Name** is displayed as field name
+ **Size in bits** determines the field size in bits. 
    It can also be a mathematical expression and can use previously parsed fields (referenced by their name)
+ **display type** (optional) defines how the value should be displayed. 
    It is a comma separated list with the following possible types: *int*, *hex*, *str*, *bin*, *intE* (int with changed endianness). 
    The default is *int, hex, bin* if this field is not given.
+ **condition** (optional) the field is only considered if the condition is fulfilled. The condition can contain any logical expression and the names of already parsed fields.

# Examples

## IPv6 Packets

* `python3 ./hdec.py sample/ipv6_icmpv6 hex header/IPv6 header/ICMPv6`
```
    File: sample/ipv6_icmpv6.txt
    Definition: header/IPv6, header/ICMPv6
    Type: hex
    
    Version: 6 
    TrafficClass: 0x00 
    FlowLabel: 0x10000 
    Length: 24 
    NextHeader: 0x3a 58 
    HopLimit: 64 
    Source: 0xfe8000000000000002124b0006a0f908 
    Destination: 0xfe8000000000000002124b00068a090f 
    
    Type: 128 0x80 
    Code: 0 0x00 
    Checksum: 0xb924 
    Identifier: 0x0000 
    Sequence: 0x0000 
    Payload: 0x04040404040404040404040404040404
```
* `python3 ./hdec.py sample/ipv6_udp hex header/IPv6 header/UDP`
```
    File: sample/ipv6_upd.txt
    Definition: header/IPv6, header/UDP
    Type: hex
    
    Version: 6 
    TrafficClass: 0x00 
    FlowLabel: 0x00000 
    Length: 16 
    NextHeader: 0x11 17 
    HopLimit: 64 
    Source: 0xfe8000000000000002124b0006a0f908 
    Destination: 0xfe8000000000000002124b00068a090f 
    
    SourcePort: 7778 0x1e62 
    DestinationPort: 7777 0x1e61 
    Length: 16 0x0010 
    Checksum: 0xea70 
    Payload: 0x0000320000320000
```
* `python3 ./hdec.py sample/6lowpan_iphc hex header/IPHC`
```
    File: sample/6lowpan_iphc.txt
    Definition: header/IPHC
    Type: hex
    
    Start: 0b011 
    TF: 0b01 1 
    NH: 0b0 
    HopLimit: 0b10 2 
    CID: 0b0 
    SAC: 0b0 
    SAM: 0b11 3 
    M: 0b0 
    DAC: 0b0 
    DAM: 0b11 3 
    ECN: 0b00 0 
    Padding: 0b00 
    FlowLabel: 0x10000 
    NextHeader: 0x3a 58 
```
## Bitmap

* `python3 ./hdec.py sample/bitmap.bmp raw header/BMP`
```
    File: sample/bitmap.bmp
    Definition: header/BMP
    Type: raw

    Magic: 0x424d BM
    FileSize: 307338 
    Zero: 0x00000000 
    Position: 138 
    HeaderLen: 124 
    Width: 320 
    Height: 320 
    Layers: 1 
    Depth: 24 
    Compression: 0 
    DataLength: 307200 
    XPixelMeter: 2835 
    YPixelMeter: 2835 
    UsedColors: 0 
    ImportantColors: 0 
```