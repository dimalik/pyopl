# Python Online Paper Locator

Pyopl is an extensible python module that searches and fetches bibtex citations from online sources and adds them to your bibliography. Currently, it supports searching and fetching through `crossref` and `arxiv`. The application has been designed in a modular manner providing an API such that adding/editing search engines becomes as easy as possible.

## Installation

Download the provided repo and run

```bash
python setup.py install
```

## Dependencies

Although Pyopl by itself does not have any dependencies, some search engines might. Currently, `arxiv` depends on [Nathan Grigg's `arxiv2bib`](https://github.com/nathangrigg/arxiv2bib) (for bib formatting) and [`feedparser`](https://pypi.python.org/pypi/feedparser) (for reading the API).

## License

BSD
