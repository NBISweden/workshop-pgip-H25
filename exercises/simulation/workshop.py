import os
import sys
from datetime import datetime

import tqdm
import yaml
from IPython.core.display import HTML
from jupyterquiz import display_quiz


path = os.path.dirname(os.path.normpath(__file__))


def load_quiz(section):
    with open(os.path.join(path, "assets/quiz.yaml"), encoding="utf-8") as fh:
        try:
            quiz = yaml.safe_load(fh)
        except yaml.YAMLError as e:
            print(e)
    if section in quiz.keys():
        return quiz[section]
    return


scilife_colors = {
    "lime": "#a7c947",
    "lime25": "#e9f2d1",
    "lime50": "#d3e4a3",
    "lime75": "#bdd775",
    "teal": "#045c64",
    "teal25": "#c0d6d8",
    "teal50": "#82aeb2",
    "teal75": "#43858b",
    "aqua": "#4c979f",
    "aqua25": "#d2e5e7",
    "aqua50": "#a6cbcf",
    "aqua75": "#79b1b7",
    "grape": "#491f53",
    "grape25": "#d2c7d4",
    "grape50": "#a48fa9",
    "grape75": "#77577e",
    "lightgray": "#e5e5e5",
    "mediumgray": "#a6a6a6",
    "darkgray": "#3f3f3f",
    "black": "#202020",
}

color_dict = {
    "--jq-multiple-choice-bg": scilife_colors[
        "lime"
    ],  # Background for the question part of multiple-choice questions
    "--jq-mc-button-bg": scilife_colors[
        "teal25"
    ],  # Background for the buttons when not pressed
    "--jq-mc-button-border": scilife_colors["teal50"],  # Border of the buttons
    "--jq-mc-button-inset-shadow": scilife_colors[
        "teal75"
    ],  # Color of inset shadow for pressed buttons
    "--jq-many-choice-bg": scilife_colors[
        "lime"
    ],  # Background for question part of many-choice questions
    "--jq-numeric-bg": scilife_colors[
        "lime"
    ],  # Background for question part of numeric questions
    "--jq-numeric-input-bg": scilife_colors[
        "lime75"
    ],  # Background for input area of numeric questions
    "--jq-numeric-input-label": scilife_colors[
        "lime"
    ],  # Color for input of numeric questions
    "--jq-numeric-input-shadow": scilife_colors[
        "lime75"
    ],  # Color for shadow of input area of numeric questions when selected
    "--jq-incorrect-color": scilife_colors["grape"],  # Color for incorrect answers
    "--jq-correct-color": scilife_colors["teal50"],  # Color for correct answers
    "--jq-text-color": scilife_colors["lime25"],  # Color for question text
}


class DownloadProgressBar(tqdm.tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


styles = """dl.exercise {
    border: #a7c947 1px solid;
    margin-top: 1em;
}
.exercise dt {
    color: #e9f2d1; background-color: #a7c947;
    padding: 6px; display: block;
}
.exercise dt::before {
    content: '🧐 ';
}
.exercise dd {
    padding: 6px;
}
"""


class Workbook:
    styles = styles
    css = f"<style>{styles}</style>"
    js = "<script src='https://d3js.org/d3.v7.min.js'></script>"
    # See https://github.com/jupyterlite/jupyterlite/issues/407#issuecomment-1353088447
    html_text = [
        """<table style="width: 100%;"><tr>
        <td style="text-align: left;">✅ Your notebook is ready to go!</td>""",  # => 0
        """<td style="text-align: right;">
        <button type="button" id="button_for_indexeddb">Clear JupyterLite local storage
        </button></td>""",  # => 1 (omit if not in jlite)
        "</tr></table>",  # => 2
        """<script>
        window.button_for_indexeddb.onclick = function(e) {
            window.indexedDB.open('JupyterLite Storage').onsuccess = function(e) {
                // There are also other tables that I'm not clearing:
                // "counters", "settings", "local-storage-detect-blob-support"
                let tables = ["checkpoints", "files"];

                let db = e.target.result;
                let t = db.transaction(tables, "readwrite");

                function clearTable(tablename) {
                    let st = t.objectStore(tablename);
                    st.count().onsuccess = function(e) {
                        console.log("Deleting " + e.target.result +
                        " entries from " + tablename + "...");
                        st.clear().onsuccess = function(e) {
                            console.log(tablename + " is cleared!");
                        }
                    }
                }

                for (let tablename of tables) {
                    clearTable(tablename);
                }
            }
        };
        </script>""",  # => 3 (omit if not in jlite)
    ]

    # Used for making SVG formatting smaller
    small_class = "x-lab-sml"
    small_style = (
        ".x-lab-sml .sym {transform:scale(0.6)} "
        ".x-lab-sml .lab {font-size:7pt;}"  # All labels small
        ".x-lab-sml .x-axis .tick .lab {"
        "font-weight:normal;transform:rotate(90deg);text-anchor:start;dominant-baseline:central;}"  # noqa
    )

    def __init__(self):
        name = type(self).__name__
        self.quiz = load_quiz(name)

    def question(self, label):
        display_quiz(self.quiz[label], colors=color_dict)

    @staticmethod
    def download(url):
        return DownloadProgressBar(
            unit="B", unit_scale=True, miniters=1, desc=url.split("/")[-1]
        )

    @property
    def setup(self):
        if "pyodide" in sys.modules:
            return HTML(self.js + self.css + "".join(self.html_text))
        else:
            return HTML(
                self.js + self.css + "".join([self.html_text[0], self.html_text[2]])
            )


class HOWTO(Workbook):
    def __init__(self):
        super().__init__()
        self.quiz["day"][0]["answers"][0]["value"] = datetime.today().day


class Simulation(Workbook):
    def __init__(self):
        super().__init__()


class Stdpopsim(Workbook):
    def __init__(self):
        super().__init__()


class ARGInference(Workbook):
    def __init__(self):
        super().__init__()
