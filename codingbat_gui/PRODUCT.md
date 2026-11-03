# Physics practice

<!-- impeccable:product-schema 1 -->

## Platform
web

## Users and purpose
One student reviewing PH-UY 1013 HW8 and the Spring 2026 and Fall 2025 midterms.
Practice all ten problems in each set as small Python or C++ functions, with
immediate output and tests.

## Operating context
Local KDE Plasma computer, Firefox, installed Python. The existing
`../physics_leetcode.py` and `../physics_leetcode_cases.json` are the exercise
source for HW8. `midterms.py` contains the twenty midterm tasks, original exam
values, and additional practice cases. The PDFs remain available as reference
material, and original midterm diagrams appear beside their exercises.

## Capabilities and constraints
A basic CodingBat-like GUI: choose a problem, read its instructions, edit a
standalone function, run it, and read output or errors in the selected language.
Both editors have syntax highlighting. C++ uses C++20 and supplies the test
driver automatically; students do not write main(). No build or compiler
controls. The locally bundled CodeMirror 5 editor provides Alt-drag column
selection, Alt-click and keyboard multicursors, selected-line indenting,
autoindent, matching brackets, line numbers, an active-line highlight, a cursor
position indicator, and undo/redo. Completion suggests only parameters
and variables declared earlier in the current document; comments and strings are
excluded. No library completions, snippets, or generated solutions. Preserve
separate work and progress per problem and language. Keep test
feedback plain and include original exam/homework values. A set selector keeps
all three collections available; saved code and progress are separate per set
and language, preserving the original HW8 storage keys. GitHub alternatives were
researched separately at the user's request.

## Open implementation assumptions
The optional platform/error questions were sent during implementation. Pending
an answer, use a local Firefox page and ordinary Python exception messages.

## Brand commitments
The user explicitly requested a very basic interface like CodingBat. Plain,
compact controls and readable code take precedence over decorative design.
