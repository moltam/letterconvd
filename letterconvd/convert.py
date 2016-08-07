
import argparse
import os
import csv
from datetime import datetime

class ImdbConverter(object):
    """Converts the input IMDb export file to Letterboxd CSV format.

    https://letterboxd.com/about/importing-data/
    """

    PART_POS = 0 # position
    PART_IMDB_ID = 1 # const
    PART_CREATED = 2 # created
    PART_MODIFIED = 3 # modified
    PART_DESCRIPTION = 4 # description
    PART_TITLE = 5 # Title
    PART_TITLE_TYPE = 6 # Title type
    PART_DIRECTORS = 7 # Directors
    PART_USER_RATING = 8  # You rated
    PART_IMDB_RATING = 9  # IMDb Rating
    PART_RUNTIME = 10  # Runtime (mins)
    PART_YEAR = 11  # Year
    PART_GENRES = 12  # Genres
    PART_NUM_VOTES = 13  # Num. Votes
    PART_RELEASE_DATE = 14  # Release Date (month/day/year)
    PART_URL = 15  # URL

    CSV_DELIMITER = ','
    CSV_QUOTE = '"'

    def __init__(self, inputfile):
        """

        Args:
            inputfile (str): The path of the IMDB export file.
        """
        self._inputfile = inputfile
        if not os.path.isfile(inputfile):
            raise FileNotFoundError("Input file not found: " + inputfile)

    def convert(self, outputfile):
        """ Converts the input file into the output file.

        Args:
            outputfile (str): The path of the outputfile.
        """
        file = open(outputfile, 'w')
        outwriter = csv.writer(file, delimiter=self.CSV_DELIMITER, quotechar=self.CSV_QUOTE, quoting=csv.QUOTE_ALL)
        headers = ["imdbID", "Title", "Year", "Directors", "WatchedDate", "CreatedDate", "Rating10"];
        outwriter.writerow(headers)

        with open(inputfile, 'r') as imdbfile:
            imdbfile.readline()  # skip header
            imdbreader = csv.reader(imdbfile, delimiter=self.CSV_DELIMITER, quotechar=self.CSV_QUOTE)

            for row in imdbreader:
                outwriter.writerow(self._convert_row(row))

        file.close()

    def _convert_row(self, row):
        """ Returns a list that contains one row formatted output data.

        Args:
            row (list):

        Returns:
            list:
        """
        return [
            row[self.PART_IMDB_ID],
            row[self.PART_TITLE],
            row[self.PART_YEAR],
            row[self.PART_DIRECTORS],
            self._convert_datetime(row[self.PART_CREATED]),
            '',
            row[self.PART_USER_RATING]
        ]

    def _convert_datetime(self, date_string, format="%Y-%m-%d"):
        """ Converts the IMDb dates into the specified format

        Args:
            date_string (str): A date value, e.g. "Wed Aug 21 12:55:59 2013"
            format (str): Optional, the output date format. Default to YYYY-MM-DD
        Returns:
            str: The formatted date.
        """
        parsed_date = datetime.strptime(date_string, "%a %b %d %H:%M:%S %Y")

        return parsed_date.strftime(format)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile")
    inputfile = parser.parse_args().inputfile

    converter = ImdbConverter(inputfile)
    outputfile = os.path.splitext(inputfile)[0] + '_out.csv'
    converter.convert(outputfile)

