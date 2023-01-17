import os
import argparse

msg = 'This program compiles the *.vm code.'

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("f_path", help = "Give folder or file path.")
args = parser.parse_args(["/Users/jayeshdhadphale/Desktop/All_jayesh/Study/My_Computer/nand2tetris/projects/10/test"])

# /Users/jayeshdhadphale/Desktop/All_jayesh/Study/My_Computer/nand2tetris/projects/10/test/

file_path_inp = args.f_path

if os.path.isdir(file_path_inp):
    print("Input is the directory.")
    jack_files         = [file_path_inp+'/'+f for f in os.listdir(file_path_inp) if '.jack' in f]
    output_file_tokens = [jf[0:jf.find('.jack')] + 'T.xml' for jf in jack_files]
    output_file        = [jf[0:jf.find('.jack')] + '.xml' for jf in jack_files]
    
    
elif os.path.isfile(file_path_inp):
    print("Input is the file.")
    jack_files          = [file_path_inp]
    fld_jack, file_jack = os.path.split(file_path_inp)
    file_initials       = file_jack[0:file_jack.find('.jack')]
    output_file_tokens  = [fld_jack + '/'+ file_initials + 'T.xml']
    output_file         = [fld_jack + '/'+ file_initials + '.xml']
    

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
            
            if loc_s > loc_e:
                print("Correct the comment using syntax, /* Comment */")
            
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
                    if (char_element==' ') and len(word)>0:
                        token_list.append(word)
                        word = ''
                    elif (char_element in symbols):
                        if len(word)>0:
                            token_list.append(word)
                            word = ''
                        token_list.append(char_element)
                    elif (char_element!=' '): 
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
                    xml_list.append('<integerConstant> ' + token  + ' </integerConstant>')
                    token_list_analysed.append(['integerConstant',token])
                else:
                    xml_list.append('<identifier> ' + token  + ' </identifier>')
                    token_list_analysed.append(['identifier',token])
            
    xml_list.append('</tokens>')
    return xml_list, token_list_analysed


"""
'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 
'int'  , 'char'       , 'boolean' , 'void'  , 'true' , 'false' , 'null',
'this' , 'let'        , 'do'      , 'if'    , 'else' , 'while' , 'return'
"""

