# 2E 38 33 2A 2E 36

from basicparser import BasicUntokenizer

itens = [('VERSN',1),
    ('E-PPC',2),
    ('D-FILE',2),
    ('DF-CC',2),
    ('VARS',2),
    ('DEST',2),
    ('E-LINE',2),
    ('CH-ADD',2),
    ('X-PTR',2),
    ('STKBOT',2),
    ('STKEND',2),
    ('BERG',1),
    ('MEM',2),
    ('-',1),
    ('DF-SZ',1),
    ('S-TOP',2),
    ('LAST-K',2),
    ('DEBOUNCE',1),
    ('MARGIN',1),
    ('NXTLIN',2),
    ('OLDPPC',2),
    ('FLAGX',1),
    ('STRLEN',2),
    ('T-ADDR',2),
    ('SEED',2),
    ('FRAMES',2),
    ('COORDS',2),
    ('PR-CC',1),
    ('S-POSN',2),
    ('CDFLAG',1),
    ('PRBUFF',33),
    ('MEMBOT',30),
    ('--',2)
]

def one_byte(n : str, bb):
    b = int(bb[0])
    return f"{n} = {b:02x} {b:03d} " + bin(b)[2:].rjust(8,'0')

def two_bytes(n : str, v):
    b = int(v[0]) + int(v[1]) * 256
    return f"{n} = {b:04x} {b:d}"

def n_bytes(n : str, v):
    b = " ".join("{0:02X}".format(int(x)) for x in v)
    return f"{n} = {b}"

formatador = {1 : one_byte, 2 : two_bytes}

def format(n,dd):
    return formatador.get(len(dd), n_bytes)(n,dd)

import sys
with open(sys.argv[1],'rb') as inp:
    dados = inp.read()

i = 0
for item in itens:
    l = item[1]
    x = dados[i:i+l]
    addr = 0x4009 + i
    print(f"{addr} " + format(item[0],x))
    i += l
print(i,i + 0x4009)
bu = BasicUntokenizer()
p = i
q = (dados[7] + dados[8] * 256)-0x4009
while p < q:
    w = bu.untokenize(dados[p:], p-116+0x4009)
    if w == -1:
        break
    else:
        p += w
for i, line in enumerate(bu.lines):
    print(line, end='')