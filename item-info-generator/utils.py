def format_description(description):
    """
    Format a description string to make it more readable.
    """
    if description:
        return description.replace("#c", "").replace("\\n", "\n").replace("#", "").replace("\\r", "")
    return None

def get_gender_from_id(nItemID):
    nItemID = int(nItemID)
    if nItemID // 1000000 != 1:
        return 2
    switch = nItemID // 1000 % 10
    if switch == 0:
        return 0
    elif switch == 1:
        return 1
    else:
        return 2