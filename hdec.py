import sys
import bitstring # sudo pip install bitstring
from bitstring import BitStream, Bits
import struct

class Field:
    def __init__(self, name, bits, types, prefix = ""):
        self.name = name
        self.bits = bits
        self.types = types
        self.prefix = prefix
    
    def __repr__(self):
        return self.name + " (" + str(self.bits) + ")"
    
    def getBits(self):
        return self.bits
    
    def getName(self):
        return self.name
    
    def getTypes(self):
        t = []
        for ty in self.types:
            if ty[-1] == 'E':
                t.append((ty[:-1], True))
            else:
                t.append((ty, False))
        return t
    
    def getPrefix(self):
        return self.prefix


def parseDefinition(definition, bits = []):
    with open(definition) as df:
        d = df.readlines()
        for l in d:
            p = l.split(":")
            if len(p) == 2:
                bits.append(Field(p[0].strip(), (p[1].strip()), ["hex", "int", "bin"], definition))
            elif len(p) == 3:
                types = list(map(lambda x: x.strip(), p[2].strip().split(",")))
                bits.append(Field(p[0].strip(), (p[1].strip()), types, definition))
    return bits

def endianness(x, endian, bits):
    if endian:
        if bits == 32:
            return (((x << 24) & 0xFF000000) | ((x <<  8) & 0x00FF0000) | ((x >>  8) & 0x0000FF00) | ((x >> 24) & 0x000000FF))
        elif bits == 16:
            return (((x <<  8) & 0xFF00) | ((x >>  8) & 0x00FF))
        else:
            return x 
    else:
        return x
    
def main(argv):
    if len(argv) < 4:
        print("Usage: " + argv[0] + " <header dump> <type (hex|bin|raw)> <definition>")
        return
    
    filename = argv[1]
    typ = argv[2]
    definition = []
    for argc in range(3, len(argv)):
        definition.append(argv[argc])

    print("File: " + filename)
    print("Definition: " + ", ".join(definition))
    print("Type: " + typ)
    
    bits = []
    for d in definition:
        bits = parseDefinition(d, bits)
    
    content = None
    field = None
    with open(filename) as f:
            if typ == "hex":
                content = f.read().strip()
                field = BitStream("0x" + content)
                
            if typ == "bin":
                content = f.read().strip()
                field = BitStream("0b" + content)
        
            if typ == "raw":
                field = BitStream(f)
        
    parsed = {}
    pos = 0
    last_header = None
    for bit in bits:
        field.pos = pos
        
        bitlen = 0
        lenexpr = bit.getBits()
        for p in parsed.keys():
            lenexpr = lenexpr.replace(p, str(parsed[p]))
        try:
            bitlen = eval(lenexpr)
        except:
            print("Error: " + str(bit.getBits()) + " is not a valid size!")
            return
        
        val = field.read(bitlen)
        parsed[bit.getName()] = val.uint
        pos += bitlen
        if last_header is not bit.getPrefix():
            last_header = bit.getPrefix()
            print("")
        
        out = bit.getName() + ": "
        for t, endian in bit.getTypes():
            if t == "hex":
                out += "0x" + val.hex + " "
            if t == "int":
                out += str(endianness(val.uint, endian, int(bitlen))) + " "
            if t == "bin":
                out += "0b" + val.bin + " "
            if t == "str":
                s = ""
                for si in range(0, len(str(val)[2:]), 2):
                    out += str(chr(int(str(val)[si + 2:si + 4], 16)))
        print(out)

if __name__ == "__main__":
    main(sys.argv)