class CompilationEngine:
    def __init__(self, token_list_analysed):
        self.token_list_analysed = token_list_analysed
        self.token_index = 0 
        self.parsed_list = []
        
    def compileClass(self):
        if self.token_list_analysed[self.token_index][1] == 'class':
            self.parsed_list.append('<class>')
            
            self.eat_var(['class'])             # Check for class keyword
            self.eat_type(['identifier'])       # Check for the class name
            self.eat_var(['{'])                 # Check for opening curly bracket
            
            self.compileClassVarDec()
            while self.token_index < (len(self.token_list_analysed)-1):
                self.compileSubroutine()
            
            self.eat_var(['}'])
            self.parsed_list.append('</class>')
        
        else:
            print(self.token_list_analysed[self.token_index][1] + ' must be class.')
        
        return
    
    
    #======================================================================================
    # Complie the fields, static or class objects declared at the start of class 
    #======================================================================================
    def compileClassVarDec(self):
        
        while self.token_list_analysed[self.token_index][1] in ['field', 'static']:
            self.parsed_list.append('<classVarDec>')
            self.eat_type(['keyword'])         # Check keywods. Already field or static is checked

            # Check type of variable
            if self.token_list_analysed[self.token_index][0] == 'keyword':
                self.eat_var(['int', 'char', 'boolean'])
                
            else:
                self.eat_type(['identifier'])
                

            flag_end_line = False
            # Check the variables
            while not(flag_end_line) and self.token_list_analysed[self.token_index][0] == 'identifier':
                self.eat_type(['identifier'])

                if self.token_list_analysed[self.token_index][1] == ';':
                    flag_end_line = True
                    
                self.eat_var([',',';'])
            self.parsed_list.append('</classVarDec>')
        
        return
    
    def compileSubroutine(self):    
        self.parsed_list.append('<subroutineDec>')

        self.eat_var(['constructor', 'function', 'method'])            # Check subroutine type
        if self.token_list_analysed[self.token_index][0] == 'keyword': # Check type of variable
            self.eat_var(['void', 'int', 'char', 'boolean'])
        else:
            self.eat_type(['identifier'])

        self.eat_type(['identifier'])                                  # Check for subroutine name
        self.eat_var(['('])                                            # Check opening bracket (
        self.compileParameterList()                                    # Check parameter list
        self.eat_var([')'])                                            # Check closing bracket )
        self.compileSubroutineBody()                                   # Check subroutine body
        self.parsed_list.append('</subroutineDec>')
        return
    
    def compileParameterList(self):
        self.parsed_list.append('<parameterList>')
        while self.token_list_analysed[self.token_index][0] in ['keyword', 'identifier']:
            
            self.eat_type(['keyword', 'identifier'])
            
            # Check variable name
            self.eat_type(['identifier'])
            
            # Check the variables
            if self.token_list_analysed[self.token_index][1]==',':
                self.eat_var([','])
            
        self.parsed_list.append('</parameterList>')
        return
    
    def compileSubroutineBody(self):
        self.parsed_list.append('<subroutineBody>')
        self.eat_var(['{'])
        self.compileVarDec()
        self.compileStatements()
        self.eat_var(['}'])
        self.parsed_list.append('</subroutineBody>')
        return
    
    def compileVarDec(self):
        
        while self.token_list_analysed[self.token_index][1] in ['var']:
            self.parsed_list.append('<varDec>')
            self.eat_type(['keyword'])         # Check keywods. Already var is checked

            # Check type of variable
            if self.token_list_analysed[self.token_index][0] == 'keyword':
                self.eat_var(['int', 'char', 'boolean']) 
            else:
                self.eat_type(['identifier'])
                
            flag_end_line = False
            # Check the variables
            while not(flag_end_line) and self.token_list_analysed[self.token_index][0] == 'identifier':
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
        self.eat_type(['identifier'])
        self.eat_var(['='])
        self.compileExpression()
        self.eat_var([';'])
        self.parsed_list.append('</letStatement>')
        return
    
    def compileIf(self):
        self.parsed_list.append('<ifStatement>')
        self.eat_var(['if'])
        self.eat_var(['('])
        self.compileExpression()
        self.eat_var([')'])
        self.eat_var(['{'])
        self.compileStatements()
        self.eat_var(['}'])
        
        if self.token_list_analysed[self.token_index][1]=='else':
            self.eat_var(['else'])
            self.eat_var(['{'])
            self.compileStatements()
            self.eat_var(['}'])
        self.parsed_list.append('</ifStatement>')
        return
    
    def compileWhile(self):
        self.parsed_list.append('<whileStatement>')
        self.eat_var(['while'])
        self.eat_var(['('])
        self.compileExpression()
        self.eat_var([')'])
        self.eat_var(['{'])
        self.compileStatements()
        self.eat_var(['}'])
        self.parsed_list.append('</whileStatement>')
        
        return
    
    def compileDo(self):
        self.parsed_list.append('<doStatement>')
        self.eat_var(['do'])
        self.eat_type(['identifier'])
        
        if self.token_list_analysed[self.token_index][1] == '.':
            self.eat_var(['.'])
            self.eat_type(['identifier'])
            
        self.eat_var(['('])
        self.compileExpressionList()
        self.eat_var(')')
        self.eat_var([';'])
        self.parsed_list.append('</doStatement>')
        return
    
    def compileReturn(self):
        self.parsed_list.append('<returnStatement>')
        self.eat_var(['return'])
        
        if self.token_list_analysed[self.token_index][1]!=';':
            self.compileExpression()
            
        self.eat_var([';'])
        
        self.parsed_list.append('</returnStatement>')
        return
    
    def compileExpression(self):
        self.parsed_list.append('<expression>')
        self.compileTerm()
        self.parsed_list.append('</expression>')
        return
    
    def compileTerm(self):
        self.parsed_list.append('<term>')
        self.eat_type(['identifier','keyword','integerConstant','stringConstant'])
        self.parsed_list.append('</term>')
        return
    
    def compileExpressionList(self):
        self.parsed_list.append('<expressionList>')
        while self.token_list_analysed[self.token_index][1] != ')':
            self.compileExpression()
            
            if self.token_list_analysed[self.token_index][1] == ',':
                self.eat_var([','])
        self.parsed_list.append('</expressionList>')
        return
    
    
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


