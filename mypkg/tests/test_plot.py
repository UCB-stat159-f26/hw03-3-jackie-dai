"""Run from the repository root with python -m unittest discover -s tests -v."""

import json
import os
import tempfile
import unittest
from importlib import import_module
from io import BytesIO
from pathlib import Path, PurePosixPath
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import urlsplit

import matplotlib
import pandas as pd

matplotlib.use("Agg")
from matplotlib import pyplot as plt

from mypkg.get_tennis_data import get_tennis_data
from mypkg.plot_data import plot_data

download_module = import_module("mypkg.submodules.download")

def match(date, result, opponent, opponent_age_or_birthdate, width=27):
    """Build a synthetic Tennis Abstract row using the homework's field layout."""
    row = [""] * width
    row[:5] = [date, "Example Open", "Hard", "W", result]
    row[11] = opponent
    row[16] = opponent_age_or_birthdate
    return row


def career_js(*matches):
    rows = ",\n  ".join(json.dumps(row) for row in matches)
    return "var morematchmx = [" + rows + "];\n"


MOCK_FILES = {
    "SerenaWilliams.js": "var dob=19810926;\n",
    "SerenaWilliamsCareer.js": career_js(
        match("19951030", "L", "Older Opponent", "19770119"),
        match("19970307", "W", "Younger Opponent", "19830801"),
    ),
    "RafaelNadal.js": "var dob=19860603;\n",
    "RafaelNadalCareer.js": career_js(
        match("20010910", "L", "Older Opponent", "22.264202601", width=43),
        match("20010917", "W", "Younger Opponent", "18.7597535934", width=43),
    ),
}

def fake_urlopen(request, *args, **kwargs):
    url = request if isinstance(request, str) else request.full_url
    filename = PurePosixPath(urlsplit(url).path).name
    if filename in MOCK_FILES:
        return BytesIO(MOCK_FILES[filename].encode("utf-8"))
    raise HTTPError(url, 404, "Not Found", None, BytesIO())


class TestTennisPackage(unittest.TestCase):
    def setUp(self):
        temp_dir = self.enterContext(tempfile.TemporaryDirectory())
        self.addCleanup(os.chdir, os.getcwd())
        os.chdir(temp_dir)
        Path("output").mkdir()
        self.addCleanup(plt.close, "all")
        self.enterContext(patch.object(download_module, "urlopen", side_effect=fake_urlopen))

    def test_serena_name_formats_return_the_same_data(self):
        expected = get_tennis_data("Serena Williams")
        for name in ("serena williams", "SerenaWilliams"):
            with self.subTest(name=name):
                pd.testing.assert_frame_equal(get_tennis_data(name), expected)

    def test_opponent_birthdate_is_converted_to_age(self):
        data = get_tennis_data("Serena Williams").sort_values("date")
        self.assertEqual(data["result"].tolist(), ["L", "W"])
        first, second = data.to_dict("records")
        self.assertEqual(pd.Timestamp(first["date"]), pd.Timestamp("1995-10-30"))
        self.assertAlmostEqual(first["player_age"], 14.09, delta=0.02)
        self.assertAlmostEqual(first["age_diff"], -4.69, delta=0.02)
        self.assertAlmostEqual(second["age_diff"], 1.85, delta=0.02)

    def test_numeric_opponent_age_is_used_directly(self):
        data = get_tennis_data("Rafael Nadal").sort_values("date")
        self.assertEqual(data["result"].tolist(), ["L", "W"])
        first, second = data.to_dict("records")
        self.assertAlmostEqual(first["player_age"], 15.27, delta=0.02)
        self.assertAlmostEqual(first["age_diff"], -7.00, delta=0.02)
        self.assertAlmostEqual(second["age_diff"], -3.47, delta=0.02)

    def test_unknown_player_has_a_meaningful_error(self):
        message = (
            r"(?i)gaston\s*sanchez|(?:unknown|invalid|no such) player"
            r"|player.*(?:not found|does not exist)"
        )
        with self.assertRaisesRegex(Exception, message):
            get_tennis_data("Gaston Sanchez")

    def test_plot_uses_player_age_age_difference_and_result(self):
        data = get_tennis_data("Serena Williams")
        figure = plot_data(data)
        figure.canvas.draw()

        points = []
        for collection in figure.axes[0].collections:
            offsets = collection.get_offsets()
            colors = collection.get_facecolors()
            for index, (x, y) in enumerate(offsets):
                color = colors[0 if len(colors) == 1 else index]
                points.append((x, y, tuple(color)))

        self.assertEqual(len(points), len(data))
        colors_by_result = {}
        expected = data.sort_values("player_age").itertuples()
        for (x, y, color), row in zip(sorted(points), expected):
            self.assertAlmostEqual(x, row.player_age)
            self.assertAlmostEqual(y, row.age_diff)
            colors_by_result[row.result] = color
        self.assertNotEqual(colors_by_result["W"], colors_by_result["L"])
