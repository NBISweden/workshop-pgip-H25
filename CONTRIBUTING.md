# Contributor guide

We welcome contributions to this repository in the form of bug
reports, feature requests, and pull requests. Please read through and
follow the guidelines detailed below.

# Development environment

For local development of slide material you will need the following
prerequisites:

- [Quarto](https://quarto.org/)
- [pixi](https://pixi.sh/latest/)
- R packages listed in `pixi.toml` (install with `pixi update`)

## Linting

The manifest contains a task called `lint` which will run code
linters, such as `pre-commit`, on the source code. Run

```
pixi run lint
```

to run the `lint` task list.

### Tips and tricks

The markdown linter will throw an error whenever lines exceed 88
characters (rule `MD013`). Long lines are sometimes unavoidable for
links. To disable the linter, enclose the affected lines with a
`markdownlint-disable` comment:

```
<!-- markdownlint-disable MD013 -->

Long line here that throws an error

<!-- markdownlint-enable MD013 -->
```

# Building the site with Quarto

There are two pre-defined tasks to build the site.

## Preview

The `qpv` task will run [`quarto
preview`](https://quarto.org/docs/websites/#website-preview) and will
launch a browser with the rendered website:

```
pixi r qpv
```

This is the preferred command for development as changes to source
will automatically reload the browser.

## Render

The `qrd` task will run [`quarto
render`](https://quarto.org/docs/projects/quarto-projects.html#rendering-projects):

```
pixi r qrd
```

# Images

Make sure to compress image files as much as you can so as not to
bloat the repository. For example, to compress `png` files you can run

```
pngquant -q 10 --output filename.png filename.png -f
```

and for `jpg` files

```
jpegoptim --size 100k --force -o filename.jpg
```

You can adjust the parameters in case you think the quality becomes
too poor. The colors can at times become less clear and crisp, but
that is a small price to pay for reduction in size.

Another alternative is to use the smaller
[webp](https://developers.google.com/speed/webp) format.

# Presentation material

## Slide structure

Some recommendations on how to structure the slides. Sections are at
level 1, slides are at level 2.

### Fenced divs

Use fenced divs wherever possible for grouping content:

```
## Slide

:::{}

- item 1
- item 2

:::
```

### Columns

Use `.columns` div for multi-column content.

```
## Slide

:::: {.columns}

::: {.column width="50%"}

:::

::: {.column width="50%"}

:::

::::
```

### Citations

Wherever possible, use the custom `.flushright` div to flush citations
to the right.

```
## Slide

::: {.flushright}

@citation-key

:::
```

### Notes

The use of notes is encouraged for links, background information and
more. Notes will show up in presenter view, but can also be a resource
should we convert slides into an article.

```
## Slide

::: {.notes}

Links to URLs, data provenance, ...

:::
```

### R code blocks

Use fenced div with `r` tag for R code blocks:

````
## Slide

```{r }
#| label: my-label
#| echo: false
#| eval: true
#| out-width: 100%

## R code here to generate plot / table
```
````

### TikZ figures

The [TikZ](https://tikz.dev/) package can be used to make more complex
diagrams and illustrations. Make sure to set `cache: true`.

````
## Slide

```{r, engine="tikz", fig.ext="svg"}
#| label: tikz-label
#| echo: false
#| eval: true
#| cache: true
#| out-width: 800px
#| out-height: 550px
#| fig-align: center
\begin{tikzpicture}[>=latex]
%% TikZ code here
\end{tikzpicture}
```
````

# Content

Content is organized under folders `slides`, `exercises` and
`recipes`. Each folder contains an index file that lists content. Add
content by adding a subdirectory along with an `index.qmd` file. The
relative path to the index file should be listed in the content index
file and the main `_quarto.yml`.

Slides have been developed using the
[nbis-quarto-revealjs](https://github.com/percyfal/nbis-quarto-revealjs)
Quarto template. Exercises make use of the
[nbis-course](https://github.com/percyfal/nbis-course-quarto) template
(NB: targeted for update!). The recipes are code snippets that have
been used to generate plots and simulations.
