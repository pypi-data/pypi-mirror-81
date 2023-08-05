#!/usr/bin/env python

"""
Converts notebooks to interactive HTML pages with Juniper + Binder.

Usage:
  nbjuniper TARGET (-f juniper_settings.yaml)
  nbjuniper (-h | --help)

`nbjuniper example_notebook.ipynb ...` converts example_notebook.ipynb into example_notebook.html.

Arguments:
  TARGET                     IPython notebook to convert. If TARGET is a directory, nbjuniper will
                             render all .ipynb files in that directory (non-recursively by default).

Options:
  -h --help                  Show this screen.
  -f FILENAME                yaml file containing specific settings for the Juniper client.
                             See https://github.com/ines/juniper for all possibilities, and
                             this project's README.md for an example.
  -r TARGET                  Recursively render all .ipynb files within TARGET (should be a directory)
  --no-head                  Skip writing the HTML head to the page.
  --decapitate               Write the HTML head to a separate file (juniper_head.html).
  --binderhub                BinderHub instance to which to connect (default is https://mybinder.org).
  --repo                     Github repository used to build Binder Docker image on the BinderHub.
                             (default is the very minimal ashtonmv/python_binder).
  --theme                    Supported themes are 'callysto' (default), 'monokai', 'material', and
                             'neat'.

See the README.md for a more complete explanation of nbjuniper options and usage.
"""

import os
import json
import yaml
import sys
from markdown import markdown


def collect_notebooks(directory, recursive=False):
    notebooks = {}
    if recursive:
        for root, dirs, files in os.walk(directory):
                for name in files:
                    nb = os.path.join(root, name)
                    if nb.endswith(".ipynb"):
                        with open(nb) as f:
                            notebooks[nb] = json.load(f)
    else:
        for nb in [os.path.join(directory, nb) for nb in
                   os.listdir(directory) if nb.endswith(".ipynb")]:
            with open(nb) as f:
                notebooks[nb] = json.load(f)
    return notebooks


def main():

    settings = {
        "url": "https://mybinder.org",
        "repo": "ashtonmv/python_binder",
        "theme": "callysto",
        "msgLoading": " ",
        "useStorage": True,
        "isolateCells": False
    }

    notebooks = {}
    for i, arg in enumerate(sys.argv):
        if i == 1:
            if arg.lower() in ["-h", "--help"]:
                print(__doc__)
                return
            else:
                if os.path.isfile(arg):
                    with open(arg) as f:
                        notebooks[arg] = json.load(f)
                elif os.path.isdir(arg):
                    recursive = "-r" in sys.argv
                    notebooks = collect_notebooks(arg, recursive)
                elif arg.lower() == "-r":
                    notebooks = collect_notebooks(sys.argv[i+1], recursive=True)

        if arg.lower() == "-f":
            with open(sys.argv[i+1]) as f:
                settings.update(yaml.safe_load(f))

        elif arg.lower() == "--binderhub":
            settings.update({"url": sys.argv[i+1]})

        elif arg.lower() == "--repo":
            settings.update({"repo": sys.argv[i+1]})

        elif arg.lower() == "--theme":
            settings.update({"theme": sys.argv[i+1]})

    if len(notebooks) == 0:
        raise ValueError("Please specify a valid notebook to convert: nbjuniper example_notebook.ipynb")

    theme = settings["theme"]

    for k, v in settings.items():
        if type(v) != bool:
            settings[k] = f"'{v}'"
        else:
            settings[k] = str(v).lower()

    juniper_json = ", ".join([f"{key}: {value}" for key, value in settings.items()]) 

    head = [
        "<head>",
        "  <script type='text/javascript' src='https://code.jquery.com/jquery-3.5.1.min.js'></script>",
        "  <script type='text/javascript' src='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/cdn/juniper.min.js'></script>",
        "  <script type='text/javascript' src='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/cdn/events.js'></script>",
        "  <script type='text/javascript' src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>",
        f"  <script>$(document).ready(function() {{new Juniper({{ {juniper_json} }})}});</script>",
        f"  <link rel='stylesheet' href='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/cdn/styles/{theme}.css'></link>",
        "</head>",
    ]

    for filename in notebooks:
        notebook = notebooks[filename]
        body = ["<body>"]
        body.append("<div class='juniper-notebook'>")
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                body.append("<pre data-executable>")
                body.append("".join(cell["source"]))
                body.append("</pre>")
            else:
                body.append(markdown("".join(cell["source"])))
        body.append("</div>")
        body.append("</body>")

        if "--no-head" not in sys.argv and "--decapitate" not in sys.argv:
            with open(filename.replace("ipynb", "html"), "w") as o:
                o.write("\n".join(head))
                o.write("\n".join(body))
        else:
            with open(filename.replace("ipynb", "html"), "w") as o:
                o.write("\n".join(body))

    if "--no-head" not in sys.argv:
        with open("juniper_head.html", "w") as o:
            o.write("\n".join(head))

if __name__ == "__main__":
    main()
