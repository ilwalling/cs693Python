import ast
import re
#SampleIncludingAll1.py

class finalProject:

    def __init__(self):
        self.a = 2

    def parse_input(self):
        userFile = input("File would you like to use?")
        global file
        global line
        file = open(userFile, "r")
        line = next(file)

    def loc(self):
        print("1 = Yes \n0 = No")
        commentsFlag = input("Include Comments? (1/0) ")
        emptyLineFlag = input("Include Empty Lines? (1/0) ")
        importFlag = input("Include Imports? (1/0) ")
        numEmptyLines = 0
        numLines = 0
        numCommentLines = 0
        numImportLines = 0
        global line
        inComment = 0

        while line:
            numLines += 1
            stringLine = str(line)
            stringLine = stringLine.strip()

            if commentsFlag == "0":

                if stringLine.startswith("#"):
                    numCommentLines += 1

                if stringLine.startswith('"""') and stringLine.endswith('"""') and stringLine != '""""':
                    numCommentLines += 1

                if stringLine == '"""':
                    if inComment == 0:
                        inComment = 1
                    else:
                        inComment = 0

                if inComment == 1 and line != '\n':
                    numCommentLines += 1

            if emptyLineFlag == "0":
                if line in ['\n']:
                    numEmptyLines += 1

            if importFlag == "0":
                if stringLine.startswith("import") and inComment == 0:
                    numImportLines += 1

            line = next(file, None)
        #print(numLines)
        #print(numEmptyLines)
        #print(numCommentLines)
        #print(numImportLines)
        print("LOC \n----------")
        print(numLines-numImportLines-numEmptyLines-numCommentLines)

    def lcom4(self):
        global file
        tree = ast.parse(file)

    def noc(self):
        global line
        print("NOC \n----------")
        classNames = []
        classChildren = []
        while line:
            stringLine = line.strip()
            if stringLine.startswith('class'):
                matchedClass = re.search('\ [a-zA-Z0-9]+', line)
                classNames.append(matchedClass.group(0).strip())
                index = 0
                for x in line:
                    if x == '(':
                        startSubstring = index+1
                    if x == ')':
                        endSubstring = index
                        allChildren = line[startSubstring:endSubstring]
                        allChildren = allChildren.split(',')
                        for each in allChildren:
                            classChildren.append(each)
                    index += 1

            line = next(file, None)
        for aClass in classNames:
            childCounter = 0
            for aChild in classChildren:
                if aClass == aChild:
                    childCounter += 1
            print(aClass)
            print(childCounter)

    def wmc(self):
        global line
        constructorFlag = input("Include the Constructor? (1/0) ")
        numOfDefs = 0
        print("WMC \n----------")
        while line:
            stringLine = line.strip()
            if stringLine.startswith('class'):
                print(numOfDefs, '\n')
                matches = re.search('\ [a-zA-Z0-9]+', line)
                print(matches.group(0).strip())
                numOfDefs = 0

            if stringLine.startswith('def'):
                if stringLine.find('__init__') != -1 and constructorFlag == "0":
                    numOfDefs += 0
                else:
                    numOfDefs += 1
            line = next(file, None)
        print(numOfDefs)


f = finalProject()
f.parse_input()
#f.loc()
#f.lcom4()
f.noc()
#f.wmc()

