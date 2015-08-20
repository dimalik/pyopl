"""
Abstract Result Class. It is optional but recommended to use this in formatting
the results.

Things to cover when written properly:
1) the string passed from fetch_results is called parsed_obj
2) as in engine the name of the engine is determined by the name of the file.
3) title strips any newlines (shouldn't the others do that too?)
4) authors are formatted in bibtex form (i.e. separated by commas in all but
the last one where it's separated by and).
"""


import os
import sys


class Result(object):

    def __init__(self, parsed_obj):
        self.parsed_obj = parsed_obj

    @classmethod
    def _get_name(cls):
        return os.path.basename(
            sys.modules[cls.__module__].__file__).split('.')[0]

    def __get_title(self):
        """Return the publication title"""
        title = self.get_title()
        return ' '.join(title.split('\n'))

    def __get_authors(self):
        """
        Take a list of string (authors' names) and return them in more
        readable (bibtex like) format.
        """
        authors = self.get_authors()
        if not len(authors):
            return ''
        elif len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
            return ' and '.join(authors)
        else:
            return ' and '.join([', '.join(authors[:-1]), authors[-1]])

    def __get_id(self):
        """Return the publication id"""
        return self.get_id()

    def __get_year(self):
        """Return the publication year"""
        return self.get_year()
    
    def __str__(self):
        return "[{}]\t({})\n\t{}\n\t{} | {}\t\n".format(
            self.__get_id(),
            self.__class__._get_name(),
            self.__get_title(),
            self.__get_authors(),
            self.__get_year()
            )

