## 1.0.2 (2024-06-05)

### Fix

- **release-main.yml**: fix setup-pdm action for releasing to PyPi

## 1.0.1 (2024-06-05)

### Fix

- trigger automated release flow on main

## 1.0.0 (2024-06-04)

### BREAKING CHANGE

- sitemappy not available in pypi, renamed interface to sitemappy-cli

### Fix

- rename sitemappy to sitemappy-cli for publishing

## 0.2.0 (2024-06-04)

### Feat

- print to cmd optional CLI arg
- **crawler.py**: configurable crawling politeness
- **crawler.py**: crawl depth flag for depth of pages to follow
- **main.py**: argument for number of async workers
- concurrent workers and asyncio queue, results output to json file
- **Crawler**: relative url and anchor link handling
- async get requested url response and validation
- output url argument to console

### Refactor

- **main.py**: cli tool help text formatting
