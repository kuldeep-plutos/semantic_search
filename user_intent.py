def classify(text):
    text = text.lower()
    if 'poll' in text or 'vote' in text:
        return 'poll'
    elif 'offer' in text or 'voucher' in text or 'deal' in text:
        return 'offer'
    else:
        return 'other'

def poll_category(text):
    text = text.lower()
    if 'entert' in text:
        return 'entertainment'
    if 'sport' in text:
        return 'sports'
    if 'lifest' in text:
        return 'lifestyle'
    else:
        return 'entertainment'