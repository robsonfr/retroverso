import re
import struct


# Extracted from http://fileformats.archiveteam.org/wiki/Sinclair_BASIC_tokenized_file

ZX81_TOKENS = {' ': 0,
               '"': 11,
               '£': 12,
               '$': 13,
               ':': 14,
               '?': 15,
               '(': 16,
               ')': 17,
               '>': 18,
               '<': 19,
               '=': 20,
               '+': 21,
               '-': 22,
               '*': 23,
               '/': 24,
               ';': 25,
               ',': 26,
               '.': 27,
               '0': 28,
               '1': 29,
               '2': 30,
               '3': 31,
               '4': 32,
               '5': 33,
               '6': 34,
               '7': 35,
               '8': 36,
               '9': 37,
               'A': 38,
               'B': 39,
               'C': 40,
               'D': 41,
               'E': 42,
               'F': 43,
               'G': 44,
               'H': 45,
               'I': 46,
               'J': 47,
               'K': 48,
               'L': 49,
               'M': 50,
               'N': 51,
               'O': 52,
               'P': 53,
               'Q': 54,
               'R': 55,
               'S': 56,
               'T': 57,
               'U': 58,
               'V': 59,
               'W': 60,
               'X': 61,
               'Y': 62,
               'Z': 63,
               'RND': 64,
               'INKEY$': 65,
               'PI': 66,
               'EDIT': 117,
               'NEWLINE': 118,
               'RUBOUT': 119,
               '/': 120,
               'FUNCTION': 121,
               '""': 192,
               'AT': 193,
               'TAB': 194,
               '?': 195,
               'CODE': 196,
               'VAL': 197,
               'LEN': 198,
               'SIN': 199,
               'COS': 200,
               'TAN': 201,
               'ASN': 202,
               'ACS': 203,
               'ATN': 204,
               'LN': 205,
               'EXP': 206,
               'INT': 207,
               'SQR': 208,
               'SGN': 209,
               'ABS': 210,
               'PEEK': 211,
               'USR': 212,
               'STR$': 213,
               'CHR$': 214,
               'NOT': 215,
               '**': 216,
               'OR': 217,
               'AND': 218,
               '<=': 219,
               '>=': 220,
               '<>': 221,
               'THEN': 222,
               'TO': 223,
               'STEP': 224,
               'LPRINT': 225,
               'LLIST': 226,
               'STOP': 227,
               'SLOW': 228,
               'FAST': 229,
               'NEW': 230,
               'SCROLL': 231,
               'CONT': 232,
               'DIM': 233,
               'REM': 234,
               'FOR': 235,
               'GOTO': 236,
               'GOSUB': 237,
               'INPUT': 238,
               'LOAD': 239,
               'LIST': 240,
               'LET': 241,
               'PAUSE': 242,
               'NEXT': 243,
               'POKE': 244,
               'PRINT': 245,
               'PLOT': 246,
               'RUN': 247,
               'SAVE': 248,
               'RAND': 249,
               'IF': 250,
               'CLS': 251,
               'UNPLOT': 252,
               'CLEAR': 253,
               'RETURN': 254,
               'COPY': 255}

