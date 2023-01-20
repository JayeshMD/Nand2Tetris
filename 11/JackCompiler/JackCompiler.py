#!/usr/local/bin/python3

import os
import argparse

msg = 'This program compiles the *.vm code.'

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("f_path", help = "Give folder or file path.")
args = parser.parse_args()

file_path_inp = args.f_path

if os.path.isdir(file_path_inp):
    print("Input is the directory.")
    jack_files         = [file_path_inp+'/'+f for f in os.listdir(file_path_inp) if '.jack' in f]
    output_file_tokens = [jf[0:jf.find('.jack')] + 'T.xml' for jf in jack_files]
    output_file        = [jf[0:jf.find('.jack')] +  '.xml' for jf in jack_files]
    output_file_vm     = [jf[0:jf.find('.jack')] +   '.vm' for jf in jack_files]
    
    
elif os.path.isfile(file_path_inp):
    print("Input is the file.")
    jack_files          = [file_path_inp]
    fld_jack, file_jack = os.path.split(file_path_inp)
    file_initials       = file_jack[0:file_jack.find('.jack')]
    output_file_tokens  = [fld_jack + '/'+ file_initials + 'T.xml']
    output_file         = [fld_jack + '/'+ file_initials +  '.xml']
    output_file_vm      = [fld_jack + '/'+ file_initials +   '.vm']

def remove_single_line_comments(file_lines):
    # Removes: // Comment to end of line
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

def remove_multi_line_comments(file_lines):
    # Removes: /* Comment until closing */
    flag = 0                    # flag =0: outside the comment, flag=1: inside the /*...*/ block 
    file_clean = []
    for fl in file_lines:
        if flag==0:
            # The comment has not yet detected
            
            loc_s = fl.find('/*')
            loc_e = fl.find('*/')
            
            # if loc_s > loc_e:
            #     print("Correct the comment using syntax, /* Comment */")
            
            if loc_s==-1 :
                # The comment has not started
                fl_app = fl
            else:
                # The comment has started
                if loc_e == -1:
                    # Comment does not end on the same line 
                    flag = 1
                else:
                    # Comment ends on the same line 
                    fl_app = fl[loc_e+2::]            #========> Change
                    flag = 0
                    
                
            if len(fl_app)>0:
                file_clean.append(fl_app)
        else:
            # Comment has stared 
            loc_e = fl.find('*/')
            if loc_e!=-1 :
                fl_app = fl[loc_e+2::]                 #========> Change
                flag = 0
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
    file_lines_temp = remove_single_line_comments(file_lines)
    file_lines_temp = remove_multi_line_comments(file_lines_temp)
    file_lines_temp = remove_backslash_n(file_lines_temp)
    return file_lines_temp

keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 
            'int'  , 'char'       , 'boolean' , 'void'  , 'true' , 'false' , 'null',
            'this' , 'let'        , 'do'      , 'if'    , 'else' , 'while' , 'return']

symbols = [ '{' , '}' , '(' , ')' , '[' , ']' , '.' ,
            ',' , ';' , '+' , '-' , '*' , '/' , '&' ,
            '|' , '<' , '>' , '=' , '~']

int_cont = [0,32767]


math_op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

math_op_dict = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}

math_op_vm = {'+':'add', '-':'sub','*':'call Math.multiply 2', '/': 'call Math.divide 2', \
              '&':'and', '|':'or' ,'<':'lt', '>': 'gt', '=':'eq'}

math_uni_vm = {'-':'neg', '~':'not'}

#memory_seg_vm = {'var':'local','field':'this','static':'static','argument':'argument'}

