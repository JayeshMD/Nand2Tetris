#!/usr/local/bin/python3

import os
import argparse

msg = 'This program compiles the *.vm code without brancing commands'



parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-f", "--f_path", help = "Give folder or file path.")
args = parser.parse_args()

print(args.f_path)

file_path_inp = args.f_path

if os.path.isdir(file_path_inp):
    vm_files = [file_path_inp+'/'+f for f in os.listdir(file_path_inp) if '.vm' in f]
    fld_parent, fld = os.path.split(file_path_inp)
    output_file = file_path_inp + '/'+ fld + '.asm'
elif os.path.isfile(file_path_inp):
    vm_files = [file_path_inp]
    fld_vm, file_vm = os.path.split(file_path_inp)
    file_initials = file_vm[0:file_vm.find('.vm')]
    output_file = fld_vm + '/'+ file_initials + '.asm'

def remove_comments(file_lines):
    file_clean = []
    for fl in file_lines:
        loc = fl.find('//')
        if loc==-1:
            fl_app = fl
        else:
            fl_app = fl[0:loc]
        if len(fl_app)>0:
            file_clean.append(fl_app)
    return file_clean

def remove_backslash_n(file_lines):
    file_clean = []
    for fl in file_lines:
        loc = fl.find('\n')
        if loc==-1:
            fl_app = fl
        else:
            fl_app = fl[0:loc]
        if len(fl_app)>0:
            file_clean.append(fl_app)
    return file_clean

def get_clean_file(file_path):
    file = open(file_path)
    file_lines = file.readlines()
    file_lines_temp = remove_comments(file_lines)
    file_lines_temp = remove_backslash_n(file_lines_temp)
    return file_lines_temp

def get_assem_push(line_elements, file_initials):
    if line_elements[1] == 'constant':
        assem  = '@'+ line_elements[2]+'\n'
        assem += 'D=A'+'\n'
        assem += '@SP'+'\n'
        assem += 'AM=M+1'+'\n'
        assem += 'A=A-1'+ '\n'
        assem += 'M=D'+'\n'
        
    if line_elements[1] == 'local':
        assem  = '@'+ line_elements[2]+'\n'
        assem += 'D=A'+'\n'
        assem += '@LCL'+'\n'
        assem += 'A=D+M'+'\n'
        assem += 'D=M'+'\n'
        assem += '@SP'+'\n'
        assem += 'AM=M+1'+'\n'
        assem += 'A=A-1'+ '\n'
        assem += 'M=D'+'\n'
        
    if line_elements[1] == 'argument':
        assem  = '@'+ line_elements[2]+'\n'
        assem += 'D=A'+'\n'
        assem += '@ARG'+'\n'
        assem += 'A=D+M'+'\n'
        assem += 'D=M'+'\n'
        assem += '@SP'+'\n'
        assem += 'AM=M+1'+'\n'
        assem += 'A=A-1'+ '\n'
        assem += 'M=D'+'\n'
        
    if line_elements[1] == 'this':
        assem  = '@'+ line_elements[2]+'\n'
        assem += 'D=A'+'\n'
        assem += '@THIS'+'\n'
        assem += 'A=D+M'+'\n'
        assem += 'D=M'+'\n'
        assem += '@SP'+'\n'
        assem += 'AM=M+1'+'\n'
        assem += 'A=A-1'+ '\n'
        assem += 'M=D'+'\n'
        
    if line_elements[1] == 'that':
        assem  = '@'+ line_elements[2]+'\n'
        assem += 'D=A'+'\n'
        assem += '@THAT'+'\n'
        assem += 'A=D+M'+'\n'
        assem += 'D=M'+'\n'
        assem += '@SP'+'\n'
        assem += 'AM=M+1'+'\n'
        assem += 'A=A-1'+ '\n'
        assem += 'M=D'+'\n'
        
    if line_elements[1] == 'temp':
        assem  = '@5'+'\n'
        assem += 'D=A'+'\n'
        assem += '@'+ line_elements[2]+'\n'
        assem += 'A=A+D'+'\n'
        assem += 'D=M'+'\n'
        assem += '@SP'+'\n'
        assem += 'AM=M+1'+'\n'
        assem += 'A=A-1'+ '\n'
        assem += 'M=D'+'\n'
        
    if line_elements[1] == 'static':
        assem  = '@'+ file_initials +'.'+ str(line_elements[2]) +'\n'
        assem += 'D=M'+'\n'
        assem += '@SP'+'\n'
        assem += 'AM=M+1'+'\n'
        assem += 'A=A-1'+ '\n'
        assem += 'M=D'+'\n'
        
    if line_elements[1] == 'pointer':
        if line_elements[2] == '0':
            assem  = '@THIS'+'\n'
        else:
            assem  = '@THAT'+'\n'
        assem += 'D=M'+'\n'
        assem += '@SP'+'\n'
        assem += 'AM=M+1'+'\n'
        assem += 'A=A-1'+ '\n'
        assem += 'M=D'+'\n'
            
    return assem


