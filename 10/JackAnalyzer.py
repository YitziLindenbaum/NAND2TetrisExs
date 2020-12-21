from sys import argv
from os import listdir
from os.path import isdir, isfile, join
jt = __import__('JackTokenizer')
ce = __import__('CompilationEngine')

XML_EXTENSION = '.xml'
JACK_EXTENSION = '.jack'

if __name__ == '__main__':
    all_files = [argv[1]]
    if isdir(argv[1]):  # The supplied path is a directory
        # List all .asm files in the directory
        all_files = [join(argv[1], file) for file in listdir(argv[1]) if isfile(join(argv[1], file)) if file.endswith(JACK_EXTENSION)]

    for file in all_files:
        with open(file, 'r') as f:
            tokenizer = jt.JackTokenizer(f)

        out_file_name = file.replace(JACK_EXTENSION, XML_EXTENSION)
        with open(out_file_name, 'w') as out_file:
            comp_engine = ce.CompilationEngine(tokenizer, out_file)
