from typing import Optional


def is_verbatim(input_text: str) -> Optional[str]:
    """
    Check if a user input is a "verbatim request", meaning it should
    be parsed without checking for correctness or close matches.

    If verbatim, return the string without the verbatim signifier.
    Otherwise, returns None.

    Arguments:
        input_text: String to check for verbatimness.

    Returns:
        None if not verbatim request, otherwise verbatim text.
    """

    # First check - wrapped in quotes.
    if input_text[0] == '"' and input_text[-1] == '"':
        return input_text[1:-1]

    # Second check - ends with an asterix.
    elif input_text[-1] == "*" and len(input_text) > 1:
        return input_text[:-1]

    # Any other checks go here.

    # Not verbatim
    return None
