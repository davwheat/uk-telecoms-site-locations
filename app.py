import pandas as pd
from typing import Any, Union
import requests
import mapply
import urllib.parse

mapply.init(n_workers=10)

cols: dict[Any, Any] = {
    "id": "string",
    "billing authority code": "string",
    "community code": "string",
    "ba reference": "string",
    "description code": "string",
    "primary description text": "string",
    "uarn": "string",
    "property identifier": "string",
    "business name": "string",
    "number": "string",
    "street": "string",
    "town": "string",
    "postal district": "string",
    "county": "string",
    "postcode": "string",
    "effective date": "string",
    "composite indicator": "string",
    "rateable value": "string",
    "appeal settlement code": "string",
    "assessment reference": "string",
    "list alteration date": "string",
    "scat code and suffix": "string",
    "substreet level 3": "string",
    "substreet level 2": "string",
    "substreet level 1": "string",
    "case number": "string",
    "current from date": "string",
    "current to date": "string",
    "_": "string",
}

df = pd.read_csv(
    "data_converted.csv",
    low_memory=False,
    names=list(cols.keys()),
    dtype=cols,
    header=None,
    encoding="latin-1",
    index_col=0,
)


def limit_df_by_scat(df, scat):
    return df[df["scat code and suffix"] == scat]


def main():
    global df

    pd.set_option(
        "display.max_rows",
        None,
    )
    pd.set_option(
        "display.max_columns",
        None,
    )
    pd.set_option(
        "display.max_colwidth",
        None,
    )

    df = limit_df_by_scat(df, "066G")
    df = df[
        [
            "uarn",
            "property identifier",
            "business name",
            "number",
            "street",
            "town",
            "county",
            "postcode",
            "rateable value",
            "current from date",
            "current to date",
        ]
    ]

    df["lat"] = None
    df["lng"] = None

    output_csv(df)

    df = df.mapply(look_up_address, axis=1, result_type="expand")

    output_csv(df)


def output_csv(df: pd.DataFrame) -> None:
    df.to_csv("all_comms_sites.csv", index=False)


addr_cnt = 0


def look_up_address(row: dict[str, Any], no_number: bool = False) -> dict[str, Any]:
    num = row["number"]
    street = row["street"]
    town = row["town"]
    postalcode = row["postcode"]

    query = {
        "street": f"{num} {street}",
        "city": town,
        "postalcode": postalcode,
        "countrycodes": "gb",
        "format": "json",
    }

    if no_number:
        query["street"] = street

    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params=query,
            headers={"user-agent": "david+ukbra@mastdatabase.co.uk"},
        ).json()

        if len(r) > 0:
            row["lat"] = r[0]["lat"]
            row["lng"] = r[0]["lon"]

            return row
        else:
            if not no_number:
                return look_up_address(row, no_number=True)
            else:
                q = urllib.parse.urlencode(query)
                print(
                    f"NONE: {num} {street}, {postalcode} - https://nominatim.openstreetmap.org/search?{q}"
                )

    except Exception as e:
        print(e)
        q = urllib.parse.urlencode(query)
        print(
            f"FAILED: {num} {street}, {postalcode} - https://nominatim.openstreetmap.org/search?{q}"
        )

    row["lat"] = None
    row["lng"] = None

    return row


if __name__ == "__main__":
    main()
