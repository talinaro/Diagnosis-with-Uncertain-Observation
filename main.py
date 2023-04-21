import glob

from consts import SYS_FILE_EXTENSION
from system_parser import parse_system


def main(data_systems_dir):
    # parse all the systems
    data_systems = [
        parse_system(filepath)
        for filepath in glob.glob(pathname=fr'{data_systems_dir}/*.{SYS_FILE_EXTENSION}')
    ]


if __name__ == '__main__':
    main(data_systems_dir='circuits_examples/Data_Systems')
