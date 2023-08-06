# Zoia

`zoia` is a utility to organize your library of academic papers.

## Installation

You can install `zoia` by running:

```sh
pip install zoia
```

## Organization

`zoia` uses a simple, flat layout to organize data.  Every paper is referenced
by a unique citation key (typically shortened to "citekey").  This would be
the same key that you would reference with `citep` or `citet` in LaTeX.
Bibliographic data is by default stored in a SQLite database called
`metadata.db` which is located in `$HOME/.local/share/zoia`.

Each paper also gets its own subdirectory in the root directory.  Within each
subdirectory the document (if it exists) is stored as `document.pdf`.  Any
notes associated with the document are stored as `notes.md`.  However, `zoia`
imposes no additional structure on the layout.  If you would like to add
additional files for a paper (e.g., supplementary data, code, or text), you are
free to do so.

A sample directory structure might look like this:

```
my_library
         └── einstein05-electrodynamics
             ├── document.pdf
             └── notes.md
```

## Citation key style

`zoia`'s citation key style is based on [Harvard
referencing](https://en.wikipedia.org/wiki/Parenthetical_referencing).  `zoia`
generates citekeys by taking the last names of the first three authors on the
paper and joining them by `+`, (with a trailing `+` if there are more than
three authors), followed by the last two digits of the publication year,
followed by a hyphen, followed by the first word of the title (excluding common
words like "the", "a", "on", etc.).  

### Examples

| Author(s)                                 | Title                                                                          | Year | Citation key                  |
| --------                                  | -----                                                                          | ---- | ------------                  |
| Einstein, A.                              | On the electrodynamics of moving bodies                                        | 1905 | einstein05-electrodynamics    |
| Einstein, A., and Rosen, N.               | The particle problem in the general theory of relativity                       | 1935 | einstein+rosen35-particle     |
| Abbott, B. P., et al.                     | Observation of Gravitational Waves from a Binary Black Hole Merger             | 2016 | abbott+16-obseravtion         |

### Collisions

Inevitably you will one day try to add two different papers which have the same
auto-generated citation keys.  The default style makes this rare, but does not
guarantee that it will never happen.  When it does, `zoia` will add the
character `b` after the year.  For example, suppose a lesser known physicist by
the name of Egbert Einstein had written another, somewhat less revolutionary,
paper in 1905 called "On the electrodynamics of stationary bodies".  If you
tried to add it, it would get a citekey of `einstein05b-electrodynamics`.  If
the citekey with the `b` already exists, `zoia` will try adding a `c`, and then
a `d`, etc. all the way up to `z`.  If that's still not good enough it will
continue with `aa`, `ab`, etc., though pray that things never come to that.

Note that the first paper will retain its original citekey --- it won't get an
`a` added to it.  This is because you may have been using that old citekey in
your papers.  Changing the citekey would break that link.

## Configuration

`zoia` follows the XDG standard and stores its configuration data in
`$XDG_CONFIG_HOME/zoia` if the `XDG_CONFIG_HOME` environment variable is set.
If it is not set it uses the standard default of `$HOME/.config/zoia`.
Whatever the directory, `zoia` keeps its configuration data in file called
`config.yaml`.

## Usage

### Initialization

After you have installed `zoia` you can initialize your library by running:

```
zoia init [directory]
```

This will tell `zoia` that your library is going to be stored in the provided
directory.  (Note that this directory must be empty.)  If you don't provide a
directory, `zoia` will store your library in your current working directory if
it is empty.  If it isn't empty, it will try creating a subdirectory named
`zoia` and will store your library there (assuming that that subdirectory
doesn't already exist).

### Adding a paper

Once you have initialized your library, you can add items by specifying an
identifier.  The following identifiers are currently supported:

* arXiv IDs
* DOIs
* ISBNs

`zoia` will figure out what kind of identifier you've given it on its own:

```sh
zoia add 1602.03837
zoia add 10.1103/PhysRevLett.116.061102
zoia add 9781400889099
```

It's also fine to include prefixes like `arxiv:1602.03837` or
`doi:10.1103/PhysRevLett.116.061102`.

`zoia` will add the paper's metadata to the `.metadata.json` file and download
the PDF if it is on the arXiv.  (If you provide a DOI, `zoia` will still check
to see if the paper exists on the arXiv and download it if it does.)

In the future `zoia` will also support adding papers by their PDFs directly.

### Opening a paper

You can open the PDF of a paper in your library from its citekey by running:

```
zoia open <citekey>
```

This will open the PDF using your default PDF viewer.  In the future it will be
possible to also open the PDF based on the arXiv ID, DOI, or ISBN.

### Taking notes on a paper

`zoia` keeps your notes for a paper in a Markdown file called `notes.md` in
that paper's subdirectory.  You can edit that file in your default editor by
running:

```
zoia note <citekey>
```

### Editing a paper's metadata

If there is an error in a paper's metadata, you can edit it by running:

```
zoia edit <citekey>
```

By default `zoia` will present the data in JSON format, but if you prefer YAML,
you can specify that with the `--syntax=yaml` option.

## Synchronization

Although `zoia` does not natively support synchronization across multiple
devices at the moment, its simple data structure makes it easy to use with
third-party synchronization software.  In particular I recommend using
[Syncthing](https://syncthing.net/) for this purpose.  By pointing Syncthing at
the directory containing `zoia`'s library on both devices you can keep your
library synchronized.

## About the name

`zoia` is named in honor of the librarian [Zoia
Horn](https://en.wikipedia.org/wiki/Zoia_Horn) who spent her life fighting for
intellectual and academic freedom.
