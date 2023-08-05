from pathlib import Path
import re

from typing import (
    Any as typeAny,
    Callable as typeCallable,
    Dict as typeDict,
    IO as typeIO,
    List as typeList,
    Mapping as typeMapping,
    NoReturn as typeNoReturn,
    Tuple as typeTuple,
    Union as typeUnion,
)


import altair as alt
from altair.utils import parse_shorthand
from altair.utils.schemapi import Undefined as altUndefined
import altair_viewer as altview
import pandas as pd

from csvviz.cli_utils import clout, clerr
from csvviz.exceptions import *
from csvviz.settings import *


import click
from csvviz.cli_utils import clout, clerr, clexit, standard_options_decor

ENCODING_CHANNEL_NAMES = (
    "x",
    "y",
    "fill",
    "size",
    "stroke",
    "facet",
)


def lookup_mark_method(viz_type: str) -> alt.Chart:
    """
    convenience method that translates our command names, e.g. bar, dot, line, to
    the equivalent in altair
    """
    vname = viz_type.lower()

    if vname in (
        "area",
        "bar",
        "line",
    ):
        m = f"mark_{vname}"
    elif vname == "hist":
        m = "mark_bar"
    elif vname == "scatter":
        m = "mark_point"
    elif vname == "abstract":
        m = "mark_bar"  # for testing purposes
    else:
        raise ValueError(f"{viz_type} is not a recognized viz/chart type")
    return m


def open_chart_in_browser(chart: alt.Chart) -> typeNoReturn:
    # a helpful wrapper around altair_viewer.altview
    altview.show(chart)


