#!/usr/bin/env python

import pytest
from click.testing import CliRunner

import json
from pathlib import Path

from csvviz.exceptions import *
from csvviz.settings import *

from csvviz.cmds.area import Areakit

area = Areakit.register_command()

TONK_ARGS = [
    "examples/tonk.csv",
    "--json",
    "--no-preview",
]

STOCK_ARGS = [
    "examples/stocks.csv",
    "--json",
    "--no-preview",
]


def test_area_defaults():
    """
    MVP, where x is columns[0] and y is columns[1]

    just a catch all sanity test...
    Should resemble what's in tests/fixtures/bar-basic.json
    """
    cdata = json.loads(CliRunner().invoke(area, [*TONK_ARGS]).output)

    assert cdata["mark"]["type"] == "area"

    datavals = list(cdata["datasets"].values())[0]
    assert datavals[0] == {"date": "2007-01-01", "price": 37.67}
    assert datavals[-1] == {"date": "2010-03-01", "price": 128.82}

    # even though date is in YYYY-MM-DD format, Altair doesn't automatically know it's temporal
    assert cdata["encoding"]["x"] == {"field": "date", "type": "nominal"}
    assert cdata["encoding"]["y"] == {"field": "price", "type": "quantitative"}


def test_area_multiseries_defaults():
    cdata = json.loads(
        CliRunner()
        .invoke(area, ["-x", "date", "-y", "price", "--color", "company", *STOCK_ARGS])
        .output
    )
    e = cdata["encoding"]["fill"]
    assert e["field"] == "company"
    assert e["type"] == "nominal"
    assert e["legend"]["title"] == "company"


def test_area_fill_sort():
    cdata = json.loads(
        CliRunner()
        .invoke(
            area,
            [
                "-x",
                "date",
                "-y",
                "price",
                "--color",
                "company",
                "--color-sort",
                "asc",
                *STOCK_ARGS,
            ],
        )
        .output
    )
    o = cdata["encoding"]["order"]
    assert o["field"] == "company"
    assert o["sort"] == "ascending"


def test_area_fill_sort_desc():
    cdata = json.loads(
        CliRunner()
        .invoke(
            area,
            ["-x", "date", "-y", "price", "-c", "company", "-cs", "desc", *STOCK_ARGS],
        )
        .output
    )
    o = cdata["encoding"]["order"]
    assert o["field"] == "company"
    assert o["sort"] == "descending"


def test_area_colors():
    cdata = json.loads(
        CliRunner()
        .invoke(
            area,
            [
                "-x",
                "date",
                "-y",
                "price",
                "-c",
                "company",
                "-C",
                "red,yellow",
                *STOCK_ARGS,
            ],
        )
        .output
    )
    e = cdata["encoding"]["fill"]
    assert e["scale"]["range"] == ["red", "yellow"]


def test_area_error_when_fill_sort_but_no_fill():
    result = CliRunner().invoke(
        area, ["-x", "date", "-y", "price", "-cs", "asc", *STOCK_ARGS]
    )
    assert result.exit_code == 1
    assert (
        "MissingDataReference: --color-sort 'asc' was specified, but no --color value"
        in result.output.strip()
    )
