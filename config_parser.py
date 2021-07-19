import re
import logging
import argparse


logging.basicConfig(level=logging.INFO)

COMMENT_PREFIX = '$'
INTEGER_RE = "[+-]?[0-9\-]+$"
FLOAT_RE = "[+-]?[0-9]+\.[0-9]+$"
BOOLEAN_TRUE = ['on', 'yes', 'true']
BOOLEAN_FALSE = ['off', 'no', 'false']


class ConfigParse:
    def __init__(self):
        pass

    def read(self, filename: str = None):
        if filename is None:
            return
        try:
            with open(filename) as fp:
                self.read_file(fp)
        except OSError:
            pass

    def read_file(self, fp):
        """
        Parse a configuration file line by line.

        Each line may be
        - Comments starting with '#'
        - Boolean-like values (on/off, yes/no, true/false)
        - Numeric values (integers, doubles)

        Comments will be removed from the object.
        """
        for line in fp:
            # Emtpy line with no characters will be ignored
            if line.strip() == '':
                continue

            # Lines starting Comment Prefix will be ignored
            if line.strip().startswith(COMMENT_PREFIX):
                continue

            # Checks if the current line is in format (object_name=object_value), i.e. there is '=' in the line
            # Ignores any characters present in the line which is not similar to the format.
            # Any object_name cannot have '=' character.
            # So the first '=' character should be a split between object_name and object_value.
            # The object_value may contain '=' if it is long string
            variable_split = line.find('=')
            if variable_split == -1:
                continue

            # Parse Key and Value part from both sides of '='
            object_name = line[:variable_split].strip()
            object_value = line[variable_split+1:].strip()

            # Check if left_part which is key or object name is valid identifier in Python
            if not object_name.isidentifier():
                logging.error(f'Invalid object name - "{object_name}"')
                continue

            # Convert the Object Value part in Integer, Float, Boolean or return String
            object_value = self.conv(object_value)

            # Set object name and value to the class object
            setattr(self, object_name, object_value)

    def conv(self, value):
        if re.match(INTEGER_RE, value):
            return int(value)
        if re.match(FLOAT_RE, value):
            return float(value)
        if value in BOOLEAN_TRUE:
            return True
        if value in BOOLEAN_FALSE:
            return False
        return value

    def __repr__(self):
        output = '\nObject Name/Value --> '
        for name, value in self.__dict__.items():
            output += f'{name}={value}\n'
        return output

if __name__ == '__main__':
    # Construct Argument Parser for getting Config Filepath
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, nargs="?", default=None)
    args = parser.parse_args()

    config = ConfigParse()
    config.read(args.file)

    logging.info(config)
    # logging.info(config.host)
    # logging.info(config.user)
    # logging.info(config.debug_mode)
    # logging.info(config.verbose)
    # logging.info(config.test_mode)