ZX81_CODES = {0: ' ',
              11: '"',
              12: '£',
              13: '$',
              14: ':',
              15: '?',
              16: '(',
              17: ')',
              18: '>',
              19: '<',
              20: '=',
              21: '+',
              22: '-',
              23: '*',
              24: '/',
              25: ';',
              26: ',',
              27: '.',
              28: '0',
              29: '1',
              30: '2',
              31: '3',
              32: '4',
              33: '5',
              34: '6',
              35: '7',
              36: '8',
              37: '9',
              38: 'A',
              39: 'B',
              40: 'C',
              41: 'D',
              42: 'E',
              43: 'F',
              44: 'G',
              45: 'H',
              46: 'I',
              47: 'J',
              48: 'K',
              49: 'L',
              50: 'M',
              51: 'N',
              52: 'O',
              53: 'P',
              54: 'Q',
              55: 'R',
              56: 'S',
              57: 'T',
              58: 'U',
              59: 'V',
              60: 'W',
              61: 'X',
              62: 'Y',
              63: 'Z',
              64: 'RND',
              65: 'INKEY$',
              66: 'PI',
              112: '<cursor up>',
              113: '<cursor down>',
              114: '<cursor left>',
              115: '<cursor right>',
              116: 'GRAPHICS',
              117: 'EDIT',
              118: '',
              119: 'RUBOUT',
              120: '/',
              121: 'FUNCTION',
              126: '',
              127: 'cursor',
              128: ' ',
              139: '"',
              140: '£',
              141: '$',
              142: ':',
              143: '?',
              144: '(',
              145: ')',
              146: '>',
              147: '<',
              148: '=',
              149: '+',
              150: '-',
              151: '*',
              152: '/',
              153: ';',
              154: '-',
              155: '.',
              156: '0',
              157: '1',
              158: '2',
              159: '3',
              160: '4',
              161: '5',
              162: '6',
              163: '7',
              164: '8',
              165: '9',
              166: 'A',
              167: 'B',
              168: 'C',
              169: 'D',
              170: 'E',
              171: 'F',
              172: 'G',
              173: 'H',
              174: 'I',
              175: 'J',
              176: 'K',
              177: 'L',
              178: 'M',
              179: 'N',
              180: 'O',
              181: 'P',
              182: 'Q',
              183: 'R',
              184: 'S',
              185: 'T',
              186: 'U',
              187: 'V',
              188: 'W',
              189: 'X',
              190: 'Y',
              191: 'Z',
              192: '""',
              193: 'AT ',
              194: 'TAB ',
              195: '? ',
              196: 'CODE ',
              197: 'VAL ',
              198: 'LEN ',
              199: 'SIN ',
              200: 'COS ',
              201: 'TAN ',
              202: 'ASN ',
              203: 'ACS ',
              204: 'ATN ',
              205: 'LN ',
              206: 'EXP ',
              207: 'INT ',
              208: 'SQR ',
              209: 'SGN ',
              210: 'ABS ',
              211: 'PEEK ',
              212: 'USR ',
              213: 'STR$ ',
              214: 'CHR$ ',
              215: 'NOT ',
              216: '** ',
              217: ' OR ',
              218: ' AND ',
              219: '<=',
              220: '>=',
              221: '<> ',
              222: ' THEN ',
              223: ' TO ',
              224: ' STEP ',
              225: 'LPRINT ',
              226: 'LLIST',
              227: 'STOP',
              228: 'SLOW',
              229: 'FAST',
              230: 'NEW',
              231: 'SCROLL',
              232: 'CONT',
              233: 'DIM ',
              234: 'REM ',
              235: 'FOR ',
              236: 'GOTO ',
              237: 'GOSUB ',
              238: 'INPUT ',
              239: 'LOAD ',
              240: 'LIST',
              241: 'LET ',
              242: 'PAUSE ',
              243: 'NEXT ',
              244: 'POKE ',
              245: 'PRINT ',
              246: 'PLOT ',
              247: 'RUN ',
              248: 'SAVE ',
              249: 'RAND ',
              250: 'IF ',
              251: 'CLS',
              252: 'UNPLOT ',
              253: 'CLEAR',
              254: 'RETURN',
              255: 'COPY '}

def fl_to_fp(f):
    ret=bytearray([0]*5)
    if f != 0.0:
        fl_val=struct.pack(">f",f)
        # os primeiros 9 bits contem o sinal e o expoente
        # com offset de 127. Para o formato de 40 bits, 
        # primeiro vem o expoente com offset de 128, depois
        # o sinal
        expoente = ((fl_val[0] & 127) << 1) | ((fl_val[1] & 128) >> 7)
        ret[0]= (expoente + 2)
        ret[1] = (fl_val[0] & 128) | (fl_val[1] & 127)
        ret[2] = fl_val[2]
        ret[3] = fl_val[3]
    return ret


class PFile:
    SAVE_AREA = [   ('VERSN ', 1),
                ('E_PPC ', 2),
                ('D_File', 2),
                ('DF_CC ', 2),
                ('VARS  ', 2),
                ('DEST  ', 2),
                ('E_LINE', 2),
                ('CH_ADD', 2),
                ('X_PTR ', 2),
                ('STKBOT', 2),
                ('STKEND', 2),
                ('BERG  ', 1),
                ('MEM   ', 2),
                ('PAD1- ', 1),
                ('DF_SZ ', 1),
                ('S_TOP ', 2),
                ('LAST_K', 2),
                ('DEBOUN', 1),
                ('MARGIN', 1),
                ('NXTLIN', 2),
                ('OLDPPC', 2),
                ('FLAGX ', 1),
                ('STRLEN', 2),
                ('T_ADDR', 2),
                ('SEED  ', 2),
                ('FRAMES', 2),
                ('COORDS', 2),
                ('PR_CC ', 1),
                ('S_POSN', 2),
                ('CDFLAG', 1),
                ('PRBUFF', 32),
                ('NEWL  ', 1),
                ('MEMBOT',30),
                ('PAD2- ',2)]
        
    def __init__(self):
        self.header_info = dict()

    def parse_header(self, header : bytes):
        p = 0
        for name, size in PFile.SAVE_AREA:
            self.header_info[name.rstrip()] = header[p:p+size]
            p += size