class Vizkit(object):
    """
    The interface between Click.command, Altair.Chart, and Pandas.dataframe
    """

    viz_type = "abstract"
    viz_info = (
        f"""A {viz_type} visualization"""  # this should be defined in every subclass
    )
    viz_epilog = ""

    def __init__(self, input_file, kwargs):
        self.kwargs = kwargs
        self.warnings = []

        self.input_file = input_file
        self._dataframe = pd.read_csv(self.input_file)
        # TODO: too many properties?
        self.theme = kwargs.get("theme")
        self.channels = self.prepare_channels()
        self.style_properties = self.prepare_styles()
        self.interactive_mode = self.kwargs.get("is_interactive")

        # the chart itself
        self.chart = self.build_chart(
            channels=self.channels,
            style_properties=self.style_properties,
            interactive_mode=self.interactive_mode,
        )

        self._manage_legends()  # TODO: this is only here b/c no better place to put it yet
        self._manage_axis()

    ##########################################################
    # These are boilerplate methods, unlikely to be subclassed
    ##########################################################
    def build_chart(
        self, channels: dict, style_properties: dict, interactive_mode: bool
    ) -> alt.Chart:
        chart = self._create_chart()
        chart = chart.encode(**channels)

        # import IPython; IPython.embed()

        chart = chart.properties(**style_properties)

        if interactive_mode:
            chart = chart.interactive()

        return chart

    def output_chart(self, oargs={}) -> typeNoReturn:
        # --interactive/--static chart is independent of whether or not we're previewing it,
        #  which is reflected in its JSON representation
        # echo JSON before doing a preview

        oargs = self.output_kwargs if not oargs else oargs

        if oargs["to_json"]:
            clout(self.chart.to_json(indent=2))

    def preview_chart(self) -> typeUnion[typeNoReturn, bool]:
        if not self.kwargs.get("no_preview"):
            open_chart_in_browser(self.chart)
        else:
            return False

    def _manage_axis(self) -> typeNoReturn:
        """
        expects self.chart and self.channels to have been initialized; alters alt.chart inplace

        TODO: no idea where to put this, other than to make it an internal method used by build_chart()

        """
        if self.channels.get("facet"):
            self.chart = self.chart.resolve_axis(x="independent")

    def _manage_legends(self) -> typeNoReturn:
        """
        expects self.channels to already have been prepared; alters them inplace

        TODO: no idea where to put this, other than to make it an internal method used by build_chart()
        """
        channels = self.channels

        for cname in (
            "fill",
            "size",
            "stroke",
        ):
            if channel := channels.get(cname):
                channel.legend = self._config_legend(
                    self.legend_kwargs, channel_name=self.resolve_channel_name(channel)
                )

        return

    #################### prepare
    def prepare_channels(
        self,
    ) -> typeDict[str, typeUnion[alt.X, alt.Y, alt.Fill, alt.Size]]:
        """
        TK TODO:
        prepare_channels is the better name
        # TODO: this should be an abstract method in the base class, but for now, it's
        #   an obsolete version of Barkit, for testing ease

        This method does the bespoke work to combine channels with legends/colors/etc
        and should be implemented in every subclass
        """
        channels = self._create_channels(self.channel_kwargs)

        # if self.kwargs.get("flipxy"):
        #     channels["x"], channels["y"] = (channels["y"], channels["x"])
        self._set_channel_colorscale("fill", channels)

        return channels

    def prepare_styles(self) -> typeDict:
        return self._config_styles(self.kwargs)

    #####################################################################
    # internal helpers
    #####################################################################
    def _create_channels(
        self, kwargs: typeDict
    ) -> typeDict[str, typeUnion[alt.X, alt.Y, alt.Fill, alt.Size]]:
        def _validate_fieldname(shorthand: str, fieldname: str) -> bool:
            if fieldname not in self.column_names:
                return False
            else:
                return True

        channels = {}
        # configure x and y channels, which default to 0 and 1-indexed column
        # if names aren't specified

        cargs = kwargs.copy()
        for i, n in enumerate(
            (
                "xvar",
                "yvar",
            )
        ):
            # TODO: this kind of rickety tbh
            #   colstr can be either a column name or Altair's shorthand syntax, e.g. 'sum(amount):Q'
            #   if kwargs['xvar/yvar'] isn't defined, then pull 0/1 index from column_names
            cargs[n] = cargs[n] if cargs[n] else self.column_names[i]

        for n in ENCODING_CHANNEL_NAMES:
            argname = f"{n}var"
            if shorthand := cargs[argname]:
                ed = parse_shorthand(shorthand, data=self.df)

                if _validate_fieldname(shorthand=shorthand, fieldname=ed["field"]):
                    _channel = getattr(alt, n.capitalize())  # e.g. alt.X or alt.Y
                    channels[n] = _channel(**ed)
                else:
                    raise InvalidDataReference(
                        f"""'{shorthand}' is either an invalid column name, or invalid Altair shorthand"""
                    )

        ##################################################################
        # set xlim and ylim, if they exist
        for i in (
            "x",
            "y",
        ):
            j = f"{i}lim"
            if limstr := self.kwargs.get(j):
                channels[
                    i
                ].scale = (
                    alt.Scale()
                )  # if channels[i].scale == alt.Undefined else channels[i].scale
                _min, _max = [k.strip() for k in limstr.split(",")]
                channels[i].scale.domain = [_min, _max]

        #################################
        # set facets, i.e. grid
        if channels.get("facet"):
            if _fc := kwargs["facetcolumns"]:
                channels["facet"].columns = _fc

        return channels

    def _create_chart(self) -> alt.Chart:
        alt.themes.enable(self.theme)

        chartfoo = getattr(alt.Chart(self.df), self.mark_type)
        return chartfoo(clip=True)

    def _set_channel_colorscale(self, channelvar: str, channels: dict) -> typeNoReturn:
        """
        Given a channelvar, e.g. 'fill', 'stroke'

        Check self.channels[channelvar] to see if it's been created

        If so, modify self.channels[channelvar].range

        If not, do nothing, but issue a warning that self.channels[channelvar] was expected

        """
        ## fill color stuff
        #         channel = self.channels.get(channelvar)
        colorargs = {
            k: self.kwargs[k]
            for k in (
                "colors",
                "color_scheme",
            )
            if self.kwargs.get(k)
        }

        if channel := channels.get(channelvar):
            config = {"scheme": DEFAULT_COLOR_SCHEME}
            if colorargs:
                if _cs := colorargs.get("color_scheme"):
                    config["scheme"] = _cs
                    # TODO: if _cs does not match a valid color scheme, then raise a warning/error

                if _cx := colorargs.get("colors"):
                    # don't think this needs to be a formal parser
                    config["range"] = _cx.strip().split(",")
                    # for now, only colors OR color_scheme can be set, not both
                    config.pop("scheme", None)
            channel.scale = alt.Scale(**config)
        else:  # optional expected channel is not present
            if colorargs:  # but color settings were present
                self.warnings.append(
                    f"The {channelvar} variable was not specified, so colors/color_scheme is ignored."
                )

    #####################################################################
    # properties
    @property
    def name(self) -> str:
        return self.viz_type

    @property
    def mark_type(self) -> str:
        return lookup_mark_method(self.viz_type)

    @property
    def df(self) -> pd.DataFrame:
        return self._dataframe

    @property
    def column_names(self) -> typeList[str]:
        return list(self.df.columns)

    #####################################################################
    #  kwarg properties
    #  TODO: refactor later
    @property
    def channel_kwargs(self) -> typeDict:
        _ARGKEYS = [f"{n}var" for n in ENCODING_CHANNEL_NAMES] + ["facetcolumns"]
        return {k: self.kwargs.get(k) for k in _ARGKEYS}

    @property
    def color_kwargs(self) -> typeDict:
        _ARGKEYS = (
            "color_scheme",
            "colors",
        )
        return {k: self.kwargs.get(k) for k in _ARGKEYS}

    @property
    def legend_kwargs(self) -> typeDict:
        _ARGKEYS = (
            "no_legend",
            "TK-orient",
            "TK-title",
        )
        return {k: self.kwargs.get(k) for k in _ARGKEYS}

    @property
    def output_kwargs(self) -> typeDict:
        _ARGKEYS = (
            "to_json",
            "no_preview",
        )
        return {k: self.kwargs.get(k) for k in _ARGKEYS}

    # Not needed if there are no other interactive-like attributes
    # @property
    # def render_kwargs(self) -> typeDict:
    #     _ARGKEYS = ('is_interactive',)
    #     return {k: self.kwargs.get(k) for k in _ARGKEYS}

    # @property
    # def sorting_kwargs(self) -> typeDict:
    #     _ARGKEYS = ("sortx_var",)
    #     return {k: self.kwargs.get(k) for k in _ARGKEYS}

    @property
    def styling_kwargs(self) -> typeDict:
        _ARGKEYS = ("title",)
        return {k: self.kwargs.get(k) for k in _ARGKEYS}

    #####################################################################
    ##### chart aspect configurations (static helper methods)

    @staticmethod
    def _config_legend(
        kwargs: typeDict, channel_name: str = ""
    ) -> typeUnion[typeDict, bool]:

        config = {}
        if kwargs["no_legend"]:
            config = None
        else:
            config["orient"] = DEFAULT_LEGEND_ORIENTATION
            config["title"] = channel_name
        # else:
        #     # TODO: let users configure orientation and title...somehow
        #     config["title"] = colname if not kwargs.get("TK-column-title") else colname
        #     if _o := kwargs.get("TK-orientation"):
        #         config["orient"] = _o
        #     else:
        #         config["orient"] = DEFAULT_LEGEND_ORIENTATION
        return config

    # @staticmethod
    # def _config_sorting(kwargs: typeDict) -> typeDict:
    #     config = {}
    #     if _sortx := kwargs.get("sortx_var"):
    #         _sign, _cname = re.match(r"(-?)(.+)", _sortx).groups()

    #         # TODO: this needs to be changed; should handle altair shorthand: https://stackoverflow.com/questions/52877697/order-bar-chart-in-altair
    #         config["field"] = _cname
    #         config["order"] = "descending" if _sign == "-" else "ascending"

    #     return config

    @staticmethod
    def _config_styles(kwargs: typeDict) -> typeDict:
        config = {}

        if _title := kwargs.get("title"):
            config["title"] = _title

        return config

    @classmethod
    def register_command(klass):
        # TODO: this is bad OOP; _foo should be properly named and in some more logical place
        def _foo(**kwargs):
            try:
                vk = klass(input_file=kwargs.get("input_file"), kwargs=kwargs)
            except (InvalidDataReference, MissingDataReference) as err:
                clexit(1, err)
            else:
                vk.output_chart()
                for w in vk.warnings:
                    clerr(f"Warning: {w}")
                vk.preview_chart()

        command = _foo
        command = click.command(
            name=klass.viz_type, help=klass.viz_info, epilog=klass.viz_epilog
        )(command)
        command = standard_options_decor(command)
        for decor in reversed(klass.COMMAND_DECORATORS):
            command = decor(command)

        return command

    @staticmethod
    def resolve_channel_name(
        channel: typeUnion[alt.X, alt.Y, alt.Fill, alt.Size]
    ) -> str:
        return next(
            (
                getattr(channel, a)
                for a in ("title", "field", "aggregate")
                if getattr(channel, a) != altUndefined
            ),
            altUndefined,
        )
