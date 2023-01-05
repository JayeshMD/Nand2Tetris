import numpy as np
import codes

#%% File
file = "/Users/jayeshdhadphale/Desktop/D_folder/My_Computer/nand2tetris/projects/06/pong/PongL.asm"

f = open(file,'r')
prog=f.readlines()

#%% Parsing
def rem_space(st):
    b = ''
    for p in st:
        if p!=' ' and p!='\t':
            b = b+p
    return b

def split_C(line):
    if ('=' in line) and (';' in line):
        dest = rem_space(line[:line.find('=')])
        comp = rem_space(line[line.find('=')+1:line.find(';')])
        jmp  = rem_space(line[line.find(';')+1:])
    if not('=' in line) and (';' in line):   
        dest = 'null'
        comp = rem_space(line[:line.find(';')])
        jmp  = rem_space(line[line.find(';')+1:])
    if ('=' in line) and not(';' in line):
        dest = rem_space(line[:line.find('=')])
        comp = rem_space(line[line.find('=')+1:])
        jmp  = 'null'

    return {'dest':dest, 'comp':comp, 'jmp' :jmp }

def Parser(prog):
    par_arr = []
    for line in prog:
        flag=0
        for i in range(len(line)):
            if line[i]!=' ' and line[i]!='\n':
                flag=1
                if line[i:i+2]=='//':
                    tp = 'Comment'
                elif line[i]=='(':
                    tp = 'label'
                else:
                    tp = 'instruction'
                break
        if flag==0:
            tp = 'empty'
        
        if tp == 'instruction':
            if '@' in line:
                tp2 = 'A-instruction'
                if '//' in line:
                    par = line[line.find('@')+1:line.find('//')]
                else:
                    par = line[line.find('@')+1:line.find('\n')]
                par = rem_space(par)
            else:
                tp2 = 'C-instruction'
                if '//' in line:
                    par = line[:line.find('//')]
                    par = split_C(par)
                else:
                    par = line[:line.find('\n')]
                    par = split_C(par)

        elif tp == 'label':
            tp2 = 'label'
            par = rem_space(line[line.find('(')+1:line.find(')')])
        else:
            tp2 =''
            par = None

        if tp2 == 'A-instruction':
            par2 = ['A',par]
        if tp2 == 'C-instruction':
            par2 = ['C',par]
        if tp2 == 'label':
            par2 = ['label',par]

        if par != None:
            par_arr.append(par2)
    return par_arr

#%% generate code
def gen_code(par_arr):
    bin_code = []
    for par in par_arr:
        if par[0]=='A':
            bin_code.append('0'+str(np.binary_repr(int(par[1]),15)))
        if par[0]=='C':
            #print(par[1]['comp'])
            bin_code.append('111' + codes.comp[par[1]['comp']] + codes.dest[par[1]['dest']] + codes.jmp[par[1]['jmp']])
    return bin_code


par_arr = Parser(prog)
[print(i) for i in par_arr]
bin_code = gen_code(par_arr)
[print(i) for i in bin_code]


textfile = open("bin_file.hack", "w")
for element in bin_code:
    textfile.write(element + "\n")
textfile.close()










'''
class SymbolTable:
    def __init__(self):
        self.sym = []
        self.val = []

    def add_Lablel(self,name,address):
        pass

    def add_Variable(self,name,address):
        pass
'''