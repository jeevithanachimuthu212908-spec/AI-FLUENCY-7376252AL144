def read_notice():
    """Read the college fee notice and return its contents as plain text."""
    
    try:
        with open("notice.txt", "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"ERROR: Could not read the notice. {e}"
    