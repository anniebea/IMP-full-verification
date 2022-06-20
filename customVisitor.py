import IMP_py.IMP_DVisitor
from IMP_py.IMP_DParser import IMP_DParser
from automatic_start_conditions import get_start_condition
from state_dict_cleanup import *


class CustomVisitor(IMP_py.IMP_DVisitor.IMP_DVisitor):
    startState = "p"
    endState = "q"
    currState = ""
    loopCount = 0
    tempCount = 0
    rulesList = dict()
    invarList = dict()

    def visitProgr(self, ctx: IMP_DParser.ProgrContext):
        return str(self.visitChildren(ctx))

    def visitStmt(self, ctx: IMP_DParser.StmtContext):
        if ctx.cond_stmt() is not None:
            return self.visitCond_stmt(ctx.getChild(0))
        elif ctx.loop() is not None:
            return self.visitLoop(ctx.getChild(0))
        elif ctx.input_stmt() is not None:
            return self.visitInput_stmt(ctx.getChild(0))
        elif ctx.output_stmt() is not None:
            return self.visitOutput_stmt(ctx.getChild(0))
        elif ctx.assign_stmt() is not None:
            return self.visitAssign_stmt(ctx.getChild(0))

        return self.visitChildren(ctx)

    def visitSeries(self, ctx: IMP_DParser.SeriesContext):
        serEndState = self.endState
        seriesStmts = list()
        if ctx.getChildCount() != 1:
            self.tempCount += 1
            self.endState = "midcondition" + str(self.tempCount)
        stmtVal = str(self.visitStmt(ctx.getChild(0)))
        result = stmtVal
        seriesStmts.append(stmtVal)
        for i in range(2, ctx.getChildCount(), 2):
            self.startState = self.endState
            if i == ctx.getChildCount()-1:
                self.endState = serEndState
            else:
                self.tempCount += 1
                self.endState = "midcondition" + str(self.tempCount)
            seriesStmts.append(";")
            stmtVal = str(self.visitStmt(ctx.getChild(i)))
            result += " ; " + stmtVal
            seriesStmts.append(stmtVal)
        # print("PN'S: ", get_start_condition("series", seriesStmts, self.endState))
        # print("SERRESULT: ", result, " (serresult)")
        return result

    def visitAssign_stmt(self, ctx: IMP_DParser.Assign_stmtContext):
        var = str(ctx.getChild(0))
        expr = str(self.visitExpr(ctx.getChild(2)))

        self.rulesList[self.startState] = get_start_condition("assign", [var, expr], self.endState)

        result = var + ":=" + expr
        return result

    def visitLoop(self, ctx: IMP_DParser.LoopContext):
        loopStartState = self.startState
        loopEndState = self.endState
        invariantNum = self.visitInvariant(ctx.getChild(1))
        invariant = self.invarList[str(invariantNum)]
        # print("INVARIANT: ", invariant)

        loopCond = self.visitLog_expr(ctx.getChild(2))

        self.startState = str(invariant) + " and " + str(loopCond)
        self.endState = str(invariant)
        loopBody = self.visitSeries(ctx.getChild(4))
        result = "while " + loopCond + " do " + loopBody + " od"
        self.startState = loopStartState

        self.rulesList[self.startState] = invariant
        self.rulesList[str(invariant) + " and not " + str(loopCond)] = loopEndState

        get_start_condition("loop", invariant, self.endState)
        self.endState = loopEndState
        self.loopCount += 1
        return result

    def visitInvariant(self, ctx: IMP_DParser.InvariantContext):
        return ctx.getChild(1)

    def visitCond_stmt(self, ctx: IMP_DParser.Cond_stmtContext):  # IF STATEMENT
        ifStart = self.startState

        ifCond = str(self.visitLog_expr(ctx.getChild(1)))
        self.startState += " and " + ifCond
        posResult = str(self.visitSeries(ctx.getChild(3)))
        self.startState = ifStart + " and not " + ifCond
        negResult = str(self.visitSeries(ctx.getChild(5)))

        result = "(" + posResult + " -- " + negResult + ")"
        get_start_condition("if", [ifCond, posResult, negResult], self.endState)

        return result

    def visitExpr(self, ctx: IMP_DParser.ExprContext):
        result = str(self.visitTerm(ctx.getChild(0)))
        for i in range(2, ctx.getChildCount(), 2):
            if str(ctx.getChild(i-1)) == "+":
                result += "+" + str(self.visitTerm(ctx.getChild(i)))
            else:
                result += "-" + str(self.visitTerm(ctx.getChild(i)))
        return result

    def visitTerm(self, ctx: IMP_DParser.TermContext):
        result = str(self.visitElem(ctx.getChild(0)))
        for i in range(2, ctx.getChildCount(), 2):
            if str(ctx.getChild(i-1)) == "*":
                result += "*" + str(self.visitElem(ctx.getChild(i)))
            else:
                result += "/" + str(self.visitElem(ctx.getChild(i)))
        return result

    def visitElem(self, ctx: IMP_DParser.ElemContext):
        if str(ctx.getChildCount()) == "1":  # NUMBER | VARNAME
            result = str(ctx.getChild(0))
        else:  # LPARENTHESIS expr RPARENTHESIS
            result = self.visitExpr(ctx.getChild(1))
        return result

    def visitLog_expr(self, ctx: IMP_DParser.Log_exprContext):
        result = str(self.visitLog_term(ctx.getChild(0)))
        for i in range(2, ctx.getChildCount(), 2):
            result += " or " + str(self.visitLog_term(ctx.getChild(i)))
        return result

    def visitLog_term(self, ctx: IMP_DParser.Log_exprContext):
        result = str(self.visitLog_elem(ctx.getChild(0)))
        for i in range(2, ctx.getChildCount(), 2):
            result += " and " + str(self.visitLog_elem(ctx.getChild(i)))
        return result

    def visitLog_elem(self, ctx: IMP_DParser.Log_elemContext):
        result = None
        if str(ctx.getChildCount()) == "1":  # BOOL | condition | VARNAME
            if ctx.condition() is not None:
                result = "" + str(self.visitCondition(ctx.getChild(0)))
            else:
                result = "" + str(ctx.getChild(0))
        elif str(ctx.getChildCount()) == "2":  # NOT ( BOOL | condition | VARNAME )
            if ctx.condition() is not None:
                result = "not " + str(self.visitCondition(ctx.getChild(1)))
            else:
                result = "not " + str(ctx.getChild(1))
        elif str(ctx.getChildCount()) == "3":  # LPARENTHESIS log_expr RPARENTHESIS
            result = self.visitLog_expr(ctx.getChild(1))
        elif str(ctx.getChildCount()) == "4":  # NOT LPARENTHESIS log_expr RPARENTHESIS
            result = "not " + str(self.visitLog_expr(ctx.getChild(2)))
        return result

    def visitCondition(self, ctx: IMP_DParser.ConditionContext):  # expr RELATION expr
        childVal1 = str(ctx.getChild(1))
        childVal0 = str(self.visitExpr(ctx.getChild(0)))
        childVal2 = str(self.visitExpr(ctx.getChild(2)))
        return str(childVal0) + str(childVal1) + str(childVal2)

"""
<antlr4.tree.Tree.TerminalNodeImpl object at 0x000001FFBC30A040>,                   while
<IMP_py.IMP_DParser.IMP_DParser.InvariantContext object at 0x000001FFBC2F7B50>,     invariant
<IMP_py.IMP_DParser.IMP_DParser.Log_exprContext object at 0x000001FFBC2F7BC0>,      log_epr
<antlr4.tree.Tree.TerminalNodeImpl object at 0x000001FFBC30B1C0>,                   do
<IMP_py.IMP_DParser.IMP_DParser.SeriesContext object at 0x000001FFBC560200>,        series
<antlr4.tree.Tree.TerminalNodeImpl object at 0x000001FFBC30B980>                    od
"""
