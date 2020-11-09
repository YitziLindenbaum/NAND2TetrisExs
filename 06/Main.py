from sys import argv
from os import listdir
from os.path import isdir, isfile, join
p = __import__('Parser')
c = __import__('Code')

ASM_EXTENSION = '.asm'
HACK_EXTENSION = '.hack'
NEWLINE = '\n'

if __name__ == '__main__':
    all_files = [argv[0]]
    if isdir(argv[0]):  # The supplied path is a directory
        all_files = [file for file in listdir(argv[0]) if isfile(join(argv[0], file)) if file.endswith(ASM_EXTENSION)]  # List all .asm files in the directory

    print(all_files)
    for file in all_files:
        f = open(file, 'r')
        parser = p.Parser(f)
        f.close()

        out_file_name = file.replace(ASM_EXTENSION, HACK_EXTENSION)
        with open(out_file_name, 'w') as out_file:

            while parser.hasMoreCommands():
                parser.advance()
                code = c.Code(parser)
                bin_code = code.processCode()
                out_file.write(bin_code)
                out_file.write(NEWLINE)
