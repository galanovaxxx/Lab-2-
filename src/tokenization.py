def tokenization_function(s: str) -> list:
    s = s.split()
    k = 0
    while k < len(s):
        if s[k][0] == '"':
            while s[k][-1] != '"':
                s[k] = ' '.join([s[k], s[k + 1]])
                s.pop(k + 1)
        if s[k][0] == '"' and s[k][-1] == '"':
            s[k] = s[k][1:-1]
        k += 1
    return s
