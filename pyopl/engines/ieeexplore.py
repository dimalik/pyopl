"""ieeexplore docstring to be inserted here."""

import xml.etree.ElementTree as ET

from engine import Engine
from result import Result


class IEEEXploreResult(Result):
    """IEEE Xplore Result Parser"""
    
    def get_title(self):
        """Return the publication title"""
        try:
            return self.parsed_obj['title'].encode('utf-8')
        except:
            return '(no title)'.encode('utf-8')

    def get_authors(self):
        """Return a list of strings with the authors' names."""
        authors = []
        if 'authors' not in self.parsed_obj:
            return ''
        for i, author in enumerate(self.parsed_obj['authors']):
            authors.append(author['name'].encode('utf-8'))
        return authors

    def get_year(self):
        """Return the publication year of the citation. """
        if 'published_parsed' in self.parsed_obj:
            return str(self.parsed_obj['published_parsed'].tm_year)
        return ''

    def get_id(self):
        """Extract and return the arXiv identifier."""
        if 'id' in self.parsed_obj:
            return self.parsed_obj['id'].split('/')[-1]
        return ''


class IEEEXploreEngine(Engine):
    """IEEE Xplore Engine"""
    query_url = "http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?querytext={}\
&sortfield=py&sortorder=asc"

    def parse(self, contents):
        root = ET.fromstring(contents)
        return [doc for doc in root.iter('document')]

    def fetch_results(self, contents):
        """
        See http://ieeexplore.ieee.org/gateway/ for more info on the API.
        """
        citations = []
        contents_dict = self.parse(contents)
        try:
            for item in contents_dict:
                citations.append(IEEEXploreResult(item))
        except KeyError:
            raise ValueError("AtomXML response was not correctly formatted.")
        return citations

    def get_citation(self, identifier):
        """
        Return the bib entry using nathan grigg's arxiv2bib
        (http://nathangrigg.github.io/arxiv2bib/)
        """
        pass
        #        cli = Cli([identifier])
#        cli.run()
#        return "\n".join(cli.output)
