#!/usr/local/bin/python3

import os
import argparse

msg = 'This program compiles the *.vm code without brancing commands'



parser = argparse.ArgumentParser(description = msg)
parser.add_argument("f_path", help = "Give folder or file path.")
args = parser.parse_args()

file_path_inp = args.f_path

if os.path.isdir(file_path_inp):
    vm_files_temp = [f for f in os.listdir(file_path_inp) if '.vm' in f]
    if 'Sys.vm' in vm_files_temp:
        vm_files_temp.remove('Sys.vm')
        vm_files_temp.insert(0, 'Sys.vm')
    
    vm_files = [file_path_inp+'/'+ vm_f for vm_f in vm_files_temp]
    

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
    assem  = '@SP' + '\n'
    assem += 'AM=M-1' + '\n'
    assem += 'D=M' + '\n'
    assem += 'A=A-1' + '\n'
    assem += 'M=M+D' + '\n'
    return assem

def get_assem_sub():
    assem  = '@SP' + '\n'
    assem += 'AM=M-1' + '\n'
    assem += 'D=M' + '\n'
    assem += 'A=A-1' + '\n'
    assem += 'M=M-D' + '\n'
    return assem

def get_assem_and():
    assem  = '@SP' + '\n'
    assem += 'AM=M-1' + '\n'
    assem += 'D=M' + '\n'
    assem += 'A=A-1' + '\n'
    assem += 'M=D&M' + '\n'
    return assem

def get_assem_or():
    assem  = '@SP' + '\n'
    assem += 'AM=M-1' + '\n'
    assem += 'D=M' + '\n'
    assem += 'A=A-1' + '\n'
    assem += 'M=D|M' + '\n'
    return assem

def get_assem_not():
    assem  = '@SP' + '\n'
    assem += 'A=M-1' + '\n'
    assem += 'M=!M' + '\n'
    return assem

def get_assem_neg():
    assem  = '@SP' + '\n'
    assem += 'A=M-1' + '\n'
    assem += 'M=-M' + '\n'
    return assem

def get_assem_eq(label_avail):
    assem  = '@SP' + '\n'
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
    assem  = '@SP' + '\n'
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
    assem  = '@SP' + '\n'
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

# Part 2
def get_assem_label(label):
    assem = '('+label+')' + '\n'
    return assem

def get_assem_if_goto(label):
    assem  = '@SP'+ '\n'
    assem += 'AM=M-1'+ '\n'
    assem += 'D=M'+ '\n'
    assem += '@'+label+ '\n'
    assem += 'D; JNE' + '\n'
    return assem

def get_assem_goto(label):
    assem  = '@'+label+ '\n'
    assem += '0; JMP' + '\n'
    return assem

def get_assem_function(line_elements):
    assem = '('+line_elements[1]+')' + '\n'
    # Push SP value into LCL
    assem += '@SP'+ '\n'
    assem += 'D=M'+ '\n'
    assem += '@LCL'+ '\n'
    assem += 'M=D'+ '\n'

    #Initializing local memory segment
    assem += '@0'+ '\n'
    assem += 'D=A'+ '\n'
    assem += '@SP'+ '\n'    # Can be removed but makes implementation robust as SP may not be 0 in general
    assem += 'A=M'+ '\n'
    for i in range(int(line_elements[2])):
        assem += 'M=D'+ '\n'
        assem += 'A=A+1'+ '\n'
    assem += 'D=A'+ '\n'
    assem += '@SP'+ '\n'
    assem += 'M=D'+ '\n'
    return assem