def tokenizer(file_clean):
    token_list = []
    word   = ''
    string_flag = False
    for prog_line in file_clean:
        for char_element in prog_line:
            if char_element == '"' and not(string_flag):
                token_list.append('"')
                string_flag = not(string_flag)
            elif char_element == '"' and string_flag:
                 token_list.append(word)
                 token_list.append('"')
                 word = ''
                 string_flag = not(string_flag)
            else:
                if not(string_flag):
                    if ((char_element==' ') or (char_element=='\t')) and len(word)>0:
                        token_list.append(word)
                        word = ''
                    elif (char_element in symbols):
                        if len(word)>0:
                            token_list.append(word)
                            word = ''
                        token_list.append(char_element)
                    elif (char_element!=' ') and (char_element!='\t'): 
                        word += char_element
                else:
                    word += char_element


    xml_list = ['<tokens>']
    token_list_analysed = []
    string_flag = False

    for token in token_list:
        if token in keywords:
            xml_list.append('<keyword> ' + token  + ' </keyword>')
            token_list_analysed.append(['keyword',token])
        elif token in symbols:
            xml_list.append('<symbol> ' + token  + ' </symbol>')
            token_list_analysed.append(['symbol',token])
        else:
            if token=='"':
                string_flag = not(string_flag)
            elif string_flag:
                xml_list.append('<stringConstant> ' + token  + ' </stringConstant>')
                token_list_analysed.append(['stringConstant',token])
            else:
                if token.isnumeric():
                    if 0<=int(token) or int(token)<=32767: 
                        xml_list.append('<integerConstant> ' + token  + ' </integerConstant>')
                        token_list_analysed.append(['integerConstant',token])
                    else:
                        print("Integer constant must be within [0,32767] range but received "+ token)
                else:
                    xml_list.append('<identifier> ' + token  + ' </identifier>')
                    token_list_analysed.append(['identifier',token])
            
    xml_list.append('</tokens>')
    return xml_list, token_list_analysed

'''
type = int, char, boolean, CLASS_NAME, SUBROUTINE_NAME
kind = static, field, argument, var => var is the local variable
index = Non negative integer
'''
class def_identifier:
    def __init__(self, type_a='', kind_a='', index_a=0, category_a=''):
        self.type = type_a
        self.kind = kind_a
        self.index = index_a
        self.category = category_a

    def __repr__(self):
        return '{type:'+self.type+', kind:'+self.kind+', index:'+ str(self.index) + '}'

def varCount(sym_tab, kind):
    count = 0
    for key in sym_tab.keys():
        if sym_tab[key].kind == kind:
            count += 1
    return count

# sym_tab = {}
# sym_tab['x'] = def_identifier(type='int',kind='field', index = 0)
# sym_tab['y'] = def_identifier(type='int',kind='field', index = 1)
# sym_tab['z'] = def_identifier(type='Point',kind='argument', index = 0) 

