from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.requests import Request
from starlette.routing import Route

import mysql.connector
import json
from decimal import Decimal

from typing import List, Dict, Any


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class DecimalCompatJSONResponse(JSONResponse):
    def render(self, content: Any):
        return json.dumps(
            content,
            cls=DecimalEncoder,
        ).encode("utf-8")


with open("/db.json", "r") as f:
    db_cfg = json.load(f)

mydb = mysql.connector.connect(
    host=db_cfg["host"],
    port=db_cfg["port"],
    user=db_cfg["user"],
    password=db_cfg["password"],
    database=db_cfg["database"],
)


async def get_nodes_within_bounds(ne_lat, ne_lng, sw_lat, sw_lng):
    cr = mydb.cursor(dictionary=True)

    cr.execute(
        "SELECT * FROM `properties` WHERE (lat BETWEEN %s AND %s) AND (lng BETWEEN %s AND %s)",
        (sw_lat, ne_lat, sw_lng, ne_lng),
    )

    data = cr.fetchall()

    cr.close()

    return data


async def hello_world(request: Request):
    return HTMLResponse(
        """
<p>Hello there!</p>
<p>This API is run by <a href="https://davwheat.dev" target="_blank">David Wheatley</a>
using location data from <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>
and business rates information from HMRC's Valuation Office Agency
<a href="https://www.tax.service.gov.uk/business-rates-find/terms-and-conditions">under license</a>.
<p><a href="https://github.com/davwheat/uk-telecoms-site-locations">This project is open source on GitHub!</a></p>
"""
    )


async def get_sites(request: Request):

    ne_lat = request.query_params.get("ne_lat", 0)
    ne_lng = request.query_params.get("ne_lng", 0)
    sw_lat = request.query_params.get("sw_lat", 0)
    sw_lng = request.query_params.get("sw_lng", 0)

    if ne_lat and ne_lng and sw_lat and sw_lng:
        ne_lat = float(ne_lat)
        ne_lng = float(ne_lng)
        sw_lat = float(sw_lat)
        sw_lng = float(sw_lng)
    else:
        raise ValueError(
            "You must provide values for parameters: ne_lat, ne_lng, sw_lat, sw_lng"
        )

    all_records = await get_nodes_within_bounds(ne_lat, ne_lng, sw_lat, sw_lng)

    return DecimalCompatJSONResponse(
        {
            "license": "Data © Valuation Office Agency (https://www.tax.service.gov.uk/business-rates-find/terms-and-conditions). Positional data © OpenStreetMap contributors (https://www.openstreetmap.org/copyright).",
            "data": all_records,
        }
    )


app = Starlette(
    # debug=True,
    routes=[
        Route("/", hello_world),
        Route("/sites", get_sites),
    ],
)
