"use strict";

// A local lexical highlighter. Editing stays in the ordinary accessible textarea.
(() => {
  const words = text => new Set(text.split(/\s+/));
  const python = words("False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield match case type");
  const cpp = words("alignas alignof asm auto bool break case catch char char8_t char16_t char32_t class concept const consteval constexpr constinit const_cast continue co_await co_return co_yield decltype default delete do double dynamic_cast else enum explicit export extern false float for friend goto if inline int long mutable namespace new noexcept nullptr operator private protected public register reinterpret_cast requires return short signed sizeof static static_assert static_cast struct switch template this thread_local throw true try typedef typeid typename union unsigned using virtual void volatile wchar_t while");
  const builtins = words("abs all any bin bool bytearray bytes callable chr classmethod complex dict divmod enumerate filter float format frozenset getattr hasattr hash hex id input int isinstance issubclass iter len list map max min next object oct open ord pow print property range repr reversed round set setattr slice sorted staticmethod str sum super tuple type vars zip math std string vector tuple cout cin cerr endl size_t");
  const escape = text => text.replace(/[&<>"']/g, c => ({"&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"}[c]));

  window.highlightCode = (source, language = "python") => {
    const tokens = [];
    const keywords = language === "cpp" ? cpp : python;
    let i = 0;
    let definition = false;
    const emit = (text, kind) => tokens.push(kind ? `<span class="syntax-${kind}">${escape(text)}</span>` : escape(text));
    while (i < source.length) {
      const rest = source.slice(i);
      let end, match;
      if ((language === "python" && rest[0] === "#") || (language === "cpp" && rest.startsWith("//"))) {
        end = source.indexOf("\n", i);
        if (end < 0) end = source.length;
        emit(source.slice(i, end), "comment"); i = end; continue;
      }
      if (language === "cpp" && rest.startsWith("/*")) {
        end = source.indexOf("*/", i + 2);
        end = end < 0 ? source.length : end + 2;
        emit(source.slice(i, end), "comment"); i = end; continue;
      }
      if (language === "cpp" && rest[0] === "#" && !source.slice(source.lastIndexOf("\n", i - 1) + 1, i).trim()) {
        end = source.indexOf("\n", i);
        if (end < 0) end = source.length;
        emit(source.slice(i, end), "directive"); i = end; continue;
      }
      if (language === "cpp" && (match = rest.match(/^(?:u8|u|U|L)?R"([^ ()\\\t\r\n]{0,16})\(/))) {
        const close = ")" + match[1] + '"';
        end = source.indexOf(close, i + match[0].length);
        end = end < 0 ? source.length : end + close.length;
        emit(source.slice(i, end), "string"); i = end; continue;
      }
      match = rest.match(language === "cpp" ? /^(?:u8|u|U|L)?(['"])/ : /^(?:[rRuUbBfF]{0,2})?("""|'''|"|')/);
      if (match) {
        const quote = match[1];
        end = i + match[0].length;
        while (end < source.length) {
          if (source[end] === "\\") { end += 2; continue; }
          if (source.startsWith(quote, end)) { end += quote.length; break; }
          end++;
        }
        end = Math.min(end, source.length);
        emit(source.slice(i, end), "string"); i = end; continue;
      }
      if ((match = rest.match(/^(?:0[xX][\da-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+|(?:\d[\d_]*(?:\.[\d_]*)?|\.\d[\d_]*)(?:[eE][+-]?[\d_]+)?)[jJuUlLfF]*/))) {
        emit(match[0], "number"); i += match[0].length; continue;
      }
      if ((match = rest.match(/^[A-Za-z_]\w*/))) {
        const word = match[0];
        const kind = keywords.has(word) ? "keyword" : definition ? "function"
          : builtins.has(word) ? "builtin" : /^\s*\(/.test(rest.slice(word.length)) ? "function" : null;
        emit(word, kind);
        definition = language === "python" && (word === "def" || word === "class");
        i += word.length; continue;
      }
      emit(source[i]); i++;
    }
    return tokens.join("");
  };
})();
