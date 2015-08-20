# Python Online Paper Locator

Pyopl is an extensible python module that searches and fetches bibtex citations from online sources and adds them to your bibliography. Currently, it supports searching and fetching through `crossref` and `arxiv`. The application has been designed in a modular manner providing an API such that adding/editing search engines becomes as easy as possible.

## Installation

Download the provided repo and run

```bash
python setup.py install
```

## Usage

You can use pyopl to search online academic paper engines (current supported: crossref, arxiv) for your citation like this:

```bash
pyopl deep learning
```

You can also specify the engines you want to use:

```bash
pyopl --engines=arxiv,crossref deep learning
```

These commands default to the `--search` mode; If you want to fetch the bibtex citation you can do so like this:

```bash
pyopl --fetch --engines=arxiv 1312.5602v1
```

While `--engines` is optional in search mode (default all), in `--fetch` you need to specify a single engine to fetch the citation from.

Fetch mode defaults to displaying the citation in `STDOUT` (where you can pipe it to your bibliography .bib file). Optionally, you can specify your bibliography file and `pyopl` will do the appending for you:

```bash
pyopl --fetch --engines=arxiv --bib=/path/to/bib/file 1312.5602v1
```

Lastly, `pyopl` offers the ability to write the citation as a file in a specified folder. This could be useful, for example, when you want to synchronize your library between different machines:

```bash
pyopl --fetch --engines=arxiv --bib=/path/to/bib/file --secondary-bib=/path/to/bib/folder 1312.5602v1
```

## Dependencies

Although Pyopl by itself does not have any dependencies, some search engines might. Currently, `arxiv` depends on [Nathan Grigg's `arxiv2bib`](https://github.com/nathangrigg/arxiv2bib) (for bib formatting) and [`feedparser`](https://pypi.python.org/pypi/feedparser) (for reading the API).

## License

BSD
