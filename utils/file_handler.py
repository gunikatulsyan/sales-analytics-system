def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.

    Returns: list of raw lines (strings)
    """

    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            with open(filename, "r", encoding=encoding) as file:
                lines = file.readlines()
                lines = lines[1:]
                cleaned_lines = [line.strip() for line in lines if line.strip()]
                return cleaned_lines
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
    print("Error: Unable to read file due to encoding issues.")
    return []
