"""Collects any utility tool for the script"""

import pickle


class Utils:
    """Static class with util tools"""

    @staticmethod
    def from_pickle(filename):
        """
        Read data from a pickled file

        :param str filename: read the data from a pickled file
        :return: a memory-parsed file with the data
        """
        return pickle.load(open(filename, 'rb'))

    @staticmethod
    def import_csv_data(csv_filename):
        """
        Import a CSV filename with all the data

        :param str csv_filename: CSV filename with the data to process
        :return: a dictionary of all the parsed data
        """
        temp = list()
        parsed_csv_file = dict()
        lines = open(csv_filename, encoding='utf-8').readlines()
        headers = lines[0].split("\"\n")[0].replace("\"", "").split(',')
        for row_numb, row in enumerate(lines):
            if row_numb == 0:
                continue  # Skip Headers as they've been already parsed outside the loop
            line_split = row.replace("\"", "").replace("\n", "").split(',')
            if len(line_split) < 4:  # Skipping incomplete lines
                continue
            temp.append(line_split[0])
            parsed_csv_file[line_split[0]] = dict()
            parsed_csv_file[line_split[0]] = dict(zip(headers[1:], line_split[1:]))
        return parsed_csv_file
