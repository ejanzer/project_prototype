
with open('cedict.txt') as f:
    data = f.readlines()

a = open('cedict3.csv', 'w') 


for row in data:

    if row[0] == '#':
        continue

    quoted = []
    copy = []
    last_index = len(row) - 1

    for i in xrange(len(row)):

        last = None
        if i != 0:
            last = row[i-1]

        next = None
        if i != last_index:
            next = row[i+1]

        if row[i] == ' ' and quoted == []:
            copy += ','
        elif row[i] == '[' or row[i] == '(':
            if quoted == []:
                copy.append('"')
            else: 
                copy.append(row[i])

            quoted.append(row[i])

        elif row[i] == ']':
            if quoted[-1] == '[':
                quoted.pop()
                if quoted == []:
                    copy.append('"')
                else:
                    copy.append(row[i])
        elif row[i] == ')':
            if quoted[-1] == '(':
                quoted.pop()
                if quoted != []:
                    copy.append(row[i])
                else: 
                    copy.append('"')
        elif row[i] == '/' and last == ' ':
            if quoted == []:
                quoted.append('/')
                copy.append('"')
        elif row[i] == '/' and (next == ' ' or next == '\r' or next == '\n'):
            if quoted != []:
                if quoted[-1] == '/':
                    quoted.pop()
            copy.append('"')
        else:
            copy += row[i]

    copy = ''.join(copy)
    a.write(copy)

a.close()