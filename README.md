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

## Data sources

- CDC: https://github.com/cdcepi/zika
  - additional data: https://github.com/cdcepi/zika/blob/master/additional_data.md
- BuzzFeed: https://github.com/BuzzFeedNews/zika-data
