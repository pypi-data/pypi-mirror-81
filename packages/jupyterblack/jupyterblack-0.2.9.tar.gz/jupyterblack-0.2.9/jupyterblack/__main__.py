"""
Black format your Jupyter Notebook and JupyterLab.
Files must have a .ipynb extension.

Usage:
------

    $ jblack [options] [filename] [filename...]

Format one Jupyter file:

    $ jblack notebook.ipynb

Format multiple Jupyter files:

    $ jblack notebook_1.ipynb notebook_2.ipynb [...]

Format one Jupyter file with a line length of 70:

    $ jblack -l 70 notebook.ipynb


Available options are:

    [-h, --help]                  Show help
    [-l, --line_length] <int>     Set max line length to <int>

"""
import os
import sys
from jupyterblack import cout, parser


def main():
    """Read jupyterblack CLI arguments"""

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    # Sanity check -- don't allow invalid options
    valid_options = ["-h", "--help", "-l", "--line_length"]
    if any(opt not in valid_options for opt in opts):
        cout.invalid_options()
        return

    # Show help message
    if "-h" in opts or "--help" in opts:
        print(__doc__)
        return
    # Set default line length and check for input value
    line_length = 88
    if "-l" in opts or "--line_length" in opts:
        try:
            line_length = int(args.pop(0))
            if not args:
                raise IndexError
        except ValueError:
            cout.invalid_linelength()
            return
        except IndexError:
            cout.no_args()
            return

    if not args:
        cout.no_args()
        return
    # Check if input filename exists and has .ipynb extension
    for filename in args:
        if not os.path.exists(filename):
            cout.invalid_filename(filename)
            return
        if not parser.check_ipynb_extension(filename):
            cout.invalid_extension(filename)
            return

    # Black format .ipynb files
    for ipynb_filename in args:
        jupyter_content = parser.read_jupyter(ipynb_filename)
        jupyter_black = parser.format_jupyter(jupyter_content, line_length=line_length)
        parser.write_jupyter(jupyter_black, ipynb_filename)

    print("All done!")


if __name__ == "__main__":
    main()
