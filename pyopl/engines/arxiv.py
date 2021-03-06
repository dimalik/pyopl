"""arXiv docstring to be inserted here."""

from feedparser import parse
from arxiv2bib import Cli

from engine import Engine
from result import Result


class ArxivResult(Result):
    """arXiv Result Parser"""
    
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


class ArxivEngine(Engine):
    """arXiv Engine"""
    query_url = "http://export.arxiv.org/api/query?search_query=all:{}"

    def fetch_results(self, contents):
        """
        See http://arxiv.org/help/api/index for more on the structure of the
        arXiv atomxml response.
        """
        citations = []
        contents_dict = parse(contents)
        try:
            for item in contents_dict['entries']:
                citations.append(ArxivResult(item))
        except KeyError:
            raise ValueError("AtomXML response was not correctly formatted.")
        return citations

    def get_citation(self, identifier):
        """
        Return the bib entry using nathan grigg's arxiv2bib
        (http://nathangrigg.github.io/arxiv2bib/)
        """
        cli = Cli([identifier])
        cli.run()
        return "\n".join(cli.output)
