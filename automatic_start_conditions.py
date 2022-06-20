def get_start_condition(comm_type, commandList, q):
    # print(comm_type, " ; ", command, " ; ", q)

    if comm_type == "assign":
        var = commandList[0]
        expr = commandList[1]
        result = "(" + q + ")[" + expr + " / " + var + "]"
        print("assign pn: ", result)
        return result

    elif comm_type == "series":
        stmt = commandList[0]
        if len(commandList) != 1:
            result = "pn(" + stmt + "," + get_start_condition("series", commandList[2:], q) + ")"
        else:
            result = "pn(" + stmt + "," + q + ")"
        print("series pn: ", result)
        return result

    elif comm_type == "if":
        ifCond = commandList[0]
        posResult = str(commandList[1])
        negResult = str(commandList[2])
        result = "(" + ifCond + " and " + posResult + ") or (not " + ifCond + " and " + negResult + ")"
        print("if pn: ", result)
        return result

    elif comm_type == "loop":
        print("loop pn: ", commandList)
        return commandList

    else:
        return None
