def sanitize(text):
    text = text.replace("'", "\'")
    text = text.replace('"', '\"')
    return text
