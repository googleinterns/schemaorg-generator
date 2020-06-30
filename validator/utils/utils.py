def strip_shacl_prefix(url):
    term = str(url)
    return term[27:]

def strip_url(url):
    term = str(url)
    return term.split("/")[-1]

class ResultRow():
    
    def __init__(self, id, message, property_path, value, severity):
        self.id = id
        self.message = message
        self.property_path = property_path
        self.value = value
        self.severity = severity