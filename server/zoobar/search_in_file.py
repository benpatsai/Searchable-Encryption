
def search_in_file(path, keyword):
    linestring = open(path, 'r').read()
    linestring = linestring.replace('\n',' ')
    words = linestring.split(' ')
    if keyword in words:
        return True
    else: 
        return False

