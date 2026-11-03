"use strict";

// Small local editor conveniences. Completion reads declarations, never a dictionary
// of library functions, keywords, snippets, or solutions.
(() => {
  const identifier = /^[A-Za-z_]\w*$/;
  const reserved = new Set(("False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield match case const static volatile constexpr inline unsigned signed long short int float double bool char void auto string vector tuple std size_t").split(" "));

  function splitTopLevel(text) {
    const parts = [];
    let depth = 0, start = 0;
    for (let i = 0; i < text.length; i++) {
      if ("([{<".includes(text[i])) depth++;
      else if (")]}>".includes(text[i])) depth--;
      else if (text[i] === "," && depth === 0) { parts.push(text.slice(start, i)); start = i + 1; }
    }
    parts.push(text.slice(start));
    return parts;
  }

  function definedVariables(source, language) {
    const names = new Set();
    const add = name => { if (identifier.test(name) && !reserved.has(name)) names.add(name); };
    if (language === "python") {
      // Parameters, including multiline signatures, defaults, and annotations.
      for (const match of source.matchAll(/\bdef\s+[A-Za-z_]\w*\s*\(([^)]*)\)/g)) {
        for (const parameter of splitTopLevel(match[1])) {
          const name = parameter.trim().match(/^\*{0,2}([A-Za-z_]\w*)/);
          if (name) add(name[1]);
        }
      }
      // Plain, annotated, chained, and unpacked assignments at statement starts.
      for (const line of source.split(/\n|;/)) {
        let statement = line.trim();
        while (statement) {
          const assignment = statement.match(/^(\(?\s*\*?[A-Za-z_]\w*(?:\s*,\s*\*?[A-Za-z_]\w*)*\s*\)?)\s*(?::[^=]+)?\s*=(?!=)/);
          if (!assignment) break;
          for (const name of assignment[1].match(/[A-Za-z_]\w*/g) || []) add(name);
          statement = statement.slice(assignment[0].length).trim();
        }
      }
      for (const match of source.matchAll(/\bfor\s+(\(?\s*[A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*\s*\)?)\s+in\b/g)) {
        for (const name of match[1].match(/[A-Za-z_]\w*/g) || []) add(name);
      }
      for (const match of source.matchAll(/\bas\s+([A-Za-z_]\w*)/g)) add(match[1]);
    } else {
      // Common C++ variable and parameter declarations, including vectors/references.
      const template = "<(?:[^<>;{}()=]|<(?:[^<>;{}()=]|<[^<>;{}()=]*>)*>)*>";
      const type = "(?:(?:const|static|volatile|constexpr|unsigned|signed|long|short)\\s+)*(?:(?:std::)?(?:vector|array|tuple|pair|map|set|optional)\\s*" + template + "|(?:std::)?(?:string|size_t)|double|float|int|long|short|char|bool|auto)";
      const declaration = new RegExp("\\b" + type + "(?:\\s+|\\s*[*&]+\\s*)([A-Za-z_]\\w*)\\s*(?=[=;,):{\\[])", "g");
      for (const match of source.matchAll(declaration)) {
        add(match[1]);
        // Also recognize `double x = 0, y = 0;`, without treating RHS names as declarations.
        const tail = source.slice(match.index + match[0].length).split(/[;\n{}]/, 1)[0];
        for (const part of splitTopLevel(tail).slice(1)) {
          const next = part.trim().match(/^([A-Za-z_]\w*)\s*(?=[=,\[]|$)/);
          if (next) add(next[1]);
        }
      }
      for (const match of source.matchAll(/\bauto\s*(?:&&?|const)?\s*\[([^\]]+)\]/g)) {
        for (const name of match[1].split(",")) add(name.trim());
      }
    }
    return [...names];
  }

  window.practiceDefinedVariables = definedVariables;
  window.createPracticeEditor = (textarea, callbacks) => {
    let language = "python";
    let completionTimer;
    let activeLine;
    const cm = CodeMirror.fromTextArea(textarea, {
      mode: {name: "python", version: 3},
      theme: "practice",
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: false,
      lineNumbers: true,
      lineWrapping: false,
      matchBrackets: true,
      inputStyle: "textarea",
      screenReaderLabel: "Python code",
      spellcheck: false,
      autocorrect: false,
      autocapitalize: false,
      dragDrop: false,
      configureMouse: (_cm, _repeat, event) => event.altKey
        ? {unit: "rectangle", addNew: false, extend: false} : {},
      extraKeys: {
        "Ctrl-Enter": callbacks.run,
        "Cmd-Enter": callbacks.run,
        "Ctrl-Space": () => complete(true),
        "Tab": editor => {
          if (editor.getOption("readOnly")) return;
          if (editor.somethingSelected()) editor.indentSelection("add");
          else editor.replaceSelections(editor.listSelections().map(() => "    "), "end", "+input");
        },
        "Shift-Tab": editor => { if (!editor.getOption("readOnly")) editor.indentSelection("subtract"); },
        "Ctrl-Alt-Up": () => addCursor(-1),
        "Ctrl-Alt-Down": () => addCursor(1),
        "Esc": "singleSelection"
      }
    });
    cm.getInputField().setAttribute("aria-describedby", "editor-help editor-shortcuts");
    new ResizeObserver(() => cm.refresh()).observe(cm.getWrapperElement());

    function updatePosition() {
      const cursor = cm.getCursor();
      const count = cm.listSelections().length;
      const position = document.getElementById("editor-position");
      position.textContent = `Ln ${cursor.line + 1}, Col ${cursor.ch + 1}`
        + (count > 1 ? ` · ${count} cursors` : "");
      cm.operation(() => {
        if (activeLine != null && activeLine < cm.lineCount()) {
          cm.removeLineClass(activeLine, "background", "practice-active-line");
        }
        activeLine = cursor.line;
        cm.addLineClass(activeLine, "background", "practice-active-line");
      });
    }
    cm.on("cursorActivity", updatePosition);
    updatePosition();

    function addCursor(direction) {
      if (cm.getOption("readOnly")) return;
      cm.closeHint();
      const head = cm.getCursor();
      const line = head.line + direction;
      if (line < cm.firstLine() || line > cm.lastLine()) return;
      const next = CodeMirror.Pos(line, Math.min(head.ch, cm.getLine(line).length));
      cm.addSelection(next, next);
      cm.scrollIntoView(next);
    }

    function hints(editor, options) {
      if (editor.getOption("readOnly") || editor.somethingSelected() || editor.listSelections().length !== 1) return;
      const cursor = editor.getCursor();
      const line = editor.getLine(cursor.line);
      const token = editor.getTokenAt(cursor, true);
      if (/comment|string|meta/.test(token.type || "")) return;
      const prefix = line.slice(0, cursor.ch).match(/[A-Za-z_]\w*$/)?.[0] || "";
      if (prefix.length < (options.manual ? 0 : 2)) return;
      const start = cursor.ch - prefix.length;
      if (/(?:\.|->|::)\s*$/.test(line.slice(0, start))) return;
      let end = cursor.ch;
      while (end < line.length && /\w/.test(line[end])) end++;
      const word = line.slice(start, end);
      // Mask comments and strings using the language tokenizer, preserving layout.
      const clean = [];
      for (let n = editor.firstLine(); n <= cursor.line; n++) {
        const text = editor.getLine(n);
        const limit = n === cursor.line ? start : text.length;
        clean.push(editor.getLineTokens(n, true).map(t => {
          const value = text.slice(t.start, Math.min(t.end, limit));
          return t.start >= limit ? "" : /comment|string|meta/.test(t.type || "")
            ? value.replace(/[^\n]/g, " ") : value;
        }).join(""));
      }
      const list = definedVariables(clean.join("\n"), language)
        .filter(name => name.startsWith(prefix) && name !== word).sort().slice(0, 8);
      if (list.length) return {list, from: CodeMirror.Pos(cursor.line, start), to: CodeMirror.Pos(cursor.line, end)};
    }

    function complete(manual = false) {
      clearTimeout(completionTimer);
      if (!cm.getOption("readOnly")) cm.showHint({hint: hints, completeSingle: false, manual});
    }

    cm.on("change", (_editor, change) => {
      callbacks.change(cm.getValue());
      updatePosition();
      if (change.origin === "setValue") cm.closeHint();
    });
    cm.on("inputRead", (_editor, change) => {
      clearTimeout(completionTimer);
      if (change.origin === "+input" && !cm.state.completionActive) {
        completionTimer = setTimeout(() => complete(), 100);
      }
    });
    cm.on("blur", () => clearTimeout(completionTimer));
    // Alt-drag keeps a rectangular selection; a stationary Alt-click adds a cursor.
    cm.on("mousedown", (_editor, event) => {
      if (!event.altKey || event.button !== 0 || cm.getOption("readOnly")) return;
      cm.closeHint();
      const previous = cm.listSelections().map(r => ({anchor: r.anchor, head: r.head}));
      const point = cm.coordsChar({left: event.clientX, top: event.clientY}, "window");
      document.addEventListener("mouseup", end => {
        if (Math.abs(end.clientX - event.clientX) + Math.abs(end.clientY - event.clientY) < 4) {
          queueMicrotask(() => {
            const duplicate = previous.findIndex(r => CodeMirror.cmpPos(r.anchor, point) === 0 && CodeMirror.cmpPos(r.head, point) === 0);
            if (duplicate >= 0 && previous.length > 1) previous.splice(duplicate, 1);
            else previous.push({anchor: point, head: point});
            cm.setSelections(previous, previous.length - 1);
            cm.focus();
          });
        }
      }, {once: true});
    });

    return {
      get value() { return cm.getValue(); },
      set value(value) {
        clearTimeout(completionTimer);
        cm.closeHint();
        cm.setValue(value);
        cm.clearHistory();
        cm.scrollTo(0, 0);
      },
      get readOnly() { return !!cm.getOption("readOnly"); },
      set readOnly(value) {
        clearTimeout(completionTimer);
        cm.closeHint();
        cm.setOption("readOnly", value);
      },
      setLanguage(value) {
        if (language === value) return;
        language = value;
        cm.closeHint();
        cm.setOption("mode", value === "cpp" ? "text/x-c++src" : {name: "python", version: 3});
        cm.getInputField().setAttribute("aria-label", value === "cpp" ? "C++ code" : "Python code");
      },
      focus() { cm.focus(); },
      refresh() { cm.refresh(); }
    };
  };
})();
