#!/usr/bin/env python
import re
import argparse
from glob import glob 

def delete_surroundings (search,file_path,output):
    with open(file_path) as f:
        read_data = f.read()
        
    ends = [match.end() for match in re.finditer(re.escape(search), read_data)]
        
    def find_braces(end_indexes, searched_text):
        braces=[]
        j=0
        
        for k in xrange(len(ends)):
            for i,word in enumerate(read_data[ends[k]:]): 
                if word == '{':
                    j+=1
                elif word == '}' and j!=0:
                    j-=1
                elif word =='}' and j==0:
                    braces.append(i+ends[k])
                    break
        return braces
    
    braces = find_braces(ends,search)
                
    new_tex = ''.join([read_data[i] for i in xrange(len(read_data)) if i not in braces])
    new_tex = new_tex.replace(search,"")
        
    with open(output, "w") as tex_file:
        tex_file.write(new_tex)  
        
def main(macros_to_delete,files):
    for f in files:
        print "Removing command", macros_to_delete, "for", f
        delete_surroundings(macros_to_delete,f,f)
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='TeXedit')
    parser.add_argument('macros_to_delete',type=str,help='macros to delete')
    parser.add_argument('file', nargs='+', help='path to the file')
    args_namespace = parser.parse_args()
    file_names = list()  
    for arg in args_namespace.file:  
        file_names += glob(arg)  
    

    main(args_namespace.macros_to_delete,file_names)
    
    #search = '{\\rmfamily' 
    #search = '{\\selectlanguage{russian}'
    #search = '\\textcyrillic{'
    #search = '\\text{'
    #search = '\\mathit{'

    

    
