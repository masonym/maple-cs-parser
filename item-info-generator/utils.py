def format_description(description):
    """
    Format a description string to make it more readable.
    """
    if description:
        return description.replace("#c", "").replace("\\n", "\n").replace("#", "").replace("\\r", "")
    return None