from typing import Optional, Union


def pad_sides(title: str, side_len: int = 3, buffer_filler: str = "=") -> str:
    """
    Print "title" with a padding on either side made of "buffer_filler".

    Args:
        title: String to be displayed with padding.
        side_len: Integer presenting length of buffer on either side. Default 3.
        buffer_filler: Characters to use for the buffer.

    Returns:
        The padded string.
    """
    sides = side_len * buffer_filler
    return sides + title + sides


def welcome() -> None:
    """
    Welcome graphic for the program.
    """
    version = 0.7
    print(pad_sides(f" vitals {version} ", 5))


def prompt_user(current_level: Optional[Union[list[str], str]] = None) -> str:
    """
    Prompts the user for a response. Current level is indicative of which
    terminal the prompt is active from, and is used for display only.

    Args:
        current_level: Ordered list of the levels leading to this prompt.

    Returns:
        String input by user.

    """
    prompt_level = ""
    if isinstance(current_level, list):
        for level in current_level:
            prompt_level += f"({level.lower()}) "
    else:
        # Either single prompt level, or no level at all.
        prompt_level = f"({current_level.lower()}) " if current_level else " "

    return input(f"{prompt_level}-> ")
