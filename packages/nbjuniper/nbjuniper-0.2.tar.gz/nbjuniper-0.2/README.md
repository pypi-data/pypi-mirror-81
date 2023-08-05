# nbjuniper
Convert Jupyter Notebooks into runnable HTML files with [Juniper](https://github.com/ines/juniper)

<img src="screenshot.png" width="100%"/>

---

## Standalone usage
```sh
nbjuniper example_notebook.ipynb
```

The above command will create (or clobber if it exists!) the file example_notebook.html,
which can be opened as a standalone webpage or embedded in another page. 

## Jupyter-book usage

To activate Junper for all code cells in documentation that has already been built with
`jupyter-book build`, use the jupyter-book mode (it is automatically recursive):

```sh
nbjuniper documentation_folder -m jupyter-book
```

This command adds an nbjuniper header to each HTML file in your documentation. It will
only change the appearance and behavior of code cells.

## Under the hood

`nbjuniper` creates _Juniper_ notebooks- they are *not* quite the same as _Ipython/Jupyter_ notebooks ([what's the difference?](#what-nbjuniper-cannot-do)) The html
file(s) created by `nbjuniper` automatically link your code to a [MyBinder](https://mybinder.org) instance that
serves as the backend for executing the code.

## Defaults and how to override them

### MyBinder repository
By default, `nbjuniper` connects your code to my extremely minimal python Binder ([ashtonmv/python_binder](https://github.com/ashtonmv/python_binder)), where only python and its native libraries are installed. If your code has any dependencies, you'll
want to connect it to your own MyBinder docker image. If you haven't done so, create the MyBinder image for your repo [here](https://mybinder.org) and then run

```sh
nbjuniper example_notebook.ipynb --repo github_username/binder_repo
```

Where you've replaced `github_username` with your github username and `binder_repo` with the name of the repository for which you've created the MyBinder docker image.

### Using other BinderHubs
If you have your own BinderHub or are hosting your notebook on someone else's hub (e.g. [GESIS](https://notebooks.gesis.org)),
you'll want to override MyBinder.org as the default server:

```sh
nbjuniper example_notebook.ipynb --binderhub https://notebooks.gesis.org --repo github_username/binder_repo
```

### Styling
The default style of the Juniper notebook is the one I created for [callysto](https://michael-ashton.com/callysto),
which has more pink and purple than some of you might be ready for. The theme controls the syntax highlighting in
each cell as well as the cells' general appearance. 

The easiest way to switch themes is using a bundled theme (one of those listed under cdn/styles):

```sh
nbjuniper example_notebook.ipynb --theme monokai
```

You can also create your own style and hardcode it in
(see [Removing the html head](#removing-the-html-head)).
If you want to share your own cool theme with others, let me know! I'd love to add it.

### Full control of Juniper settings
For those who are familiar with [Juniper](https://github.com/ines/juniper), (and if you're not check it out! It's awesome)
you can customize every option used to create the Juniper client like so:

```sh
nbjuniper example_notebook.ipynb -f my_juniper_settings.yaml
```

where my_juniper_settings.yaml should have the form

```yaml
url: https://binder.michael-ashton.com  # must be a binderhub with CORS enabled
repo: ashtonmv/conda  # your binder repo
isolateCells: true  # Cells don't pass variables to one another
useStorage: false  # Don't cache the binder (will be slow)
msgLoading: "Loading..."  # msg to display while loading (doesn't go away if no stdout!)
...etc
```

See the [Juniper documentation](https://github.com/ines/juniper) for a full list of settings.

### Removing the html head
If you're going to embed multiple Juniper notebooks into a single page, you don't want to include the html head in
each one. That would import the stylesheet and javascript resources once per notebook, which can slow down your page load
time and is just sloppy. To chop off the head from a Juniper notebook, use the admittedly gruesome command

```sh
nbjuniper example_notebook.ipynb --decapitate
```

This will create two files: the typical example_notebook.html and the severed juniper_head.html. From here you
can either discard juniper_head.html and write your own html head, or you can embed juniper_head.html at the top
of your page where you're including the notebooks so that it's only read in once for the whole page. To prevent writing
the juniper_head.html file at all, replace `--decapitate` with `--no-head`.

### What nbjuniper cannot do
Anything that requires instantaneous feedback between the page and the MyBinder server, including certain widgets
and tab autocompletion, won't work. nbjuniper also intentionally doesn't give you a full jupyter "header"- if you
want the page to look just like a jupyter notebook, there's a good chance you should just be redirecting to
MyBinder itself.