class BasicParser:
    BASIC_LINE = re.compile(r'^(\d+)\s+(.+)$')

    def __init__(self, input: str = ''):
        if input:
            self.parse(input)

    def parse(self, input: str):
        match = BasicParser.BASIC_LINE.match(input)
        if match:
            self.line_number = int(match.group(1))
            words = match.group(2).split(' ')
            self.statement = words[0]
            self.token = ZX81_TOKENS.get(self.statement.upper(), -1)
            self.words = ' '.join(words[1:])
        #else:
        #    print(input)

    def as_bytes(self):
        byte_data = bytearray()
        byte_data += struct.pack('>H', self.line_number)
        resto = bytearray()
        tamanho = 0
        resto.append(self.token)
        ehNumero=False
        numero = ""
        word=""
        aspas=False

        def processa_num(numero):
            bytes_ret = bytearray([ZX81_TOKENS.get(lt) for lt in numero])
            bytes_ret.append(0x7E)
            try:
                bytes_ret += fl_to_fp(float(numero))
            except Exception as e :
                print(self.line_number)
                raise e 
                #sys.exit(1)
            return (False, "", bytes_ret)

        def processa_word(w, asp):
            token = ZX81_TOKENS.get(w,-1)
            bytes_ret = bytearray()
            if token == -1 or asp:
                for letter in w:
                    c=ZX81_TOKENS.get(letter,-1)
                    if c == -1:
                        print(letter)
                    bytes_ret.append(c)
            else:
                bytes_ret.append(token)
            return ("",False,bytes_ret)


        for i,b in enumerate(self.words):
            print(i,b,ehNumero,numero,word)
            if b in '0123456789.' and not aspas:
                if word:
                    word, aspas, rt = processa_word(word, aspas)
                    resto += rt
                ehNumero = True
                numero += b
            elif b != ' ':
                if ehNumero:
                    ehNumero, numero, rt = processa_num(numero)
                    resto += rt
                if b == '"' and not aspas:
                    aspas = True
                word += b
            else:
                if aspas:
                    word += b
                else:
                    if ehNumero:
                        ehNumero, numero, rt = processa_num(numero)
                        resto += rt
                    elif word:                    
                        word, aspas, rt = processa_word(word, aspas)
                        resto += rt
        if ehNumero:
            ehNumero, numero, rt = processa_num(numero)
            resto += rt
        elif word:
            word, aspas, rt = processa_word(word, aspas)
            resto += rt
        resto.append(0x76)
        tamanho = len(resto)
        byte_data += struct.pack('<H', tamanho)
        byte_data += resto
        return byte_data

    def __str__(self):
        return f'{self.line_number:04X} -> {self.statement}[{self.token:02X}] -> {self.words}'


class BasicLine:
    def __init__(self, line_number: int, length: int, text: str):
        self.line_number = line_number
        self.length = length
        self.text = text

    def __str__(self):
        return f"{self.line_number} {self.text}"


class BasicUntokenizer:
    def __init__(self):
        self.lines: list[BasicLine] = []
        self.addresses: list[int] = []

    def untokenize(self, data: bytes, address: int):
        line_number = data[0] * 256 + data[1]
        length = data[3] * 256 + data[2]
        text = ""
        c = []
        skip = 0
        for b in data[4:4+length]:
            if b == 0x7e:
                skip = 6
            if skip == 0:
                word = ZX81_CODES.get(int(b), f'<unknown:{b:02X}>')
                text += word
            else:
                skip -= 1
            c.append(b)
        text += '\n'
        #text += ': REM ' + ' '.join([f'{x:02X}' for x in c ]) + '\n'
        if line_number != 30208:
            self.lines.append(BasicLine(line_number, length, text))
            self.addresses.append(address)
            return length + 4
        else:
            return -1


if __name__ == '__main__':
    import sys
    if sys.argv[1] == '-c':
        with open(sys.argv[2], 'rt') as inp:
            basic = [BasicParser(line) for line in inp.readlines()]
        with open(sys.argv[3],'wb') as out:
            for b in basic:
                #print(b)
                out.write(b.as_bytes())
    elif sys.argv[1] == '-d':
        bu = BasicUntokenizer()
        with open(sys.argv[2], 'rb') as inp:
            wholef = inp.read()
        p = 116
        pf = PFile()
        pf.parse_header(wholef)
        for k,_ in PFile.SAVE_AREA:
            print(k," ".join([hex(v) for v in pf.header_info[k.rstrip()]]))
        q = (wholef[7]+wholef[8]*256)-0x4009
        while p < q:
            w = bu.untokenize(wholef[p:], p-116+0x4009)
            if w == -1:
                break
            else:
                p += w
        for i, line in enumerate(bu.lines):
            print(line, end='')
