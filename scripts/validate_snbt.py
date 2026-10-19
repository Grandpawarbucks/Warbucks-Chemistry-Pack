"""Structural FTB SNBT validator, following the snbt-validation skill's grammar and diagnostic codes.
Also lints strings for FTB formatting corruption ("&" followed by whitespace, or an unknown & code).
usage: python validate_snbt.py <file-or-dir>...   (exit 0 clean, 1 diagnostics, 2 invocation error)
"""
import pathlib
import re
import sys

NUM = re.compile(r"[-+]?(0x[0-9a-fA-F]+|(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?)[bBsSlLfFdD]?(?![A-Za-z0-9_.+-])")
IDENT = re.compile(r"[A-Za-z0-9_.+-]+")
SPECIAL = ("-∞F", "∞F", "-∞", "∞", "NaN", "NanF")
FMT_OK = set("0123456789abcdefklmnor")


class Tok:
    def __init__(self, kind, val, line, col):
        self.kind, self.val, self.line, self.col = kind, val, line, col


def lex(text, diags):
    toks, i, line, col = [], 0, 1, 1
    if text.startswith("﻿"):
        i = 1
    n = len(text)
    while i < n:
        c = text[i]
        if c == "\n":
            i += 1; line += 1; col = 1; continue
        if c in " \t\r":
            i += 1; col += 1; continue
        if c == "#":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c in "{}[]:,;":
            toks.append(Tok(c, c, line, col)); i += 1; col += 1; continue
        if c in "\"'":
            q, j, buf, sl, sc = c, i + 1, [], line, col
            while j < n and text[j] != q:
                if text[j] == "\\" and j + 1 < n:
                    buf.append(text[j:j + 2]); j += 2; continue
                if text[j] == "\n":
                    break
                buf.append(text[j]); j += 1
            if j >= n or text[j] != q:
                diags.append((sl, sc, "unterminated_string", "closing quote never found"))
                return toks
            toks.append(Tok("str", "".join(buf), sl, sc))
            col += j + 1 - i; i = j + 1; continue
        for sp in SPECIAL:
            if text.startswith(sp, i):
                toks.append(Tok("num", sp, line, col)); i += len(sp); col += len(sp); break
        else:
            m = NUM.match(text, i)
            if m:
                toks.append(Tok("num", m.group(), line, col)); col += m.end() - i; i = m.end(); continue
            m = IDENT.match(text, i)
            if m:
                toks.append(Tok("ident", m.group(), line, col)); col += m.end() - i; i = m.end(); continue
            diags.append((line, col, "lex_error", f"invalid character {c!r}"))
            return toks
    return toks


class Parser:
    def __init__(self, toks, diags):
        self.t, self.p, self.d, self.strings = toks, 0, diags, []

    def peek(self):
        return self.t[self.p] if self.p < len(self.t) else None

    def err(self, tok, code, msg):
        tok = tok or (self.t[-1] if self.t else Tok("", "", 1, 1))
        self.d.append((tok.line, tok.col, code, msg))
        raise StopIteration

    def value(self):
        tok = self.peek()
        if tok is None:
            self.err(None, "missing_value", "value expected before end of file")
        if tok.kind == "{":
            return self.obj()
        if tok.kind == "[":
            return self.arr()
        self.p += 1
        if tok.kind == "str":
            self.strings.append(tok)
            return
        if tok.kind == "num" or (tok.kind == "ident" and tok.val in ("true", "false")):
            return
        if tok.kind in "}],":
            self.p -= 1
            self.err(tok, "missing_value", f"value expected, found {tok.val!r}")
        self.err(tok, "invalid_value", f"bare identifier {tok.val!r} used as a value")

    def seq(self, close, item):
        open_tok = self.t[self.p]; self.p += 1
        prev = None
        while True:
            tok = self.peek()
            if tok is None:
                self.err(open_tok, "unterminated_object" if close == "}" else "unterminated_array", f"{close!r} expected before EOF")
            if tok.kind == close:
                self.p += 1; return
            if prev is not None:
                if tok.kind == ",":
                    self.p += 1
                    nxt = self.peek()
                    if nxt is not None and nxt.kind == close:
                        self.err(tok, "trailing_comma", "stray ',' before close")
                elif tok.line == prev.line:
                    self.err(tok, "missing_comma", f"same-line values need ',' (previous item at {prev.line}:{prev.col})")
            start = self.peek()
            item()
            prev = self.t[self.p - 1]
            _ = start

    def obj(self):
        keys = {}

        def item():
            k = self.peek()
            if k is None or k.kind not in ("str", "ident", "num"):
                self.err(k, "invalid_key", f"key expected, found {getattr(k, 'val', 'EOF')!r}")
            self.p += 1
            if k.val in keys:
                self.d.append((k.line, k.col, "duplicate_key", f"{k.val!r} already at line {keys[k.val]}"))
            keys[k.val] = k.line
            c = self.peek()
            if c is None or c.kind != ":":
                self.err(c or k, "expected_token", f"':' expected after key {k.val!r}")
            self.p += 1
            self.value()
        self.seq("}", item)

    def arr(self):
        if self.p + 2 < len(self.t) and self.t[self.p + 1].kind == "ident" and self.t[self.p + 1].val in "BIL" \
                and self.t[self.p + 2].kind == ";":
            self.p += 2
            self.t[self.p] = Tok("[", "[", self.t[self.p].line, self.t[self.p].col)  # ';' acts as the opener
        self.seq("]", self.value)


def fmt_issues(s):
    out = []
    for m in re.finditer(r"&(.?)", s.replace("\\&", "")):
        ch = m.group(1)
        if ch == "" or ch.isspace():
            out.append("'&' followed by whitespace/end (escape as \\&)")
        elif ch.lower() not in FMT_OK and ch != "#":
            out.append(f"unknown formatting code &{ch}")
    return out


def validate(path):
    diags = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [(1, 1, "encoding_error", "not valid UTF-8")]
    if not text.strip():
        return [(1, 1, "empty_file", "file is empty")]
    toks = lex(text, diags)
    if diags:
        return diags
    p = Parser(toks, diags)
    try:
        p.value()
        if p.peek() is not None:
            p.err(p.peek(), "trailing_tokens", "extra tokens after the top-level structure")
    except StopIteration:
        pass
    for s in p.strings:
        for msg in fmt_issues(s.val):
            diags.append((s.line, s.col, "format_code", msg + f": {s.val[:70]!r}"))
    return diags


def main():
    targets = sys.argv[1:]
    if not targets:
        print(__doc__); sys.exit(2)
    files = []
    for t in targets:
        p = pathlib.Path(t)
        if not p.exists():
            print(f"{t}: io_error: no such path"); sys.exit(2)
        files += sorted(p.rglob("*.snbt")) if p.is_dir() else [p]
    bad = 0
    for f in files:
        for line, col, code, msg in validate(f):
            bad += 1
            print(f"{f}:{line}:{col}: {code}: {msg}")
    print(f"{len(files)} files, {bad} diagnostics")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
