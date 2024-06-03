## 📖 About 

Sitemappy (or sitemap-py 😉) is a crawler that produces a sitemap for a given website.

Sitemappy can be used as a command-line application, and also provides Python interfaces for use as a library.

### Features

- [x] Print the URL for a given website when visited
- [ ] Print the links for a given webpage
- [ ] Visit the links for a given webpage
- [ ] Limit the links to follow on a webpage to the same single subdomain
- [ ] Introduce concurrency (`asyncio`, `multithreading`, `multiprocessing`)


## 🎒 Requirements 

[Python](https://www.python.org/downloads/) `3.12+`


## 💻 Installation

To use the sitemappy CLI:

```bash
pip install --user -U sitemappy
```

### Python Library

Use sitemappy in your project with one of the following:

with **pip**:

```bash
pip install -U sitemappy
```

with **PDM**:

```bash
pdm add sitemappy
```

with **Poetry** >= 1.2.0:

```bash
poetry add sitemappy
```

### macOS

via [homebrew](#macos):

```bash
brew install sitemappy
```


## 🚀 Usage

Generate a sitemap:

```shell
sitemappy https://monzo.com/
```

### Help

```shell
$ sitemappy --help
usage: sitemappy [-h] ...

Sitemappy is a CLI tool to crawl a website and create a sitemap.
For more information about the tool go to https://github.com/dan-wilton/

optional arguments:
  -h, --help            show this help message and exit
```