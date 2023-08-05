"""
scatter.py
"""
from pathlib import Path

import altair as alt
import click

from csvviz.exceptions import *
from csvviz.vizkit import Vizkit


class Scatterkit(Vizkit):
    viz_type = "scatter"
    viz_info = f"""A scatterplot for showing relationship between two independent variables x and y. Set -s/--size to create a bubble (variable dot size) chart"""
    viz_epilog = """Example:  $ csvviz scatter -x mass -y volume -s velocity data.csv"""

    def prepare_channels(self):
        channels = self._create_channels(self.channel_kwargs)
        self._set_channel_colorscale("fill", channels)
        return channels

    COMMAND_DECORATORS = (
        click.option(
            "--xvar",
            "-x",
            type=click.STRING,
            help="The name of the column for mapping x-axis values; if empty, the first (columns[0]) column is used",
        ),
        click.option(
            "--yvar",
            "-y",
            type=click.STRING,
            help="The name of the column for mapping y-axis values; if empty, the second (columns[1]) column is used",
        ),
        click.option(
            "--color",
            "-c",
            "fillvar",
            type=click.STRING,
            help="The name of the column for mapping dot colors. This is required for creating a multi-series scatter chart.",
        ),
        click.option(
            "--size",
            "-s",
            "sizevar",
            type=click.STRING,
            help="The name of the column for mapping dot size. This is required for creating a bubble chart.",
        ),
    )
