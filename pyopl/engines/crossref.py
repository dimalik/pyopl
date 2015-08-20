"""CrossRef docstring to be inserted here."""

import urllib2
import json

from engine import Engine
from result import Result


class CrossRefResult(Result):
    """CrossRef Result Parser"""

    def get_title(self):
        """Return the publication title."""
        try:
            if len(self.parsed_obj['title']) > 1:
                return ' - '.join(self.parsed_obj['title']).encode('utf-8')
            return self.parsed_obj['title'][0].encode('utf-8')
        except:
            return '(no title)'.encode('utf-8')

    def get_authors(self):
        """Return a list of strings with the authors' names."""
        authors = []
        if 'author' not in self.parsed_obj:
            return ''
        for i, author in enumerate(self.parsed_obj['author']):
            fam = author.get('family', '').encode('utf-8')
            giv = author.get('given', '').encode('utf-8')
            if giv:
                giv = giv[0]
            authors.append("{} {}.".format(fam, giv))
        return authors

    def get_year(self):
        """Return the publication year of the citation."""
        if 'issued' in self.parsed_obj:
            return str(self.parsed_obj['issued']['date-parts'][0][0])
        return ''

    def get_id(self):
        """Return the engine identifier (DOI) as a string."""
        if 'DOI' in self.parsed_obj:
            return self.parsed_obj['DOI']
        return ''


class CrossRefEngine(Engine):
    """CrossRef Engine"""
    query_url = "http://api.crossref.org/works?query={}"

    def fetch_results(self, contents):
        """
        See http://api.crossref.org/ for more on the structure of the crossref
        json response
        """
        citations = []
        contents_dict = json.loads(contents)
        try:
            for item in contents_dict['message']['items']:
                citations.append(CrossRefResult(item))
        except KeyError:
            raise ValueError("JSON response was not correctly formatted.")
        return citations

    def get_citation(self, identifier):
        """Pass the identifier to dx.doi.org and return the bib entry"""
        request = urllib2.Request('http://dx.doi.org/{}'.format(identifier))
        request.add_header("Accept", "application/x-bibtex")
        response = urllib2.urlopen(request)
        bibcit = response.read()
        return bibcit
