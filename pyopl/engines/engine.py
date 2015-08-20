"""
Abstract Engine Class. From this all the engines should inherit
See CrossRef and arXiv for more information.

Things to cover in the docstring:

that all inherited classes should supply:
1) a query_url class attribute and what it should return.
2) a fetch_results method which returns a list of strings (or Result objects)
3) a get_citation method that returns a bibtex entry

1) point to the fact that the query is preprocessed of any punctuation
2) that the name of the engine is the name of the file
"""

import os
import sys
import uuid
import urllib2
from string import maketrans, punctuation


def query_cleaner(query):
    """Remove punctuation from the query and change whitespaces to + signs"""
    return "+".join(query.translate(
        maketrans(
            punctuation,
            "".join([" "] * len(punctuation))
        )).split())


class Engine(object):
    """Engine docstring here? Or at the start?"""
    
    def __init__(self, arg):
        """
        Depening on the context arg could be either the query or the identifier
        """
        self.arg = arg

    def __get_response(self):
        """Return the HttpResponse string to be used in fetching the results"""
        response = urllib2.urlopen(
            self._get_query_url(self.arg))
        contents = response.read()
        if not contents:
            raise ValueError('HTTPResponse was empty.')
        return contents

    @classmethod
    def _get_name(cls):
        """Return the name of the engine as specified in the filename."""
        return os.path.basename(
            sys.modules[cls.__module__].__file__).split('.')[0]

    @classmethod
    def _get_query_url(cls, query):
        """Return the final (formatted) url to be queried."""
        if not hasattr(cls, 'query_url'):
            raise AttributeError('{} does not define a query_url'.format(
                cls.__name__
            ))
        return cls.query_url.format(query_cleaner(query))

    def __fetch_results(self, contents):
        """
        Call the inherited module's fetch_results method passing the response
        from the url.
        """
        return self.fetch_results(contents)

    def fetch_results(self, contents):
        """
        Return the results of the query as a list of strings or a list of
        objects defining a __str__ method (see result.py). This function
        is responsible for parsing the httpresponse returned by the internal
        __get_response method.

        Arguments:
        contents --- the httpresponse (whatever that may be -e.g. xml/http etc)

        Return:
        a list of four line strings (see result.py for formatting), or more
        simply a list of Result objects which handle string formatting
        internally
        """
        raise NotImplementedError

    def __get_citation(self, identifier):
        """
        Call the inherited module's get_citation method passing the identifier
        specified in the cmd call.
        """
        return self.get_citation(identifier)

    def get_citation(self, identifier):
        """
        Return the bibtex representation of the citation. In its simplest form
        (as in DOI related queries) the identifier could be used directly to
        fetch the bibtex entry. Otherwise, the implementer should define a way
        to create the bibtex entry (see arxiv.py for an example).

        Arguments:
        identifier --- string to be passed to the new query which would fetch
                       the info to create the bibtex entry.

        Return:
        a string containing the bibtex representation of the citation.
        """
        raise NotImplementedError

    def get_items(self):
        """Return the list of citations."""
        return self.__fetch_results(self.__get_response())

    def write_bib(self, bib_file=None, secondary_bib=None):
        """
        Append the bibtex entry to bib_file and optionally create a .bib file
        containing the same entry. If both arguments are None then the entry
        is written in the stdout.

        Arguments:
        bib_file      --- absolute path to a .bib file
        secondary_bib --- absolute path to a directory
        """

        if bib_file:
            with file(bib_file, "a") as fout:
                fout.write('\n')
                fout.write(self.__get_citation(self.arg))
                fout.write('\n')

        if secondary_bib:
            with file(os.path.join(
                    secondary_bib,
                    "{}.bib".format(str(uuid.uuid4()))), "w") as fout:
                fout.write(self.__get_citation(self.arg))

        if not (bib_file or secondary_bib):
            sys.stdout.write('\n')
            sys.stdout.write(self.__get_citation(self.arg))
            sys.stdout.write('\n')
