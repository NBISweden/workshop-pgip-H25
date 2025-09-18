import os
import sys
from datetime import datetime

import tqdm
import yaml
import numpy as np
import tskit
import pandas as pd
from IPython.core.display import HTML
from jupyterquiz import display_quiz


path = os.path.dirname(os.path.normpath(__file__))


def load_quiz(section):
    with open(os.path.join(path, "quiz.yaml"), encoding="utf-8") as fh:
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


class StdpopsimII(Workbook):
    def __init__(self):
        super().__init__()


class ARGInference(Workbook):
    def __init__(self):
        super().__init__()


# Straight from tskit tests.test_stats
def parse_time_windows(ts, time_windows):
    if time_windows is None:
        time_windows = [0.0, ts.max_root_time]
    return np.array(time_windows)


def windowed_genealogical_nearest_neighbours(
    ts,
    focal,
    reference_sets,
    windows=None,
    time_windows=None,
    span_normalise=True,
    time_normalise=True,
):
    """
    genealogical_nearest_neighbours with support for span- and time-based windows
    """
    reference_set_map = np.full(ts.num_nodes, tskit.NULL, dtype=int)
    for k, reference_set in enumerate(reference_sets):
        for u in reference_set:
            if reference_set_map[u] != tskit.NULL:
                raise ValueError("Duplicate value in reference sets")
            reference_set_map[u] = k

    windows_used = windows is not None
    time_windows_used = time_windows is not None
    windows = ts.parse_windows(windows)
    num_windows = windows.shape[0] - 1
    time_windows = parse_time_windows(ts, time_windows)
    num_time_windows = time_windows.shape[0] - 1
    A = np.zeros((num_windows, num_time_windows, len(focal), len(reference_sets)))
    K = len(reference_sets)
    parent = np.full(ts.num_nodes, tskit.NULL, dtype=int)
    sample_count = np.zeros((ts.num_nodes, K), dtype=int)
    time = ts.tables.nodes.time
    norm = np.zeros((num_windows, num_time_windows, len(focal)))

    # Set the initial conditions.
    for j in range(K):
        sample_count[reference_sets[j], j] = 1

    window_index = 0
    for (t_left, t_right), edges_out, edges_in in ts.edge_diffs():
        for edge in edges_out:
            parent[edge.child] = tskit.NULL
            v = edge.parent
            while v != tskit.NULL:
                sample_count[v] -= sample_count[edge.child]
                v = parent[v]
        for edge in edges_in:
            parent[edge.child] = edge.parent
            v = edge.parent
            while v != tskit.NULL:
                sample_count[v] += sample_count[edge.child]
                v = parent[v]

        # Update the windows
        assert window_index < num_windows
        while windows[window_index] < t_right and window_index + 1 <= num_windows:
            w_left = windows[window_index]
            w_right = windows[window_index + 1]
            left = max(t_left, w_left)
            right = min(t_right, w_right)
            span = right - left
            # Process this tree.
            for j, u in enumerate(focal):
                focal_reference_set = reference_set_map[u]
                delta = int(focal_reference_set != tskit.NULL)
                p = u
                while p != tskit.NULL:
                    total = np.sum(sample_count[p])
                    if total > delta:
                        break
                    p = parent[p]
                if p != tskit.NULL:
                    scale = span / (total - delta)
                    time_index = np.searchsorted(time_windows, time[p]) - 1
                    if 0 <= time_index < num_time_windows:
                        for k in range(len(reference_sets)):
                            n = sample_count[p, k] - int(focal_reference_set == k)
                            A[window_index, time_index, j, k] += n * scale
                        norm[window_index, time_index, j] += span
            assert span > 0
            if w_right <= t_right:
                window_index += 1
            else:
                # This interval crosses a tree boundary, so we update it again
                # in the next tree
                break

    # Reshape norm depending on normalization selected
    # Return NaN when normalisation value is 0
    if span_normalise and time_normalise:
        reshaped_norm = norm.reshape((num_windows, num_time_windows, len(focal), 1))
    elif span_normalise and not time_normalise:
        norm = np.sum(norm, axis=1)
        reshaped_norm = norm.reshape((num_windows, 1, len(focal), 1))
    elif time_normalise and not span_normalise:
        norm = np.sum(norm, axis=0)
        reshaped_norm = norm.reshape((1, num_time_windows, len(focal), 1))

    with np.errstate(invalid="ignore", divide="ignore"):
        A /= reshaped_norm
    A[np.all(A == 0, axis=3)] = np.nan

    # Remove dimension for windows and/or time_windows if parameter is None
    if not windows_used and time_windows_used:
        A = A.reshape((num_time_windows, len(focal), len(reference_sets)))
    elif not time_windows_used and windows_used:
        A = A.reshape((num_windows, len(focal), len(reference_sets)))
    elif not windows_used and not time_windows_used:
        A = A.reshape((len(focal), len(reference_sets)))
    return A


def haplotype_gnn(
    ts,
    focal_ind,
    windows,
    group_sample_sets,
):
    """Calculate the haplotype genealogical nearest neighbours (GNN)
    for the haplotypes of a focal individual"""
    ind = ts.individual(focal_ind)
    A = windowed_genealogical_nearest_neighbours(
        ts, ind.nodes, group_sample_sets, windows=windows
    )
    dflist = []
    for i in range(A.shape[1]):
        x = pd.DataFrame(A[:, i, :])
        x["haplotype"] = i
        x["start"] = windows[0:-1]
        x["end"] = windows[1:]
        dflist.append(x)
    df = pd.concat(dflist)
    df.set_index(["haplotype", "start", "end"], inplace=True)
    return df
