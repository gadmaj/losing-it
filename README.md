# losing-it

A small, local CodingBat-style physics practice app with Python and C++ support.
Includes 100 source questions and 598 numerical cases from eight distinct papers
plus Homework 8. Combined PDF downloads are represented by their individual
papers, so importing both does not duplicate the question bank.

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

## Study modes

The startup screen asks what you want to study:

1. Random questions across units, with a question count.
2. A randomized midterm: match the question count and unit distribution of a
   selected paper, or select any question count from the midterm bank.
3. A midterm selected by semester, year, and version.
4. A randomized final exam, with the same format/count choices.
5. A final exam selected by semester and year.
6. Practice within a particular unit.

Random practice can include number variations. Original-paper mode uses the
original values and question order. A saved session can be continued later.
The skill chart counts distinct question types solved by unit; repeated versions
of the same type do not inflate the bars. All progress stays in browser storage.

## Papers and reference material

| Collection | Questions |
| --- | ---: |
| Midterm, Spring 2026, versions A–D | 40 |
| Midterm, Fall 2025 | 10 |
| Midterm, Spring 2025 | 10 |
| Final, Fall 2025 | 15 |
| Final, Spring 2025 | 15 |
| Homework 8 | 10 |

Each question provides its scenario, typeset given values, a coding task,
an optional small tip, an example, and a diagram. The equation sheet mirrors
the practice PDF's two-column order and notation; relevant rows are highlighted.
Additional reference equations are available separately.

The bowl diagram is redrawn in LaTeX/TikZ, with the source included at
`codingbat_gui/diagrams/bowl.tex`. Other diagrams are geometric SVGs generated
from the displayed quantities. Every diagram can be enlarged. Compiled graphics
are included, so using the app does not require a TeX installation.

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
KaTeX 0.16.11 and the LaTeX.css file from `gadmaj/website` are bundled locally;
their license files are in the corresponding `vendor/` directories. The code
editor keeps its existing theme while question text uses Latin Modern.
