from typing import Optional, Union


def buffer_sides(title: str, side_len: int = 3, buffer_filler: str = "=") -> str:
    return side_len * buffer_filler + title + side_len * buffer_filler


def cli_warn(warning_text: str) -> str:
    """
    Standardised CLI warning, returns text for use in logging.
    """

    combined_text = "(WARNING): " + warning_text
    print(combined_text)
    return combined_text


def welcome():
    version = 0.5
    print(buffer_sides(f" vitals {version} ", 5))


def prompt_user(current_level: Optional[Union[list[str], str]] = None) -> str:
    prompt_level = ""
    if isinstance(current_level, list):
        for level in current_level:
            prompt_level += f"({level.lower()}) "
    else:
        prompt_level = f"({current_level.lower()}) " if current_level else " "

    return input(f"{prompt_level}-> ")
