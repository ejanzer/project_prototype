import model
from sys import argv
import codecs

def look_up_dishes(source, dest1, dest2):
    with open(source, 'r') as f:
        data = f.readlines()

    for line in data:
        chars = line.strip('\n')
        chars = chars.decode('utf-8')
        entry = model.session.query(model.Entry).filter_by(simplified=chars).first()
        if entry:
            print chars, entry.definition
            write_out(dest1, chars, definition=entry.definition)
        else:
            c = model.find_combinations(chars)
            result = model.search(c)
            if result:
                print result
                defs = []
                for char in result:
                    defs.append(char.definition)
                definition = ''.join(defs)
                write_out(dest1, chars, definition=definition)
            else:
                write_out(dest2, chars)

def write_out(dest, chars, definition=None):
    with codecs.open(dest, 'a', encoding='utf-8') as dest:
        if definition:
            s = "%s | %s\n" % (chars, definition)
        else:
            s = "%s\n" % chars
        dest.write(s)

if __name__ == "__main__":
    script, source, dest1, dest2 = argv
    look_up_dishes(source, dest1, dest2)