from difflib import SequenceMatcher
from typing import Optional


def get_closest_matches(
    candidate_string: str, possible_strings: list[str], number_of_results: int = 1
) -> list[str]:
    """
    Given a candidate string, and a list of possible strings, return a subset of possible_strings sorted
    by similarity to the candidate string. Number of results determines how many to return.

    Arguments:
        candidate_string: The string to be matched.
        possible_strings: The strings to match against.
        number_of_results: The number of strings to return.

    Returns:
        A list of the `number_of_results` closest strings in `possible_strings` to
        `candidate_string`.
    """
    ranks = {
        SequenceMatcher(None, candidate_string, possible).ratio(): possible
        for possible in possible_strings
    }
    sorted_ranks = [
        value
        for _, value in sorted(ranks.items(), key=lambda item: item[0], reverse=True)
    ]

    return sorted_ranks[:number_of_results]


def get_closest_match(
    candidate_string: str, possible_strings: list[str]
) -> Optional[str]:
    """
    Helper function to graph the single closest value. Returns a single string.

    Arguments:
    candidate_string: The string to be matched.
    possible_strings: The strings to match against.

    Returns:
        The closest string in `possible_strings` to `candidate_string`.
    """
    return get_closest_matches(
        candidate_string=candidate_string,
        possible_strings=possible_strings,
        number_of_results=1,
    )[0]
