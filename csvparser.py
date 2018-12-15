import csv

def parseCSV(filename):

    with open(filename, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader)
        column = {}
        for h in headers:
            column[h] = []
        for row in reader:
            for h, v in zip(headers, row):
                column[h].append(v)

    print(enumerate(column['id']))
    objects = {}
    for idx, objectID in enumerate(column['id']):
            if objectID not in objects.keys():
                objects[objectID] = []
                for key, attributeValue in column.items():
                    objects[objectID].append(attributeValue[idx])
            elif objectID in objects.keys():
                objects[objectID].append(column['s_full_link'][idx])

    maxLength = 0
    for key, value in objects.items():
        if len(value) > maxLength:
            maxLength = len(value)

    for key, value in objects.items():
        diff = maxLength - len(value)
        for i in range(diff):
            value.append('NONE')

    diff = maxLength - len(headers)
    for i in range(diff):
        headers.append("{}_{}".format("s_full_link", i+1))

    outputFileName = '-'.join(('parsed',filename))
    with open(outputFileName, mode='w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(headers)
        for objectID, attributes in objects.items():
            writer.writerow(attributes)

    return outputFileName

if __name__ == '__main__':
    parseCSV('pyout.csv')