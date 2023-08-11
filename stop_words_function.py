def contains_profanity(text):
    if 'http' in text:
        return True
    elif 'https' in text:
        return True
    elif 'www' in text:
        return True
    elif 'ru' in text:
        return True
    elif 'com' in text:
        return True
    elif 't.me' in text:
        return True
    elif 'bot' in text:
        return True
    elif 'инвестиции' in text:
        return True
    elif 'p2p' in text:
        return True
    elif 'ставки' in text:
        return True
    elif 'крипта' in text:
        return True
    else:
        return False