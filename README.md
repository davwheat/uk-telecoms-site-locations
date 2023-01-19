# UK telecoms sites dataset

The UK Government has an agency called the Valuation Office Agency which calculates the [business rates payable](https://www.gov.uk/introduction-to-business-rates) for using a piece of land for non-domestic purposes.

This repo uses the dataset available for download from the VOA, filters it to include only telecommunications sites, then matches addresses to latitude and longitudes via Nominatim to build a dataset of telecoms sites throughout the UK.

## Running locally

1. Download the entire dataset from the [UK Government website](https://www.tax.service.gov.uk/business-rates-find/list-properties) ("Download the entire rating list and summary valuation datasets")
2. Extract the CSV file from the ZIP provided, and name it `data.csv`.
3. Run `python ./rewrite_csv.py`
4. Run `python ./app.py`. This will filter the data, and match it to lat/lon positions from Nominatim. This can take multiple hours.
5. The final output file will be found at `all_comms_sites.py`.

> You can also download a precompiled dataset from this repo.

## License

### Dataset

The dataset (`all_comms_sites.csv`) is licensed under a mixed license.

All columns of the file **except** `lat` and `lng` are licensed under the [terms and conditions set by the VOA on the download page](https://www.tax.service.gov.uk/business-rates-find/terms-and-conditions).

The data within `lat` and `lng` are licensed under the Open Database License. You **must** provide [suitable attribution to OpenStreetMap](https://www.openstreetmap.org/copyright) to use this part of the dataset.

For this purpose, [suitable attribution need only qualify what data is from OpenStreetMap](https://wiki.osmfoundation.org/wiki/Licence/Attribution_Guidelines#Attribution_text), thus a simple `Positional data from OpenStreetMap.` can suffice, provided "OpenStreetMap" links to the [OSM copyright page](https://www.openstreetmap.org/copyright). This may require amending if you use other data from OSM, such as map tiles.

### Other

All other files in this repository are licensed under the MIT license.