class CompilationEngine:
    def __init__(self, token_list_analysed):
        self.token_list_analysed = token_list_analysed
        self.token_index = 0 
        self.parsed_list = []
        self.class_name = ''
        self.kind_of_subroutine = ''
        self.subroutine_name = ''
        self.symbol_tab_class = {}
        self.symbol_tab_subroutine = {}
        self.vm_code = []
        self.num_of_expressions = 0
        self.label_count = 0
        self.return_type = ''
        
    def compileClass(self):
        if self.token_list_analysed[self.token_index][1] == 'class':
            self.parsed_list.append('<class>')
            
            self.eat_var(['class'])             # Check for class keyword
            self.class_name = self.token_list_analysed[self.token_index][1]
            #print("Class name:", self.class_name)
            self.eat_type(['identifier'])       # Check for the class name
            self.eat_var(['{'])                 # Check for opening curly bracket
            
            self.compileClassVarDec()
            while self.token_index < (len(self.token_list_analysed)-1):
                self.compileSubroutine()
            
            self.eat_var(['}'])
            self.parsed_list.append('</class>')
        
        else:
            print(self.token_list_analysed[self.token_index][1] + ' must be class.')

        #==========>
        #print(self.vm_code)
        #==========>
        return
    
    
    #======================================================================================
    # Complie the fields, static or class objects declared at the start of class 
    #======================================================================================
    def compileClassVarDec(self):
        
        while self.token_list_analysed[self.token_index][1] in ['field', 'static']:
            self.parsed_list.append('<classVarDec>')
            kind_a = self.token_list_analysed[self.token_index][1]
            self.eat_type(['keyword'])         # Check keywods. Already field or static is checked

            # Check type of variable
            if self.token_list_analysed[self.token_index][0] == 'keyword':
                type_a = self.token_list_analysed[self.token_index][1]
                self.eat_var(['int', 'char', 'boolean'])
            else:
                type_a = self.token_list_analysed[self.token_index][1]
                self.eat_type(['identifier'])

            index_a = varCount(self.symbol_tab_class, kind_a)    

            flag_end_line = False
            # Check the variables
            while not(flag_end_line) and self.token_list_analysed[self.token_index][0] == 'identifier':
                var_name = self.token_list_analysed[self.token_index][1]
                self.eat_type(['identifier'])
                index_a = varCount(self.symbol_tab_class, kind_a)
                self.symbol_tab_class[var_name] = def_identifier(type_a=type_a, kind_a=kind_a, index_a=index_a)
                if self.token_list_analysed[self.token_index][1] == ';':
                    flag_end_line = True
                    
                self.eat_var([',',';'])
            self.parsed_list.append('</classVarDec>')

        #========>    
        #print(self.symbol_tab_class)
        #========>
        return
    
    def compileSubroutine(self):  
        self.symbol_tab_subroutine = {}
        self.parsed_list.append('<subroutineDec>')

        #=====>
        self.kind_of_subroutine = self.token_list_analysed[self.token_index][1]
        if self.kind_of_subroutine == 'method':
            self.symbol_tab_subroutine['this'] = def_identifier(type_a = self.class_name, kind_a = 'argument', index_a = 0)
        #=====>
        
        self.eat_var(['constructor', 'function', 'method'])            # Check subroutine type
        
        #=======>
        self.return_type =  self.token_list_analysed[self.token_index][1]
        #=======>
        
        if self.token_list_analysed[self.token_index][0] == 'keyword': # Check type of variable
            self.eat_var(['void', 'int', 'char', 'boolean'])
        else:
            self.eat_type(['identifier'])

        self.subroutine_name = self.token_list_analysed[self.token_index][1]

        self.eat_type(['identifier'])                                  # Check for subroutine name
        self.eat_var(['('])                                            # Check opening bracket (
        self.compileParameterList()                                    # Check parameter list
        self.eat_var([')'])                                            # Check closing bracket )
        self.compileSubroutineBody()                                   # Check subroutine body
        self.parsed_list.append('</subroutineDec>')

        #======>
        #print("Subroutine name:", self.subroutine_name)
        #print("Symbol table:", self.symbol_tab_subroutine)
        #======>
        return
    
    def compileParameterList(self):
        self.parsed_list.append('<parameterList>')
        while self.token_list_analysed[self.token_index][0] in ['keyword', 'identifier']:

            kind_a = 'argument'
            type_a = self.token_list_analysed[self.token_index][1]

            self.eat_type(['keyword', 'identifier'])
            
            # Check variable name
            var_name = self.token_list_analysed[self.token_index][1]
            index_a = varCount(self.symbol_tab_subroutine, kind_a)
            self.symbol_tab_subroutine[var_name] = def_identifier(type_a=type_a, kind_a=kind_a, index_a=index_a)

            self.eat_type(['identifier'])
            var_name = self.token_list_analysed[self.token_index][1]
            # Check the variables
            if self.token_list_analysed[self.token_index][1]==',':
                self.eat_var([','])
            
        self.parsed_list.append('</parameterList>')
        return
    
    def compileSubroutineBody(self):
        self.parsed_list.append('<subroutineBody>')
        self.eat_var(['{'])
        self.compileVarDec()

        #==================>
        if self.kind_of_subroutine in ['function']:
            n_locals = varCount(self.symbol_tab_subroutine, 'local')
            self.vm_code.append('function '+ self.class_name+'.'+ \
                                self.subroutine_name+' '+ str(n_locals))

        if self.kind_of_subroutine in ['constructor']:
            n_locals = varCount(self.symbol_tab_subroutine, 'local')
            self.vm_code.append('function '+ self.class_name+'.'+ \
                                self.subroutine_name+' '+ str(n_locals))
            n_fields = varCount(self.symbol_tab_class, 'field')
            self.vm_code.append('push constant '+str(n_fields))
            self.vm_code.append('call Memory.alloc 1')
            self.vm_code.append('pop pointer 0')  

        if self.kind_of_subroutine in ['method']:
            n_locals = varCount(self.symbol_tab_subroutine, 'local')
            self.vm_code.append('function '+ self.class_name+'.'+ \
                                self.subroutine_name+' '+ str(n_locals))
            self.vm_code.append('push argument 0')
            self.vm_code.append('pop pointer 0')

        #==================>


        self.compileStatements()
        self.eat_var(['}'])
        self.parsed_list.append('</subroutineBody>')

        #============>
        #self.vm_code.append('push pointer 0') 
        #============>
        
        return
    
    def compileVarDec(self):
        
        while self.token_list_analysed[self.token_index][1] in ['var']:
            self.parsed_list.append('<varDec>')
            self.eat_type(['keyword'])         # Check keywods. Already var is checked

            #=====>
            kind_a = 'local'
            #=====>
            # Check type of variable
            if self.token_list_analysed[self.token_index][0] == 'keyword':
                #=====>
                type_a = self.token_list_analysed[self.token_index][1]
                #=====>
                self.eat_var(['int', 'char', 'boolean']) 
            else:
                #=====>
                type_a = self.token_list_analysed[self.token_index][1]
                #=====>
                self.eat_type(['identifier'])
                
            flag_end_line = False
            # Check the variables
            while not(flag_end_line) and self.token_list_analysed[self.token_index][0] == 'identifier':
                #=====>
                var_name = self.token_list_analysed[self.token_index][1]
                index_a = varCount(self.symbol_tab_subroutine, kind_a)
                self.symbol_tab_subroutine[var_name] = def_identifier(type_a=type_a, kind_a=kind_a, index_a = index_a)
                #=====>
                self.eat_type(['identifier'])
                if self.token_list_analysed[self.token_index][1] == ';':
                    flag_end_line = True
                    
                self.eat_var([',',';'])
            self.parsed_list.append('</varDec>')
        return
    
    def compileStatements(self):
        self.parsed_list.append('<statements>')
        while self.token_list_analysed[self.token_index][1] in ['let', 'if', 'while', 'do', 'return']:
            if self.token_list_analysed[self.token_index][1] == 'let'   :  self.compileLet()
            if self.token_list_analysed[self.token_index][1] == 'if'    :  self.compileIf()
            if self.token_list_analysed[self.token_index][1] == 'while' :  self.compileWhile()
            if self.token_list_analysed[self.token_index][1] == 'do'    :  self.compileDo()
            if self.token_list_analysed[self.token_index][1] == 'return':  self.compileReturn()
        self.parsed_list.append('</statements>')
        return
    
    def compileLet(self):
        self.parsed_list.append('<letStatement>')
        self.eat_var(['let'])

        #=======>
        name = self.token_list_analysed[self.token_index][1] 
        arr_assignment = False
        #=======>
        self.eat_type(['identifier'])

        if self.token_list_analysed[self.token_index][1] == '[':
            #===========>
            arr_assignment = True
            segment_a, index_a = self.get_seg_idx(name)
            self.vm_code.append("push "+ segment_a + ' '+ str(index_a))
            #===========>
            self.eat_var(['['])
            self.compileExpression()
            self.eat_var([']'])
            
            #===========>
            self.vm_code.append('add')
            #===========>
        self.eat_var(['='])
        self.compileExpression()
        self.eat_var([';'])
        self.parsed_list.append('</letStatement>')

        #===========>
        #print(name)
        if arr_assignment:
            self.vm_code.append('pop temp 0')
            self.vm_code.append('pop pointer 1')
            self.vm_code.append('push temp 0')
            self.vm_code.append('pop that 0')
        else:    
            segment_a, index_a = self.get_seg_idx(name)
            self.writePop(segment=segment_a, index=index_a)
        #===========>
        return
    
    def compileIf(self):
        self.parsed_list.append('<ifStatement>')
        self.eat_var(['if'])
        self.eat_var(['('])
        self.compileExpression()
        self.eat_var([')'])

        #==========>
        label_count = self.label_count
        self.label_count += 2
        self.vm_code.append('not')
        self.vm_code.append('if-goto LABEL_'+str(label_count))
        #==========>

        self.eat_var(['{'])
        self.compileStatements()
        self.eat_var(['}'])
        
        #==========>
        self.vm_code.append('goto LABEL_'+str(label_count+1))
        self.vm_code.append('label LABEL_'+str(label_count))
        #==========>

        if self.token_list_analysed[self.token_index][1]=='else':
            self.eat_var(['else'])
            self.eat_var(['{'])
            self.compileStatements()
            self.eat_var(['}'])
        self.parsed_list.append('</ifStatement>')

        #==========>
        self.vm_code.append('label LABEL_'+str(label_count+1))
        #==========>
        return
    
    def compileWhile(self):
        #==========>
        label_count = self.label_count
        self.label_count += 2
        #==========>

        #==========>
        self.vm_code.append('label LABEL_'+str(label_count))
        #==========>
        self.parsed_list.append('<whileStatement>')
        self.eat_var(['while'])
        self.eat_var(['('])
        self.compileExpression()
        self.eat_var([')'])

        #==========>
        self.vm_code.append('not')
        self.vm_code.append('if-goto LABEL_'+str(label_count+1))
        #==========>

        self.eat_var(['{'])
        self.compileStatements()
        self.eat_var(['}'])
        self.parsed_list.append('</whileStatement>')

        #==========>
        self.vm_code.append('goto LABEL_'+str(label_count))
        self.vm_code.append('label LABEL_'+str(label_count+1))
        #==========>
        
        return
    
    def compileDo(self):
        self.parsed_list.append('<doStatement>')
        self.eat_var(['do'])
        
        #=======>
        object_flag = False
        if self.token_list_analysed[self.token_index+1][1]=='.':
            name = self.token_list_analysed[self.token_index][1]

            # Checks if the current identifier is object calling method or call to class function
            if name in self.symbol_tab_subroutine.keys():
                # It is call to a method by subroutine level object

                segment_a, index_a = self.get_seg_idx(name)
                self.vm_code.append('push '+ segment_a + ' ' +str(index_a))
                vm_code_temp  = 'call '
                vm_code_temp += self.symbol_tab_subroutine[name].type + '.'
                vm_code_temp += self.token_list_analysed[self.token_index+2][1]
                object_flag = True
            elif (name in self.symbol_tab_class) and (self.kind_of_subroutine!='function'):
                # it is a call to method by class level object
                segment_a, index_a = self.get_seg_idx(name)
                self.vm_code.append('push '+ segment_a + ' ' +str(index_a))
                vm_code_temp  = 'call '
                vm_code_temp += self.symbol_tab_class[name].type + '.'
                vm_code_temp += self.token_list_analysed[self.token_index+2][1]
                object_flag = True
            elif name in self.symbol_tab_class: # Check the corectness hopefully it will handle static objects
                if self.symbol_tab_class[name].type == 'static':
                    segment_a, index_a = self.get_seg_idx(name)
                    self.vm_code.append('push '+ segment_a + ' ' +str(index_a))
                    vm_code_temp  = 'call '
                    vm_code_temp += self.symbol_tab_class[name].type + '.'
                    vm_code_temp += self.token_list_analysed[self.token_index+2][1]
                    object_flag = True
            else:
                # Already in required form class_name.function or class_name.method 
                vm_code_temp = 'call '+ self.token_list_analysed[self.token_index  ][1] \
                                      + self.token_list_analysed[self.token_index+1][1] \
                                      + self.token_list_analysed[self.token_index+2][1]

        else:
            self.vm_code.append('push pointer 0')
            vm_code_temp = 'call '+ self.class_name +'.'+self.token_list_analysed[self.token_index][1]
            object_flag = True
        #=======>

        self.eat_type(['identifier'])
        
        if self.token_list_analysed[self.token_index][1] == '.':
            
            self.eat_var(['.'])
            
            #=======>
            #vm_code_temp += '.'+self.token_list_analysed[self.token_index][1]
            #=======>
            
            self.eat_type(['identifier'])
            
        self.eat_var(['('])
        self.compileExpressionList()

        self.eat_var(')')
        self.eat_var([';'])
        self.parsed_list.append('</doStatement>')

        #===========>
        if object_flag: self.num_of_expressions += 1
        vm_code_temp += ' '+ str(self.num_of_expressions)
        self.vm_code.append(vm_code_temp)
        self.vm_code.append('pop temp 0')
        #===========>
        return
    
    def compileReturn(self):
        self.parsed_list.append('<returnStatement>')
        
        #============>
        if self.return_type == 'void':
            self.vm_code.append('push constant 0')
        #============>

        self.eat_var(['return'])
        
        if self.token_list_analysed[self.token_index][1]!=';':
            self.compileExpression()
            
        self.eat_var([';'])
        
        self.parsed_list.append('</returnStatement>')

        #========>
        self.vm_code.append('return')
        #========>

        return
    
    def compileExpression(self):
        self.parsed_list.append('<expression>')
        self.compileTerm()
        
        while self.token_list_analysed[self.token_index][1] in math_op:

            #========>
            math_op_temp = self.token_list_analysed[self.token_index][1]
            #========>

            if self.token_list_analysed[self.token_index][1] in math_op_dict.keys():
                self.parsed_list.append('<'  +self.token_list_analysed[self.token_index][0]+'> ' 
                                             +math_op_dict[self.token_list_analysed[self.token_index][1]]+ 
                                        ' </'+self.token_list_analysed[self.token_index][0]+'>')
                self.token_index += 1
                self.compileTerm()
            else:
                self.eat_var(math_op)
                self.compileTerm()

            #==========>
            self.vm_code.append(math_op_vm[math_op_temp])
            #==========>

        self.parsed_list.append('</expression>')
        return
    
    def compileTerm(self):
        self.parsed_list.append('<term>')
        if  self.token_list_analysed[self.token_index][0] in ['integerConstant', 'stringConstant']:
            
            #========>
            if self.token_list_analysed[self.token_index][0] == 'integerConstant':
                self.vm_code.append('push constant '+self.token_list_analysed[self.token_index][1])
            elif self.token_list_analysed[self.token_index][0] == 'stringConstant':
                str_temp = self.token_list_analysed[self.token_index][1]
                self.vm_code.append('push constant '+ str(len(str_temp)))
                self.vm_code.append('call String.new 1')
                for s in str_temp:
                    self.vm_code.append('push constant '+ str(ord(s)))
                    self.vm_code.append('call String.appendChar 2')
            #========>
            
            self.eat_type(['integerConstant', 'stringConstant'])
        elif self.token_list_analysed[self.token_index][1]=='(':
            self.eat_var(['('])
            self.compileExpression()
            self.eat_var([')'])
        elif self.token_list_analysed[self.token_index][1] in ['-','~']:
            
            #========>
            math_op_temp = self.token_list_analysed[self.token_index][1]
            #========>
        
            self.eat_var(['-','~'])
            self.compileTerm()

            #==========>
            self.vm_code.append(math_uni_vm[math_op_temp])
            #==========>

        elif self.token_list_analysed[self.token_index][0] in ['keyword']:
            
            #==========>
            if self.token_list_analysed[self.token_index][1] in ['true', 'false', 'null', 'this']:
                if self.token_list_analysed[self.token_index][1] in ['false','null']:
                    self.vm_code.append('push constant 0')
                if self.token_list_analysed[self.token_index][1] in ['true']:
                    self.vm_code.append('push constant 0')
                    self.vm_code.append('not')
                if self.token_list_analysed[self.token_index][1] in ['this']:
                    self.vm_code.append('push pointer 0')
            #==========>
            
            self.eat_var(['true', 'false', 'null', 'this'])

        elif self.token_list_analysed[self.token_index][0] in ['identifier']:
            #==========>
            name = self.token_list_analysed[self.token_index][1]
            #==========>
            if self.token_list_analysed[self.token_index+1][1] == '[':
                #==========>
                segment_a, index_a = self.get_seg_idx(name)
                self.vm_code.append("push "+ segment_a + ' '+ str(index_a))
                #==========>
                self.eat_type(['identifier'])
                self.eat_var(['['])
                self.compileExpression()
                self.eat_var([']'])

                #==========>
                self.vm_code.append("add")
                self.vm_code.append("pop pointer 1")
                self.vm_code.append("push that 0")
                #==========>
            elif self.token_list_analysed[self.token_index+1][1] == '(':
                name  = self.class_name
                name += '.'+self.token_list_analysed[self.token_index][1]
                self.eat_type(['identifier'])
                self.eat_var(['('])
                self.compileExpressionList()
                self.eat_var([')'])
                
                self.writeCall(name=name, n_args= self.num_of_expressions)

            elif self.token_list_analysed[self.token_index+1][1] == '.':
                
                #=======>
                object_flag = False
                if self.token_list_analysed[self.token_index+1][1]=='.':
                    name = self.token_list_analysed[self.token_index][1]

                    # Checks if the current identifier is object calling method or call to class function
                    if name in self.symbol_tab_subroutine.keys():
                        # It is call to a method by subroutine level object

                        segment_a, index_a = self.get_seg_idx(name)
                        self.vm_code.append('push '+ segment_a + ' ' +str(index_a))
                        vm_code_temp  = 'call '
                        vm_code_temp += self.symbol_tab_subroutine[name].type + '.'
                        vm_code_temp += self.token_list_analysed[self.token_index+2][1]
                        object_flag = True
                    elif (name in self.symbol_tab_class) and (self.kind_of_subroutine!='function'):
                        # it is a call to method by class level object
                        segment_a, index_a = self.get_seg_idx(name)
                        self.vm_code.append('push '+ segment_a + ' ' +str(index_a))
                        vm_code_temp  = 'call '
                        vm_code_temp += self.symbol_tab_class[name].type + '.'
                        vm_code_temp += self.token_list_analysed[self.token_index+2][1]
                        object_flag = True
                    elif name in self.symbol_tab_class: # Check the corectness hopefully it will handle static objects
                        if self.symbol_tab_class[name].type == 'static':
                            segment_a, index_a = self.get_seg_idx(name)
                            self.vm_code.append('push '+ segment_a + ' ' +str(index_a))
                            vm_code_temp  = 'call '
                            vm_code_temp += self.symbol_tab_class[name].type + '.'
                            vm_code_temp += self.token_list_analysed[self.token_index+2][1]
                            object_flag = True
                    else:
                        # Already in required form class_name.function or class_name.method 
                        vm_code_temp = 'call '+ self.token_list_analysed[self.token_index  ][1] \
                                            + self.token_list_analysed[self.token_index+1][1] \
                                            + self.token_list_analysed[self.token_index+2][1]

                else:
                    self.vm_code.append('push pointer 0')
                    vm_code_temp = 'call '+ self.class_name +'.'+self.token_list_analysed[self.token_index][1]
                    object_flag = True
                #=======>

                self.eat_type(['identifier'])
                self.eat_var(['.'])
                #=======>
                #name += '.'+self.token_list_analysed[self.token_index][1]
                #=======>
                self.eat_type(['identifier'])
                self.eat_var(['('])
                self.compileExpressionList()
                self.eat_var([')'])

                #===========>
                if object_flag: self.num_of_expressions += 1
                vm_code_temp += ' '+ str(self.num_of_expressions)
                self.vm_code.append(vm_code_temp)
                #===========>


                #self.writeCall(name=name, n_args= self.num_of_expressions)

            else:
                self.eat_type(['identifier'])
                segment_a, index_a = self.get_seg_idx(name)
                self.writePush(segment= segment_a, index= index_a)
        
        self.parsed_list.append('</term>')

        return
    
    def compileExpressionList(self):
        #=========>
        self.num_of_expressions = 0
        #=========>
        self.parsed_list.append('<expressionList>')
        while self.token_list_analysed[self.token_index][1] != ')':
            #===========>
            self.num_of_expressions +=1
            #===========>
            self.compileExpression()
            if self.token_list_analysed[self.token_index][1] == ',':
                self.eat_var([','])
        self.parsed_list.append('</expressionList>')
        return
    
    #===================================================================================
    # VM writer
    #===================================================================================
    #==========>
    def writePush(self, segment, index):
        self.vm_code.append('push '+ segment + ' '+ str(index))
        return

    def writePop(self, segment, index):
        self.vm_code.append('pop '+ segment + ' '+ str(index))
        return

    #def writeArithmetic():

    def writeLabel(self,label):
        self.vm_code.append('('+label+')')
        return

    def writeGoto(self,label):
        self.vm_code.append('goto '+ label)
        return

    #def writeIf(self,label):


    def writeCall(self, name, n_args):
        self.vm_code.append('call '+ name + ' '+ str(n_args))
        return

    def writeFunction(self, name, n_local):
        self.vm_code.append('function '+ name + ' '+ str(n_local))
        return

    def writeReturn(self):
        self.vm_code.append('return ')
        return

    #Helping function
    def get_seg_idx(self, name):
        segment_a = None 
        index_a = None
        if name in self.symbol_tab_subroutine.keys():
            segment_a = self.symbol_tab_subroutine[name].kind
            index_a   = self.symbol_tab_subroutine[name].index
        elif (name in self.symbol_tab_class.keys()) and (self.kind_of_subroutine!='function'):
            segment_a = self.symbol_tab_class[name].kind
            index_a   = self.symbol_tab_class[name].index
        elif name in self.symbol_tab_class.keys():
            if self.symbol_tab_class[name].kind == 'static':
                segment_a = self.symbol_tab_class[name].kind
                index_a   = self.symbol_tab_class[name].index
        else:   
            print("Variable " + name +" is undefined.")

        if segment_a == 'field': segment_a = 'this'

        return segment_a, index_a
    #==========>
    
    #===================================================================================
    # Common methods
    #===================================================================================
    def append_xml(self):
        self.parsed_list.append('<'  +self.token_list_analysed[self.token_index][0]+'> ' 
                                     +self.token_list_analysed[self.token_index][1]+ 
                                ' </'+self.token_list_analysed[self.token_index][0]+'>')
        self.token_index += 1
        return
    
    def eat_type(self, word_list):
        if self.token_list_analysed[self.token_index][0] in word_list:
            self.append_xml()
        else:
            print("Error: expected "+ '['+'| '.join(word_list)+' ]'+ ' but received '+ self.token_list_analysed[self.token_index][1])
            self.token_index += 1
        return
    
    def eat_var(self, word_list):
        if self.token_list_analysed[self.token_index][1] in word_list:
            self.append_xml()
        else:
            print("Error: expected "+ '['+'| '.join(word_list)+' ]'+ ' but received '+ self.token_list_analysed[self.token_index][1])
            self.token_index += 1
        return


#=============Processing file===============

count = 0 

for count in range(len(jack_files)):
    file_path = jack_files[count]    
    file_clean = get_clean_file(file_path)
    
    xml_list, token_list_analysed = tokenizer(file_clean)

    xml_file = open(output_file_tokens[count], "w")
    xml_file.write('\n'.join(xml_list))
    xml_file.close()


    comp_eng = CompilationEngine(token_list_analysed)
    comp_eng.compileClass()

    xml_file = open(output_file[count], "w")
    xml_file.write('\n'.join(comp_eng.parsed_list))
    xml_file.close()

    vm_file = open(output_file_vm[count], "w")
    vm_file.write('\n'.join(comp_eng.vm_code))
    vm_file.close()

