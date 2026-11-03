# Physics practice

<!-- impeccable:product-schema 1 -->

## Platform
Local web application: Python standard-library server and vanilla JavaScript.

## Users and purpose
A PH-UY 1013 mechanics student preparing for midterms and finals by solving
physics questions as small Python or C++ functions, with immediate test feedback.
Quick startup and useful practice controls take precedence over theming.

## Operating context
Run locally on the student's KDE Plasma computer and use Firefox. The app ships
copied question data, vector diagrams, LaTeX.css, KaTeX, CodeMirror, and fonts;
normal use requires no internet or runtime TeX installation. Original source PDFs
may remain local as optional, ignored reference files. Their absence must not
prevent practice. The TikZ source `diagrams/bowl.tex` and compiled `bowl.svg` ship
together; compilation is an asset-authoring step, not a startup requirement.

## Content and study choices
The bank contains 100 source questions and 598 numerical test cases: six midterms
(Spring 2026 A–D, Fall 2025, Spring 2025), two finals (Spring and Fall 2025), and
Homework 8. The six startup choices are random questions, randomized midterm,
original midterm by semester/year, randomized final exam, original final exam by
semester/year, and a selected unit. Homework 8 has a separate entry link.

Randomized midterm/final sessions can match the selected paper's counts by unit
or use a custom question count. Randomized modes offer optional new-number
versions and prefer different question families. Original papers preserve their
original numerical values. Unit practice and the skill chart provide focused
review; the chart counts actually solved question families per unit rather than
invented proficiency scores. Sessions can be resumed in the same browser.

## Core practice behavior
Choose a question, read the scenario and givens, inspect its diagram, write the
standalone function, run it, and read output, errors, and individual test results.
C++ uses C++20 with a supplied test driver; students do not write `main()` or
manage build settings. Tips, equation sheet, and example results are optional
disclosures. Diagrams can be enlarged. The bowl illustration separates the
physical setup from its labeled force inset.

The equation sheet preserves the two-column order and notation of page 3 of
`1013X1aS26.pdf`. Formula IDs mark the entries useful for the current task;
additional reference equations are nested separately.

CodeMirror retains its existing monospace theme, syntax highlighting, line
numbers, active line, matching brackets, undo/redo, autoindent, selected-line
indenting, Alt-drag column selection, Alt-click and keyboard multicursors, and
cursor position indicator. Completion uses parameters and earlier declared
variables, excluding comments and strings; it supplies no generated solutions.

## Persistence and implementation boundaries
Save separate drafts and solved status for every original question and language,
using the original per-set storage prefixes, including Homework 8. Randomized
appearances of one source question share that question's language-specific draft.
Session selection and position are stored in the browser. `practice.js` renders
the study flow; `study.py` assembles sessions; `question_bank.py` and
`curriculum.py` hold question and curriculum data.

## Brand commitments
Preserve the basic CodingBat-like workflow and existing green/white control
palette and editor theme. The user chose an academic worksheet tone, with the
exact LaTeX.css from gadmaj/website and Latin Modern question prose. Keep controls
plain, readable, and compact; make mathematical material and code easy to use.
