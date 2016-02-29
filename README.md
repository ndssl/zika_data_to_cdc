# Zika data to CDC format

Converting various datasets to adhere to [CDC Zika format](https://github.com/cdcepi/zika/blob/master/data_dictionary.md)

## Setup

This repository assumes that data from other repositories are sibbling directores to this repository

For example:

```
some_folder_path/
  |
  |- zika
  |- zika-data
  +- zika_data_to_cdc
```

Where:

- `zika` is the [CDC repo](https://github.com/cdcepi/zika)
- `zika-data` is the [BuzzFeed repo](https://github.com/BuzzFeedNews/zika-data)
- `zika_data_to_cdc` is this repo

## Running Scripts

The scripts found in `src/*` will assume they are run from root of the repository
(i.e., you will type something like `python src/buzzfeed/clean_parsed_colombia.py`)

## Data sources

- CDC: https://github.com/cdcepi/zika
  - additional data: https://github.com/cdcepi/zika/blob/master/additional_data.md
- BuzzFeed: https://github.com/BuzzFeedNews/zika-data

## Technical Info

The scripts need to be run from this repository's root location.

The scripts and modules located in `src/` are separated into parts for simplicity and modularity.
In doing so, most of the scripts will have the following bits of code in the import statement

```python
import os
import sys

sys.path.append(os.getcwd())
import src.helper as helper
```

This is why running the code form this diretory is so important.
it will use the `getwcd()` to append to the path,
so it knows how to find the other modules.

Yes, it's a bit hacky,
but this prevents having this repo setup as a python module,
and users do not have to edit their own `PATH` or `PYTHONPATH` variable.
