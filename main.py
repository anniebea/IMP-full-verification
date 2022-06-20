import sys
import customVisitor
import json

from IMP_py.IMP_DLexer import IMP_DLexer
from IMP_py.IMP_DParser import IMP_DParser
from antlr4 import *
from antlr4.tree.Trees import Trees
from state_dict_cleanup import *


def main(argv):
    file = open(argv[1], 'r')
    specification = file.readline()
    rawSpec = specification
    specification = specification[1:]
    specification = specification[:-2]
    startState = specification.split(",", 1)[0]
    endState = specification.split(",", 1)[1]
    # print(specification, " -> ", startState, ":", endState)
    invariants = file.readline()
    rawInv = invariants
    invariants = invariants[1:]
    invariants = invariants[:-2]
    invariants = invariants.split(",", -1)
    # print(invariants)
    file.close()

    with open(argv[1], 'r') as fin:
        data = fin.read().splitlines(True)
    with open(argv[1], 'w') as fout:
        fout.writelines(data[2:])

    inputFile = FileStream(argv[1])
    lexer = IMP_DLexer(inputFile)
    stream = CommonTokenStream(lexer)
    parser = IMP_DParser(stream)
    tree = parser.progr()  # progr - start rule
    treeString = Trees.toStringTree(tree, None, parser)
    treeString = treeString.replace("( ", "")
    treeString = treeString.replace(" )", "")

    with open(argv[1], 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(rawSpec.rstrip('\r\n') + '\n' + rawInv.rstrip('\r\n') + '\n' + content)

    # print("")
    # print("======IMP_D string tree, created using ANTLR4======")
    # print(treeString)
    # print("===================================================")
    # print("\n")

    # Visitor rules
    visitor = customVisitor.CustomVisitor()
    visitor.startState = startState
    visitor.endState = endState

    for i in range(0, len(invariants)):
        visitor.invarList[str(i+1)] = invariants[i]
    # print(visitor.invarList)
    result = visitor.visit(tree)

    print("")
    print("=======================RESULT=======================")
    print(result)
    print("------------------FORMATTED RESULT------------------")
    print(json.dumps(visitor.rulesList, sort_keys=False, indent=2))
    print("-------------------CLEANED RESULT-------------------")
    # state_clean(visitor.rulesList)
    removeTemps(visitor.rulesList)
    print(json.dumps(visitor.rulesList, sort_keys=False, indent=2))
    print("====================================================")
    print("")


if __name__ == "__main__":
    main(sys.argv)

"""
LKD aprēķins IMP_D sintaksē:
while not x=y do
    if x=<y then y:=y-x
    else x:=x-y fi
od

LKD aprēķins AM sintaksē:
LOOP(FETCH(y):FETCH(x):EQ:NEG,FETCH(y):FETCH(x):LE:BRANCH(FETCH(x):FETCH(y):SUB:STORE(y),FETCH(y):FETCH(x):SUB:STORE(x)))
"""