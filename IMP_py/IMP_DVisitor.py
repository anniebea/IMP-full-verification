# Generated from C:/Users/anitr/OneDrive/Documents/__University/6sem/PVSUS/MD5/IMP-PARTIAL-CORRECTNESS-GEN\IMP_D.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .IMP_DParser import IMP_DParser
else:
    from IMP_DParser import IMP_DParser

# This class defines a complete generic visitor for a parse tree produced by IMP_DParser.

class IMP_DVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by IMP_DParser#progr.
    def visitProgr(self, ctx:IMP_DParser.ProgrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#series.
    def visitSeries(self, ctx:IMP_DParser.SeriesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#stmt.
    def visitStmt(self, ctx:IMP_DParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#assign_stmt.
    def visitAssign_stmt(self, ctx:IMP_DParser.Assign_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#input_stmt.
    def visitInput_stmt(self, ctx:IMP_DParser.Input_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#output_stmt.
    def visitOutput_stmt(self, ctx:IMP_DParser.Output_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#varlist.
    def visitVarlist(self, ctx:IMP_DParser.VarlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#cond_stmt.
    def visitCond_stmt(self, ctx:IMP_DParser.Cond_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#loop.
    def visitLoop(self, ctx:IMP_DParser.LoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#invariant.
    def visitInvariant(self, ctx:IMP_DParser.InvariantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#log_expr.
    def visitLog_expr(self, ctx:IMP_DParser.Log_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#log_term.
    def visitLog_term(self, ctx:IMP_DParser.Log_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#log_elem.
    def visitLog_elem(self, ctx:IMP_DParser.Log_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#condition.
    def visitCondition(self, ctx:IMP_DParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#expr.
    def visitExpr(self, ctx:IMP_DParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#term.
    def visitTerm(self, ctx:IMP_DParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IMP_DParser#elem.
    def visitElem(self, ctx:IMP_DParser.ElemContext):
        return self.visitChildren(ctx)



del IMP_DParser