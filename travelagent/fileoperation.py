def updateStringInThisFile(filename, stringToSearchFor, replacingSting):
    with open(filename, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in lines:
            if stringToSearchFor in line:
                repString = replacingSting
                line = line.replace(stringToSearchFor, repString)
            f.write(line)







