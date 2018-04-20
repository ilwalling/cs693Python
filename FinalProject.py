import ast
import re
#SampleIncludingAll1.py

class reader(ast.NodeVisitor):
    def __init__(self):
        self.getAttr = ""

    def visit_Attribute(self,node):
        self.getAttr = node.attr


class finalProject:

    def __init__(self):
        self.a = 2

    def parse_input(self):
        self.userFile = input("File would you like to use?")
        self.file = open(self.userFile, "r")
        self.line = next(self.file)

    def loc(self):
        print("1 = Yes \n0 = No")
        commentsFlag = input("Include Comments? (1/0) ")
        emptyLineFlag = input("Include Empty Lines? (1/0) ")
        importFlag = input("Include Imports? (1/0) ")
        numEmptyLines = 0
        numLines = 0
        numCommentLines = 0
        numImportLines = 0
        inComment = 0

        while self.line:
            numLines += 1
            stringLine = str(self.line)
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

                if inComment == 1 and self.line != '\n':
                    numCommentLines += 1

            if emptyLineFlag == "0":
                if self.line in ['\n']:
                    numEmptyLines += 1

            if importFlag == "0":
                if stringLine.startswith("import") and inComment == 0:
                    numImportLines += 1

            self.line = next(self.file, None)
        print("LOC \n----------")
        print(numLines-numImportLines-numEmptyLines-numCommentLines)

    def lcom4(self):
        tree = ast.parse(open(self.userFile).read())
        masterList = []
        #makes a list of all function definitions for specified for each class
        for element in ast.walk(tree):
            if isinstance(element,ast.ClassDef):
                classDefinitions = []
                #classDefinitions.append(element.name)
                for classNodes in element.body:
                    if isinstance(classNodes,ast.FunctionDef):
                        functionDefinitions = []
                        if classNodes.name != '__init__':
                            if functionDefinitions != '':
                                functionDefinitions.append(classNodes.name)
                                for node in classNodes.body:
                                    visitAttr = reader()
                                    visitAttr.visit(node)
                                    if visitAttr.getAttr != '':
                                        functionDefinitions.append(visitAttr.getAttr)
                                classDefinitions.append(functionDefinitions)
                masterList.append(classDefinitions)

        #combine lists if letters overlap
        print(masterList)
        for i in range(len(masterList)):
            print ("BREAK")
            changed = False
            j = masterList[i]
            while changed != True:
                changed = False
                for n in range(len(j)-1):
                    k = j[n]
                    k1 = j[n+1]
                    for l in range(len(k)):
                            if k[l] in k1:
                                k[n] = k + k1
                                changed = True
                    print(k)
                

    def cbo(self):
        tree = ast.parse(open(self.userFile).read())
        masterList = []
        # makes a list of all function definitions for specified for each class
        for element in ast.walk(tree):
            if isinstance(element, ast.ClassDef):
                classDefinitions = []
                #classDefinitions.append(element.name)
                for classNodes in element.body:
                    if isinstance(classNodes, ast.FunctionDef):
                        functionDefinitions = []
                        if classNodes.name != '__init__':
                            if functionDefinitions != '':
                                functionDefinitions.append(classNodes.name)
                                for node in classNodes.body:
                                    visitAttr = reader()
                                    visitAttr.visit(node)
                                    if visitAttr.getAttr != '':
                                        functionDefinitions.append(visitAttr.getAttr)
                                classDefinitions.append(functionDefinitions)
                masterList.append(classDefinitions)

        # combine lists if letters overlap
        print(masterList)
        for i in range(len(masterList)):
            print ("BREAK")
            changed = False
            j = masterList[i]

    def dit(self):
        print("DIT \n----------")
        classNames = []
        classChildren = []
        while self.line:
            stringLine = self.line.strip()
            if stringLine.startswith('class'):
                matchedClass = re.search('\ [a-zA-Z0-9]+', self.line)
                classNames.append(matchedClass.group(0).strip())
                index = 0
                for x in self.line:
                    if x == '(':
                        startSubstring = index + 1
                    if x == ')':
                        endSubstring = index
                        allChildren = self.line[startSubstring:endSubstring]
                        allChildren = allChildren.split(',')
                        for each in allChildren:
                            classChildren.append(each)
                    index += 1
            self.line = next(self.file, None)

#THIS IS NOT DONE

    def noc(self):
        print("NOC \n----------")
        classNames = []
        classChildren = []
        while self.line:
            stringLine = self.line.strip()
            if stringLine.startswith('class'):
                matchedClass = re.search('\ [a-zA-Z0-9]+', self.line)
                classNames.append(matchedClass.group(0).strip())
                index = 0
                for x in self.line:
                    if x == '(':
                        startSubstring = index+1
                    if x == ')':
                        endSubstring = index
                        allChildren = self.line[startSubstring:endSubstring]
                        allChildren = allChildren.split(',')
                        for each in allChildren:
                            classChildren.append(each)
                    index += 1

            self.line = next(self.file, None)
        for aClass in classNames:
            childCounter = 0
            for aChild in classChildren:
                if aClass == aChild:
                    childCounter += 1
            print(aClass)
            print(childCounter)

    def wmc(self):
        constructorFlag = input("Include the Constructor? (1/0) ")
        numOfDefs = 0
        print("WMC \n----------")
        while self.line:
            stringLine = self.line.strip()
            if stringLine.startswith('class'):
                print(numOfDefs, '\n')
                matches = re.search('\ [a-zA-Z0-9]+', self.line)
                print(matches.group(0).strip())
                numOfDefs = 0

            if stringLine.startswith('def'):
                if stringLine.find('__init__') != -1 and constructorFlag == "0":
                    numOfDefs += 0
                else:
                    numOfDefs += 1
            self.line = next(self.file, None)
        print(numOfDefs)


f = finalProject()
f.parse_input()
#f.loc()
#f.lcom4()
f.cbo()
#f.dit()
#f.noc()
#f.wmc()

