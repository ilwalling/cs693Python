import ast
import re
from collections import deque
#SampleIncludingAll1.py

class reader(ast.NodeVisitor):
    def __init__(self):
        self.getAttr = ""

    def visit_Attribute(self,node):
        self.getAttr = node.attr

class couplingReader(ast.NodeVisitor):
    def __init__(self):
        self.getName = deque()

    @property
    def name(self):
        return '.'.join(self.getName)

    def visit_Name(self,node):
        if self.getName != deque():
            self.getName.appendleft(node.id)

    def visit_Attribute(self,node):
        self.getName.appendleft(node.attr)
        self.generic_visit(node)

class ditReader(ast.NodeVisitor):
    def __init__(self):
        self.getBase = ''

    def visit_ClassDef(self,node):
        if (len(node.bases) == 1):
            self.getBase = node.bases[0].id

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
                classDefinitions.append(element.name)
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
        print("LCOM4 \n----------")
        for i in range(len(masterList)):
            j = masterList[i]
            lcom = len(j)-1
            for n in range(1,len(j)-1):
                for n1 in range(n+1,len(j)):
                   if (set(j[n]) & set(j[n1]) != set()):
                       lcom -= 1
            print(j[0] + " = " + str(lcom))



    def cbo(self):
        tree = ast.parse(open(self.userFile).read())
        print("CBO \n----------")
        masterList = []
        foundClasses = []
        # makes a list of all function definitions for specified for each class
        for element in ast.walk(tree):
            if isinstance(element, ast.ClassDef):
                varDict = {}
                varList = []
                masterList.append(element.name)
                for classNodes in element.body:
                    if isinstance(classNodes, ast.FunctionDef):

                        for node in classNodes.body:
                            visitAttr = couplingReader()
                            visitAttr.visit(node)
                            if classNodes.name == '__init__' and visitAttr.name != '':
                                if not visitAttr.name.startswith('self.'):
                                    varDict[visitAttr.name.split('.')[2]] = visitAttr.name.split('.')[0]
                            elif visitAttr.name != '':
                                varList.append(visitAttr.name)
                otherClassList = []
                for varNames in varList:
                    splitVarNames = varNames.split('.')
                    if splitVarNames[0] != 'self':
                        otherClassList.append(splitVarNames[0])
                    if varDict != {}:
                        for key,value in varDict.items():
                            if key in splitVarNames:
                                otherClassList.append(value)
                print(otherClassList)
                foundClasses.append(otherClassList)

        for index in range(len(masterList)):
            for index2 in range(len(masterList)):
                CBO=0
                for className in foundClasses[index2]:
                    if className == masterList[index]:
                        CBO += 1
                print(masterList[index] + " compared to " + masterList[index2] + " cbo is " + str(CBO))


    def dit(self):
        print("DIT \n----------")
        tree = ast.parse(open(self.userFile).read())
        ditList = {}
        resultDict = {}
        for element in ast.walk(tree):
            if isinstance(element, ast.ClassDef):
                resultDict[element.name]=0
                visitAttr = ditReader()
                visitAttr.visit(element)
                if (visitAttr.getBase !=''):
                    ditList[element.name] = visitAttr.getBase
        for key,value in ditList.items():
            resultDict[key] += 1
            newKey = value
            while newKey in ditList.keys():
                resultDict[key] +=1
                newKey = ditList[newKey]
        for key,value in resultDict.items():
            print(key)
            print(value)


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
#f.cbo()
f.dit()
#f.noc()
#f.wmc()

