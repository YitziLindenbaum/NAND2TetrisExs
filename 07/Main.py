from sys import argv
from os import listdir
import os.path as osp

p = __import__('Parser')
c = __import__('CodeWriter')

ASM_EXTENSION = '.asm'
VM_EXTENSION = '.vm'

if __name__ == '__main__':
    all_files = [argv[1]]
    if osp.isdir(argv[1]):  # The supplied path is a directory
        # List all .vm files in the directory
        all_files = [osp.join(argv[1], file) for file in listdir(argv[1]) if osp.isfile(osp.join(argv[1], file)) if file.endswith(VM_EXTENSION)]
        out_file_name = osp.join(argv[1], osp.split(argv[1])[1]) + ASM_EXTENSION
    else:  # The supplied path is a file
        out_file_name = argv[1].replace(VM_EXTENSION, ASM_EXTENSION)

    with open(out_file_name, 'w') as out_file:
        code_writer = c.CodeWriter(out_file)
        code_writer.write_init()
        for file in all_files:
            f = open(file, 'r')
            parser = p.Parser(f)
            f.close()

            code_writer.set_file_name(osp.split(file)[1])
            while parser.has_more_commands():
                parser.advance()
                command_type = parser.command_type()
                if command_type == 'arithmetic':
                    code_writer.write_arithmetic(parser.arg1())
                elif command_type in {'pop', 'push'}:
                    code_writer.write_push_pop(command_type, parser.arg1(), int(parser.arg2()))
                elif command_type == 'label':
                    code_writer.write_label(parser.arg1())
                elif command_type == 'goto':
                    code_writer.write_goto(parser.arg1())
                elif command_type == 'if-goto':
                    code_writer.write_if(parser.arg1())
                elif command_type == 'call':
                    code_writer.write_call(parser.arg1(), parser.arg2())
                elif command_type == 'return':
                    code_writer.write_return()
                elif command_type == 'function':
                    code_writer.write_function(parser.arg1(), parser.arg2())
