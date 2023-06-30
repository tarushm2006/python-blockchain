def parse():
    fileName = input("Enter the file name")
    file = open(fileName, "r")
    lines = file.readlines()
    parsedData = ""
    for line in lines:
        parsedData = parsedData+line

    return parsedData