def get_assem_return(line_elements):
    # Save return address in R14
    assem  = '@LCL'+ '\n'
    assem += 'D=M'+ '\n'
    assem += '@5'+ '\n'
    assem += 'A=D-A'+ '\n'
    assem += 'D=M'+ '\n'
    assem += '@R14'+ '\n'
    assem += 'M=D'+ '\n'

    # Copy return value to ARG[0]
    assem += '@SP' + '\n'
    assem += 'A=M-1' + '\n'
    assem += 'D=M'+ '\n'
    assem += '@ARG'+ '\n'
    assem += 'A=M'+ '\n'
    assem += 'M=D'+ '\n'
    assem += 'D=A+1'+ '\n'
    assem += '@SP'+ '\n'
    assem += 'M=D'+ '\n'

    # Restore memory segments pointers
    assem += '@LCL' + '\n'
    assem += 'D=M'+ '\n'
    assem += '@R13'+ '\n'
    assem += 'AM=D'+ '\n'
    ['THAT','THIS','ARG','LCL']
    for mem_ptr in ['THAT','THIS','ARG','LCL']:
        assem += '@R13'+ '\n'
        assem += 'AM=M-1'+ '\n'
        assem += 'D=M'+ '\n'
        assem += '@'+mem_ptr + '\n'
        assem += 'M=D'+ '\n'

    

    #Jump to return location
    assem += '@R14'+ '\n'
    assem += 'A=M'+ '\n'
    assem += '0;JMP'+ '\n'

    return assem

def get_assem_call(line_elements, call_count):
    
    # Get return address
    # Copy all memory segment pointers
    # Jump to foo
    
    # Find ARG for callee and store in R13
    assem  = '@SP'+ '\n'
    assem += 'D=M'+ '\n'
    assem += '@'+line_elements[2]+ '\n'
    assem += 'D=D-A'+ '\n'
    assem += '@R13'+ '\n'
    assem += 'M=D'+ '\n'

    # Push return address
    assem += '@'+line_elements[1]+'_return_'+str(call_count)+ '\n'
    assem += 'D=A'+ '\n'
    assem += '@SP'+ '\n'
    assem += 'AM=M+1'+ '\n'
    assem += 'A=A-1'+ '\n'
    assem += 'M=D'+ '\n'

    for mem_ptr in ['LCL','ARG','THIS','THAT']: 
        assem += '@'+ mem_ptr+ '\n'
        assem += 'D=M'+ '\n'
        assem += '@SP'+ '\n'
        assem += 'AM=M+1'+ '\n'
        assem += 'A=A-1'+ '\n'
        assem += 'M=D'+ '\n'

    # Copy ARG value for calle from R13 into ARG
    assem += '@R13'+ '\n'
    assem += 'D=M'+ '\n'
    assem += '@ARG'+ '\n'
    assem += 'M=D'+ '\n'

    #assem += '@SP'+ '\n'
    #assem += 'AM=M+1'+ '\n'
    assem += '@'+line_elements[1]+ '\n'
    assem += '0;JMP'+ '\n'
    assem += '('+line_elements[1]+'_return_'+str(call_count)+')'+ '\n'

    call_count +=1

    return assem, call_count
    

    

def get_assem_from_vm(file_initials, file_clean, prog_assem='', internal_label_avail = 0, call_count=0):    
    
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

        # Part 2
        if line_elements[0] == 'label':
            prog_assem += get_assem_label(line_elements[1])

        if line_elements[0] == 'if-goto':
            prog_assem += get_assem_if_goto(line_elements[1])

        if line_elements[0] == 'goto':
            prog_assem += get_assem_goto(line_elements[1])

        if line_elements[0] == 'function':
            prog_assem += get_assem_function(line_elements)

        if line_elements[0] == 'return':
            prog_assem += get_assem_return(line_elements)

        if line_elements[0] == 'call':
            prog_assem_temp, call_count = get_assem_call(line_elements, call_count)
            prog_assem += prog_assem_temp

    return prog_assem, internal_label_avail, call_count

prog_assem = ''
internal_label_avail = 0
call_count = 0


for file_path in vm_files:
    
    file_clean = get_clean_file(file_path)
    fld_vm, file_vm = os.path.split(file_path)
    file_initials = file_vm[0:file_vm.find('.vm')]
    prog_assem, internal_label_avail, call_count = get_assem_from_vm(file_initials, file_clean, prog_assem, internal_label_avail, call_count)

assem_file = open(output_file, "w")
assem_file.write(prog_assem)
assem_file.close()