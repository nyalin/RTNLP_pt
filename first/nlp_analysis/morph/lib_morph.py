# import time
from kiwipiepy import Kiwi


kiwi = Kiwi()


def convert_kiwi_token(tokens=None):
    res = []
    if tokens is None:
        return res
    for token in tokens:
        if not isinstance(token, list):
            res.append({
                'form': token.form,
                'tag': token.tag,
                'start': token.start,
                'len': token.len,
            })
        else:
            result = []
            for tok in token:
                result.append({
                    'form': tok.form,
                    'tag': tok.tag,
                    'start': tok.start,
                    'len': tok.len,
                })
            res.append(result)
    return res


def kiwi_morph_anlysis(texts=''):
    res = convert_kiwi_token(kiwi.tokenize(texts))
    return res
