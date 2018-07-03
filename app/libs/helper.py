"""
this is a tools set for view function
"""


def is_isbn_or_key(word):
    if len(word) == 13 and word.isdigit():
        return 'isbn'
    word_after_replace = word.replace('-', '')
    if '-' in word and len(word_after_replace) == 10 and word_after_replace.isdigit():
        return 'isbn'
    return 'key'
