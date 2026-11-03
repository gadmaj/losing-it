# losing-it

A small, local CodingBat-style physics practice app with Python and C++ support.
Includes 30 exercises: Homework 8, the Spring 2026 midterm, and the Fall 2025 midterm.

## Run

Requires Linux, Python 3.10 or newer, Bubblewrap (`bwrap`), and GCC (`g++`) with
C++20 support. No Python packages, npm installation, or runtime internet access
are needed.

```sh
git clone https://github.com/gadmaj/losing-it.git
cd losing-it
python3 codingbat_gui/app.py
```

Open <http://127.0.0.1:8765>. On a Linux desktop, you can also run
`bash "Start Physics Practice.sh"` to start the server and open your browser.

## Editor

- Python and C++ syntax highlighting, line numbers, an active-line highlight,
  and a line/column indicator.
- Alt-drag for rectangular selection; Alt-click for another cursor.
- Ctrl-Alt-Up/Down to add a cursor on the adjacent line; Escape returns to one.
- Completion for parameters and variables declared earlier in your code.
  Type two letters or press Ctrl-Space; Tab/Enter accepts and Escape dismisses.
- Tab/Shift-Tab indents or unindents selected lines, plus autoindent,
  matching brackets, and undo/redo.
- Ctrl-Enter runs your function. C++20 test drivers are supplied automatically;
  you do not need `main()`.

Code and progress are saved in your browser, separately for each exercise set
and language. Runs happen in a resource-limited Bubblewrap process on your own
computer. The server listens only on `127.0.0.1`.

## Exercise material

The exercise text, test cases, and extracted diagrams are included. Original
PDF/HTML downloads are ignored by Git. The app works without them; if the
original PDFs are placed beside this README using their original filenames,
the matching **Original PDF** links appear automatically.

HW8 can also be used from the terminal:

```sh
python3 physics_leetcode.py --show 1
```

CodeMirror 5.65.16 is bundled locally under its MIT license; see
[`codingbat_gui/vendor/codemirror/LICENSE`](codingbat_gui/vendor/codemirror/LICENSE).
