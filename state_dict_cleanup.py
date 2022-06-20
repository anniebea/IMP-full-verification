def state_clean(d):
    # 1. find key that can be deleted
    # 2. bind the redundant keys value to original key
    # 3. delete the redundant item
    # 4. repeat step 1 as long as it returns a value
    while find_key(d) is not None:
        key = find_key(d)
        keyValue = str(d[key])
        d[key] = d[keyValue]
        del d[keyValue]
    removeTemps(d)


def find_key(d):
    for key in d:
        if d[key] in d:
            return key
    return None


def removeTemps(d):
    tempKeys = dict()
    # find all temporary keys
    for key in d:
        if "midcondition" in key:
            tempKeys[key] = d[key]
    # transfer values from temporary keys to real ones
    for key in d:
        while "midcondition" in d[key]:
            value = str(d[key])
            tempNum = value.split("midcondition", 1)[1][0]
            temp = "midcondition" + str(tempNum)
            value = value.replace(temp, tempKeys[temp])
            d[key] = value
    # delete all temporary keys
    for key in tempKeys:
        del d[key]
