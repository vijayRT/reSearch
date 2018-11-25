from bisect import bisect_left

def word_exists(wordlist, word_fragment):
    try:
        return wordlist[bisect_left(wordlist, word_fragment)].startswith(word_fragment)
    except IndexError:
        return False 