def get_assem_pop(line_elements, file_initials):
    if line_elements[1] == 'constant':
        print("Cann't pop constant.")
        assem = "// Cann't pop to constant segment."+'\n'
        
    if line_elements[1] in ['local', 'argument','this','that']:
        key_val = {'local'   : 'LCL' ,
                   'argument': 'ARG' ,
                   'this'    : 'THIS',
                   'that'    : 'THAT'}
        
        assem  = '@'+ line_elements[2]+'\n'
        assem += 'D=A'+'\n'
        assem += '@'+ key_val[line_elements[1]] +'\n'
        assem += 'D=M+D'+'\n'
        assem += '@R13' + '\n'
        assem += 'M=D' + '\n'
        assem += '@SP'+'\n'
        assem += 'AM=M-1'+'\n'
        assem += 'D=M'+ '\n'
        assem += '@13' + '\n'
        assem += 'A=M' + '\n'
        assem += 'M=D'+'\n'
        
    if line_elements[1] == 'temp':
        assem  = '@'+ line_elements[2]+'\n'
        assem += 'D=A'+'\n'
        assem += '@5'+'\n'
        assem += 'D=A+D'+'\n'
        assem += '@R13' + '\n'
        assem += 'M=D' + '\n'
        assem += '@SP'+'\n'
        assem += 'AM=M-1'+'\n'
        assem += 'D=M'+ '\n'
        assem += '@13'+ '\n'
        assem += 'A=M'+ '\n'
        assem += 'M=D'+'\n'
        
    if line_elements[1] == 'static':
        assem  = '@SP'+'\n'
        assem += 'AM=M-1'+'\n'
        assem += 'D=M'+ '\n'
        assem += '@'+ file_initials +'.'+ str(line_elements[2]) +'\n'
        assem += 'M=D'+'\n'
        
    if line_elements[1] == 'pointer':
        assem  = '@SP'+'\n'
        assem += 'AM=M-1'+'\n'
        assem += 'D=M'+'\n'
        
        if line_elements[2] == '0':
            assem += '@THIS'+'\n'
        else:
            assem += '@THAT'+'\n'
        assem += 'M=D'+'\n'
    return assem

def get_assem_add():
    assem  = '//add' + '\n'
    assem += '@SP' + '\n'
    assem += 'AM=M-1' + '\n'
    assem += 'D=M' + '\n'
    assem += 'A=A-1' + '\n'
    assem += 'M=M+D' + '\n'
    return assem

def get_assem_sub():
    assem  = '//sub' + '\n'
    assem += '@SP' + '\n'
    assem += 'AM=M-1' + '\n'
    assem += 'D=M' + '\n'
    assem += 'A=A-1' + '\n'
    assem += 'M=M-D' + '\n'
    return assem

def get_assem_and():
    assem  = '//and' + '\n'
    assem += '@SP' + '\n'
    assem += 'AM=M-1' + '\n'
    assem += 'D=M' + '\n'
    assem += 'A=A-1' + '\n'
    assem += 'M=D&M' + '\n'
    return assem

def get_assem_or():
    assem  = '//or' + '\n'
    assem += '@SP' + '\n'
    assem += 'AM=M-1' + '\n'
    assem += 'D=M' + '\n'
    assem += 'A=A-1' + '\n'
    assem += 'M=D|M' + '\n'
    return assem

def get_assem_not():
    assem  = '//not' + '\n'
    assem += '@SP' + '\n'
    assem += 'A=M-1' + '\n'
    assem += 'M=!M' + '\n'
    return assem

def get_assem_neg():
    assem  = '//neg' + '\n'
    assem += '@SP' + '\n'
    assem += 'A=M-1' + '\n'
    assem += 'M=-M' + '\n'
    return assem

