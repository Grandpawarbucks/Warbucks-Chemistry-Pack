"""Tiny helpers to rewrite Q(...) headers / descs in a chapter file by key."""
import re, sys
class F:
    def __init__(s, p):
        s.p = p; s.t = open(p, encoding='utf-8').read()
    def span(s, key):
        i = s.t.index(f'Q("{key}",')
        # find end of this Q(...) call: match parens
        d = 0; j = i
        while True:
            c = s.t[j]
            if c == '(':
                d += 1
            elif c == ')':
                d -= 1
                if d == 0:
                    break
            elif c == '"':
                k = j + 1
                while s.t[k] != '"':
                    k += 2 if s.t[k] == chr(92) else 1
                j = k
            j += 1
        return i, j + 1
    def get(s, key):
        a, b = s.span(key); return s.t[a:b]
    def header(s, key, new):
        """Replace everything from Q("key", up to and including 'desc=[' with new (must end with 'desc=[')."""
        a, b = s.span(key)
        q = s.t[a:b]
        k = q.index('desc=[') + len('desc=[')
        s.t = s.t[:a] + new + q[k:] + s.t[b:]
    def sub(s, key, old, new):
        a, b = s.span(key); q = s.t[a:b]
        assert q.count(old) == 1, (key, old, q.count(old))
        s.t = s.t[:a] + q.replace(old, new) + s.t[b:]
    def after(s, key, text):
        a, b = s.span(key)
        # insert after the trailing comma
        assert s.t[b] == ','
        s.t = s.t[:b + 1] + '\n' + text.rstrip('\n') + s.t[b + 1:]
    def save(s):
        open(s.p, 'w', encoding='utf-8', newline='\n').write(s.t)
