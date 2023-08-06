# -*- coding: utf-8 -*-
"""Docstring."""
from collections import OrderedDict
from typing import Dict
from typing import Tuple
from typing import Union
import uuid

from immutabledict import immutabledict
from labware_domain_models import LabwareDefinition
from mantarray_waveform_analysis import AMPLITUDE_UUID
from mantarray_waveform_analysis import BESSEL_LOWPASS_10_UUID
from mantarray_waveform_analysis import BUTTERWORTH_LOWPASS_30_UUID
from mantarray_waveform_analysis import CENTIMILLISECONDS_PER_SECOND
from mantarray_waveform_analysis import TWITCH_FREQUENCY_UUID
from mantarray_waveform_analysis import TWITCH_PERIOD_UUID
from mantarray_waveform_analysis import WIDTH_UUID

try:  # adapted from https://packaging.python.org/guides/single-sourcing-package-version/
    from importlib import metadata
except ImportError:  # pragma: no cover
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata  # type: ignore # Eli (9/1/20): for some reason mypy is giving weird errors for this
PACKAGE_VERSION = metadata.version("curibio.sdk")  # type: ignore # Eli (9/1/20): for some reason mypy is giving weird errors for this

TWENTY_FOUR_WELL_PLATE = LabwareDefinition(row_count=4, column_count=6)

MICROSECONDS_PER_CENTIMILLISECOND = 10
METADATA_EXCEL_SHEET_NAME = "metadata"
METADATA_RECORDING_ROW_START = 0
METADATA_INSTRUMENT_ROW_START = METADATA_RECORDING_ROW_START + 4
METADATA_OUTPUT_FILE_ROW_START = METADATA_INSTRUMENT_ROW_START + 6

CONTINUOUS_WAVEFORM_SHEET_NAME = "continuous-waveforms"
AGGREGATE_METRICS_SHEET_NAME = "aggregate-metrics"
WAVEFORM_CHART_SHEET_NAME = "continuous-waveform-plots"

INTERPOLATED_DATA_PERIOD_SECONDS = 1 / 100
INTERPOLATED_DATA_PERIOD_CMS = (
    INTERPOLATED_DATA_PERIOD_SECONDS * CENTIMILLISECONDS_PER_SECOND
)
TSP_TO_DEFAULT_FILTER_UUID = (
    {  # Tissue Sampling Period (centi-milliseconds) to default Pipeline Filter UUID
        960: BESSEL_LOWPASS_10_UUID,
        160: BUTTERWORTH_LOWPASS_30_UUID,
    }
)

DEFAULT_CELL_WIDTH = 64
CHART_HEIGHT = 300
CHART_BASE_WIDTH = 120
CHART_HEIGHT_CELLS = 15
CHART_FIXED_WIDTH_CELLS = 8
CHART_FIXED_WIDTH = DEFAULT_CELL_WIDTH * CHART_FIXED_WIDTH_CELLS
PEAK_VALLEY_COLUMN_START = 100
CHART_WINDOW_NUM_SECONDS = 10
CHART_WINDOW_NUM_DATA_POINTS = (
    CHART_WINDOW_NUM_SECONDS / INTERPOLATED_DATA_PERIOD_SECONDS
)

CALCULATED_METRIC_DISPLAY_NAMES: Dict[
    uuid.UUID, Union[str, Tuple[int, str]]
] = OrderedDict(
    [
        (TWITCH_PERIOD_UUID, "Twitch Period (seconds)"),
        (TWITCH_FREQUENCY_UUID, "Twitch Frequency (Hz)"),
        (AMPLITUDE_UUID, "Twitch Amplitude"),
        (WIDTH_UUID, (50, "Twitch Width 50 (FWHM) (seconds)")),
    ]
)
ALL_FORMATS = immutabledict({"CoV": {"num_format": "0.00%"}})
