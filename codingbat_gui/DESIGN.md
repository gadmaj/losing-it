---
name: Physics practice
description: An academic mechanics worksheet with a familiar coding workbench.
colors:
  paper: "#fff"
  ink: "#222a24"
  muted: "#536057"
  rule: "#d0d8d1"
  soft: "#f3f6f3"
  accent: "#245d34"
  accent-hover: "#194a27"
  accent-ink: "#fff"
  selection: "#d9ecdd"
  error: "#9c2424"
  error-paper: "#fff4f2"
  keyword: "#7138a1"
  string: "#23633d"
  number: "#1b58a0"
  comment: "#68716b"
  function: "#174d82"
  directive: "#87520a"
typography:
  headline:
    fontFamily: "Latin Modern Roman, Georgia, serif"
    fontSize: "clamp(26px, 3vw, 35px)"
    fontWeight: 700
    lineHeight: 1.2
  question:
    fontFamily: "Latin Modern Roman, Georgia, serif"
    fontSize: "18px"
    lineHeight: 1.6
  body:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "15px"
    lineHeight: 1.5
  code:
    fontFamily: "DejaVu Sans Mono, Liberation Mono, monospace"
    fontSize: "14px"
    lineHeight: 1.65
rounded:
  sm: "3px"
  editor: "2px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  2xl: "48px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.accent-ink}"
    rounded: "{rounded.sm}"
    padding: "10px 22px"
  button-secondary:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.accent}"
    rounded: "{rounded.sm}"
    padding: "8px 16px"
  field:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "8px 10px"
---

# Design System: Physics practice

## Overview

**Creative North Star: "Academic worksheet"**

Physics practice uses an academic worksheet as its visual authority: readable mathematical prose, precise diagrams, and a familiar code editor. Preserve the established green and white controls and the original CodeMirror theme. The exact bundled LaTeX.css from gadmaj/website supplies the typesetting foundation; application CSS adapts it to the workbench.

Information stays in a flat document flow with thin rules, optional disclosures, and explicit actions. Latin Modern gives questions their academic character, while Arial keeps controls compact and monospace preserves code structure.

**Key Characteristics:**

- Latin Modern worksheet prose and mathematical notation.
- Plain green actions and thin neutral rules.
- Original CodeMirror syntax colors and interaction model.
- Responsive document flow with enlargable vector diagrams.

## Colors

The existing green action palette sits on white paper with subdued gray-green
rules and supporting text. `tokens.css` is the implementation source of truth;
`style.css` imports it and retains compatibility aliases.

Primary accent colors belong to actions, links, solved indicators, focus rings,
and task-relevant formula borders. Selection green marks the active problem and
editor selections. Paper, ink, muted, rule, and soft provide the document layers.
Error ink and pale error paper distinguish execution failures. Keyword, string,
number, comment, function, and directive colors preserve the editor syntax theme.

**The Palette Continuity Rule.** Preserve the established green/white controls and original editor syntax colors.

## Typography

Latin Modern Roman, with Georgia and serif fallbacks, carries the masthead,
worksheet headings, and question prose. Arial, Helvetica, sans-serif carries
controls, metadata, coding instructions, and output labels. DejaVu Sans Mono,
Liberation Mono, monospace carries code and literal identifiers. KaTeX handles
mathematical notation using bundled assets.

Home headings use the headline token; question headings use a responsive size
(`clamp(25px, 2.7vw, 33px)`) and a maximum measure of 34ch. Question prose uses the
question token and a maximum measure of 70ch; below 42rem it becomes 17px.
Supporting UI generally uses 12–14px. Code uses the code token and becomes 13px
at the navigation breakpoint. Preserve indentation and disable code ligatures.

**The Type Boundary Rule.** Keep typeset question prose separate from the existing monospace editor and sans-serif controls.

## Layout

The masthead, session toolbar, and study workbench have a centered maximum width
of 1240px. The startup form is a narrower document (780px maximum including
padding), with ruled study choices in two columns from 42rem upward and one
column below. Desktop page padding is generally 28px; narrow padding is 18px.
The implemented spacing tokens run from 4px through 48px.

The session workbench uses a 192px problem rail beside a flexible main column.
At 700px and below, the rail becomes a select menu and the workbench stacks.
At 68rem and above, question prose/givens and diagram sit alongside each other
in a 1.05:1 grid with a 30px gap; below that they stack. Givens retain two columns.
Below 42rem, the course label hides, the session title wraps to its own row,
start controls stack, and the primary startup action spans the available width.
Skill rows move their bar below the label while the numerical count stays right.

The equation sheet deliberately retains two columns on narrow screens. Below
42rem its padding, gap, and formula size shrink; individual formulas can scroll.
The editor scrolls horizontally without wrapping code. Test-result tables and
large diagrams also scroll within their own regions. The diagram dialog is
limited to 95vw / 90dvh, with a 900px-wide illustration in a scrollable viewport.

## Elevation & Depth

The interface is flat: white paper, pale supporting surfaces, and thin rules
provide structure. Editor completion has no shadow. The enlarged diagram uses a
native dialog with a subdued ink backdrop at 0.3 opacity. No ornamental motion
is required; state changes are immediate.

## Shapes

Controls use modest corners (the sm token), while the editor uses the editor
radius. Most worksheet sections are open areas separated by one-pixel rules.
The skill chart uses a thin rectangular track rather than a rounded badge.

## Components

- Primary green buttons start a session; Run retains its compact bold treatment.
- Secondary outlined buttons navigate between questions; underlined text actions change study, open references, reset code, and enlarge diagrams.
- Study options are labeled radio rows with a top rule and pale selected/hover surface, not floating cards. Number fields and selects use plain borders and a 40px minimum control height.
- The problem rail uses pale selection green and bold text for the current question; solved indicators stay textual. It becomes a native select on narrow screens.
- Optional tips, equation sheet, examples, and shortcuts use native disclosures. The equation sheet reproduces page 3 of `1013X1aS26.pdf`; task-specific formulas receive a green outline and pale fill. Additional equations are a separate nested disclosure.
- CodeMirror preserves its line-number gutter, active line, syntax colors, matching brackets, multicursors, indentation, and completion. Default height is 245px, minimum 170px, with vertical resizing.
- The skill chart shows solved-family counts and green progress bars. Its rows are actionable shortcuts into unit practice.
- Diagram captions offer Enlarge. The bowl's main setup and separately labeled force inset are compiled TikZ/SVG; all vector assets remain sharp when enlarged.
- Output uses plain status text, console blocks, and bordered test tables. Errors use the dedicated error colors; successful results use the action green.

Visible keyboard focus uses a two-pixel green outline with a three-pixel offset;
selected study rows use an inset outline. Preserve semantic buttons, labels,
radio groups, disclosures, and dialog behavior. Disabled actions reduce opacity.

## Do's and Don'ts

### Do:

- Use Latin Modern for question prose and Arial for controls.
- Preserve the green/white palette and the existing CodeMirror theme.
- Keep the exam equation sheet in its source two-column order and highlight only task-specific formula IDs.
- Allow local scrolling for code, long formulas, test tables, and enlarged diagrams.

### Don't:

- Don't replace the worksheet with decorative cards or marketing sections.
- Don't apply the serif question font to the editor or controls.
- Don't recolor the editor as part of typesetting changes.
- Don't require runtime TeX or network assets for normal use.