def get_assem_eq(label_avail):
    assem  = '//eq' + '\n'
    assem += '@SP' + '\n'
    assem += 'AM=M-1' + '\n'
    assem += 'D=M' + '\n'
    assem += 'A=A-1' + '\n'
    assem += 'D=M-D' + '\n'
    assem += '@lab_'+str(label_avail) + '\n'
    assem += 'D;JEQ' + '\n'
    assem += 'D=1'+ '\n'
    assem += '(lab_'+str(label_avail)+')'+ '\n'
    assem += 'D=D-1'+ '\n'
    assem += '@SP'+ '\n'
    assem += 'A=M-1'+ '\n'
    assem += 'M=D'+ '\n'
    return assem, label_avail+1

def get_assem_gt(label_avail):
    assem  = '//gt' + '\n'
    assem += '@SP' + '\n'
    assem += 'AM=M-1' + '\n'
    assem += 'D=M' + '\n'
    assem += 'A=A-1' + '\n'
    assem += 'D=M-D' + '\n'
    assem += '@lab_'+str(label_avail) + '\n'
    assem += 'D;JGT' + '\n'
    assem += 'D=0'+ '\n'
    assem += '@lab_'+str(label_avail+1) + '\n'
    assem += '0;JMP' + '\n'
    assem += '(lab_'+str(label_avail)+')'+ '\n'
    assem += 'D=-1'+ '\n'
    assem += '(lab_'+str(label_avail+1)+')'+ '\n'
    assem += '@SP'+ '\n'
    assem += 'A=M-1'+ '\n'
    assem += 'M=D'+ '\n'
    return assem, label_avail+2   

def get_assem_lt(label_avail):
    assem  = '//lt' + '\n'
    assem += '@SP' + '\n'
    assem += 'AM=M-1' + '\n'
    assem += 'D=M' + '\n'
    assem += 'A=A-1' + '\n'
    assem += 'D=M-D' + '\n'
    assem += '@lab_'+str(label_avail) + '\n'
    assem += 'D;JLT' + '\n'
    assem += 'D=0'+ '\n'
    assem += '@lab_'+str(label_avail+1) + '\n'
    assem += '0;JMP' + '\n'
    assem += '(lab_'+str(label_avail)+')'+ '\n'
    assem += 'D=-1'+ '\n'
    assem += '(lab_'+str(label_avail+1)+')'+ '\n'
    assem += '@SP'+ '\n'
    assem += 'A=M-1'+ '\n'
    assem += 'M=D'+ '\n'
    return assem, label_avail+2   

def get_assem_from_vm(file_initials, file_clean, prog_assem='', internal_label_avail = 0):    
    
    for fl in file_clean:
        line_elements = fl.split()
        prog_assem += '//'+fl+'\n'
        # push
        if line_elements[0] == 'push':
            prog_assem += get_assem_push(line_elements, file_initials)

        if line_elements[0] == 'pop':
            prog_assem += get_assem_pop(line_elements, file_initials)

        if line_elements[0] == 'add':
            prog_assem += get_assem_add()

        if line_elements[0] == 'sub':
            prog_assem += get_assem_sub()

        if line_elements[0] == 'and':
            prog_assem += get_assem_and()

        if line_elements[0] == 'or':
            prog_assem += get_assem_or()

        if line_elements[0] == 'not':
            prog_assem += get_assem_not()

        if line_elements[0] == 'neg':
            prog_assem += get_assem_neg()

        if line_elements[0] == 'eq':
            prog_assem_temp, internal_label_avail = get_assem_eq(internal_label_avail)
            prog_assem += prog_assem_temp

        if line_elements[0] == 'gt':
            prog_assem_temp, internal_label_avail = get_assem_gt(internal_label_avail)
            prog_assem += prog_assem_temp

        if line_elements[0] == 'lt':
            prog_assem_temp, internal_label_avail = get_assem_lt(internal_label_avail)
            prog_assem += prog_assem_temp
    return prog_assem, internal_label_avail

prog_assem = ''
internal_label_avail = 0
for file_path in vm_files:
    file_clean = get_clean_file(file_path)
    fld_vm, file_vm = os.path.split(file_path)
    file_initials = file_vm[0:file_vm.find('.vm')]
    
    p_temp, lab_temp = get_assem_from_vm(file_initials, file_clean, prog_assem, internal_label_avail)
    prog_assem += p_temp

assem_file = open(output_file, "w")
assem_file.write(prog_assem)
assem_file.close()