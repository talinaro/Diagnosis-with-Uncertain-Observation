""" The main functionality of the package - parsing the system from the data .sys files """
from system_parser.system import System


def parse_system(filepath):
    return System.parse(filepath)
