# instapull
Simple tool to dump images from a Instagram timeline

![Upload Python Package](https://github.com/FrodeHus/instapull/workflows/Upload%20Python%20Package/badge.svg)


## Install

from cloned repo: `pip3 install .`

from package: `pip3 install instapull`

## Usage

```bash
usage: instapull [options] instagram-user

Pull images from a Instagram feed

positional arguments:
  instagram_user        User name of the Instagram feed to pull images from

optional arguments:
  -h, --help            show this help message and exit
  -m MAX_PAGES, --max-pages MAX_PAGES
                        Pull a maximum number of pages (12 images per page)
  -p PAGE_SIZE, --page-size PAGE_SIZE
                        Set the page size for each download pass (defaults to 12)
                      
```
