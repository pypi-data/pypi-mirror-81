#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains all functions that can be used in a sheet. 

All functions describe their behavior with a function documentation object
in the function docstring. Function documentation objects are described
in more detail in docs/README.md.

NOTE: This file is alphabetical order!
"""
from typing import List, Union
from functools import reduce
import pandas as pd


def AVG(*argv: List[Union[pd.Series, int, float]]) -> pd.Series:
    """
    {
        "function": "AVG",
        "description": "Returns the numerical mean value of the passed numbers and series.",
        "examples": [
            "AVG(1, 2)",
            "AVG(A, B)",
            "AVG(A, 2)"
        ],
        "syntax": "AVG(value1, [value2, ...])",
        "syntax_elements": [{
                "element": "value1",
                "description": "The first number or series to consider when calculating the average."
            },
            {
                "element": "value2, ... [OPTIONAL]",
                "description": "Additional numbers or series to consider when calculating the average."
            }
        ]
    }
    """
    return SUM(*argv) / len(argv)


def CLEAN(series: pd.Series) -> pd.Series:
    """
    {
        "function": "CLEAN",
        "description": "Returns the text with the non-printable ASCII characters removed.",
        "examples": [
            "CLEAN('ABC\\n')"
        ],
        "syntax": "CLEAN(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series whose non-printable characters are to be removed."
            }
        ]
    }
    """
    return series.apply(lambda x:''.join([i if 32 < ord(i) < 126 else "" for i in x]))


def CONCATENATE(*argv: List[Union[pd.Series, str]]) -> pd.Series:
    """
    {
        "function": "CONCATENATE",
        "description": "Returns the passed strings and series appended together.",
        "examples": [
            "CONCATENATE('Bite', 'the bullet')",
            "CONCATENATE(A, B)"
        ],
        "syntax": "CONCATENATE(string1, [string2, ...])",
        "syntax_elements": [{
                "element": "string1",
                "description": "The first string or series."
            },
            {
                "element": "string2, ... [OPTIONAL]",
                "description": "Additional strings or series to append in sequence."
            }
        ]
    }
    """

    def as_string(x):
        if isinstance(x, pd.Series):
            return x.astype('str')
        else:
            return str(x)

    return as_string(reduce((lambda x, y: as_string(x) + as_string(y)), argv))


def FIND(series: pd.Series, substring: str) -> pd.Series:
    """
    {
        "function": "FIND",
        "description": "Returns the position at which a string is first found within text, case-sensitive. Returns 0 if not found.",
        "examples": [
            "FIND(A, 'Jack')",
            "FIND('Ben has a friend Jack', 'Jack')"
        ],
        "syntax": "FIND(text_to_search, search_for)",
        "syntax_elements": [{
                "element": "text_to_search",
                "description": "The text or series to search for the first occurrence of search_for."
            },
            {
                "element": "search_for",
                "description": "The string to look for within text_to_search."
            }
        ]
    }
    """
    # NOTE: we do not cast _back_ to the original type, as 
    # we always want to return numbers!

    if substring is None:
        raise Exception(f'Must pass a substring to FIND, {substring} is not valid.')
    str_series = series.astype('str')
    # We add 1 to match Excel's behavior
    return str_series.str.find(substring) + 1


def LEFT(series: pd.Series, num_chars: int = 1) -> pd.Series:
    """
    {
        "function": "LEFT",
        "description": "Returns a substring from the beginning of a specified string.",
        "examples": [
            "LEFT(A, 2)",
            "LEFT('The first character!')"
        ],
        "syntax": "LEFT(string, [number_of_characters])",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series from which the left portion will be returned."
            },
            {
                "element": "number_of_characters [OPTIONAL, 1 by default]",
                "description": "The number of characters to return from the start of string."
            }
        ]
    }
    """
    series_dtype = series.dtype
    str_series = series.astype('str')
    if (num_chars < 0):
        raise ValueError(f'num_chars must be > 0, cannot be {num_chars}')
    elif (num_chars == 0):
        return str_series.str[0:0].astype(series_dtype)
    return str_series.str[0:num_chars].astype(series_dtype)


def LEN(series: pd.Series) -> pd.Series:
    """
    {
        "function": "LEN",
        "description": "Returns the length of a string.",
        "examples": [
            "LEN(A)",
            "LEN('This is 21 characters')"
        ],
        "syntax": "LEN(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series whose length will be returned."
            }
        ]
    }
    """
    return series.astype('str').str.len()


def LOWER(series: pd.Series) -> pd.Series:
    """
    {
        "function": "LOWER",
        "description": "Converts a given string to lowercase.",
        "examples": [
            "=LOWER('ABC')",
            "=LOWER(A)",
            "=LOWER('Nate Rush')"
        ],
        "syntax": "LOWER(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series to convert to lowercase."
            }
        ]
    }
    """
    series_dtype = series.dtype
    str_series = series.astype('str')
    return str_series.str.lower().astype(series_dtype)


def MID(series: pd.Series, start_loc: int, num_chars: int) -> pd.Series:
    """
    {
        "function": "MID",
        "description": "Returns a segment of a string.",
        "examples": [
            "MID(A, 2, 2)",
            "MID('Some middle characters!', 3, 4)"
        ],
        "syntax": "MID(string, starting_at, extract_length)",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series to extract the segment from."
            },
            {
                "element": "starting_at",
                "description": "The index from the left of string from which to begin extracting."
            },
            {
                "element": "extract_length",
                "description": "The length of the segment to extract."
            }
        ]
    }
    """
    series_dtype = series.dtype
    return series.astype('str').str.slice(start=(start_loc - 1), stop=(start_loc + num_chars - 1)).astype(series_dtype)


def MULTIPLY(*argv: List[Union[pd.Series, int, float]]) -> pd.Series:
    """
    {
        "function": "MULTIPLY",
        "description": "Returns the product of two numbers.",
        "examples": [
            "MULTIPLY(2,3)",
            "MULTIPLY(A,3)"
        ],
        "syntax": "MULTIPLY(factor1, [factor2, ...])",
        "syntax_elements": [{
                "element": "factor1",
                "description": "The first number to multiply."
            },
            {
                "element": "factor2, ... [OPTIONAL]",
                "description": "Additional numbers or series to multiply."
            }
        ]
    }
    """
    return reduce((lambda x, y: x * y), argv) 


def PROPER(series: pd.Series) -> pd.Series:
    """
    {
        "function": "PROPER",
        "description": "Capitalizes the first letter of each word in a specified string.",
        "examples": [
            "=PROPER('nate nush')",
            "=PROPER(A)"
        ],
        "syntax": "PROPER(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The value or series to convert to convert to proper case."
            }
        ]
    }
    """
    return series.astype('str').str.title()

def RIGHT(series: pd.Series, num_chars: int = 1) -> pd.Series:
    """
    {
        "function": "RIGHT",
        "description": "Returns a substring from the beginning of a specified string.",
        "examples": [
            "RIGHT(A, 2)",
            "RIGHT('The last character!')"
        ],
        "syntax": "RIGHT(string, [number_of_characters])",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series from which the right portion will be returned."
            },
            {
                "element": "number_of_characters [OPTIONAL, 1 by default]",
                "description": "The number of characters to return from the end of string."
            }
        ]
    }
    """
    series_dtype = series.dtype
    str_series = series.astype('str')
    if (num_chars < 0):
        raise ValueError(f'num_chars must be > 0, cannot be {num_chars}')
    elif (num_chars == 0):
        return str_series.str[0:0].astype(series_dtype)
    return str_series.str[-(num_chars):].astype(series_dtype)


def SUBSTITUTE(series: pd.Series, old_text: str, new_text: str, instance: int = -1):
    """
    {
        "function": "SUBSTITUTE",
        "description": "Replaces existing text with new text in a string.",
        "examples": [
            "SUBSTITUTE('Better great than never', 'great', 'late')",
            "SUBSTITUTE(A, 'dog', 'cat')"
        ],
        "syntax": "SUBSTITUTE(text_to_search, search_for, replace_with, [occurrence_number])",
        "syntax_elements": [{
                "element": "text_to_search",
                "description": "The text within which to search and replace."
            },
            {
                "element": "search_for",
                "description": " The string to search for within text_to_search."
            },
            {
                "element": "replace_with",
                "description": "The string that will replace search_for."
            },
            {
                "element": "occurrence_number",
                "description": "The number of times to perform the replace. Defaults to all."
            }
        ]
    }
    """

    series_dtype = series.dtype
    return series.astype('str').str.replace(old_text, new_text, n=instance).astype(series_dtype)


def SUM(*argv: List[Union[pd.Series, int, float]]) -> pd.Series:
    """
    {
        "function": "SUM",
        "description": "Returns the sum of the given numbers and series.",
        "examples": [
            "SUM(10, 11)",
            "SUM(A, B, D, F)",
            "SUM(A, B, D, F)"
        ],
        "syntax": "SUM(value1, [value2, ...])",
        "syntax_elements": [{
                "element": "value1",
                "description": "The first number or column to add together."
            },
            {
                "element": "value2, ... [OPTIONAL]",
                "description": "Additional numbers or columns to sum."
            }
        ]
    }
    """
    return reduce((lambda x, y: x + y), argv) 


def TRIM(series: pd.Series) -> pd.Series:
    """
    {
        "function": "TRIM",
        "description": "Returns a string with the leading and trailing whitespace removed.",
        "examples": [
            "=TRIM('  ABC', 'ABC')",
            "=TRIM('  ABC  ', 'ABC')",
            "=TRIM(' A B C ', 'A B C')"
        ],
        "syntax": "TRIM(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The value or series to remove the leading and trailing whitespace from."
            }
        ]
    }
    """
    def trim_string(x):
        if isinstance(x, str):
            return x.strip()
        else:
            return x
    
    return series.apply(lambda x: trim_string(x))


def UPPER(series: pd.Series) -> pd.Series:
    """
    {
        "function": "UPPER",
        "description": "Converts a given string to uppercase.",
        "examples": [
            "=UPPER('abc')",
            "=UPPER(A)",
            "=UPPER('Nate Rush')"
        ],
        "syntax": "UPPER(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series to convert to uppercase."
            }
        ]
    }
    """
    series_dtype = series.dtype
    str_series = series.astype('str')
    return str_series.str.upper().astype(series_dtype)


# TODO: we should see if we can list these automatically!
FUNCTIONS = {
    'AVG': AVG,
    'CLEAN': CLEAN,
    'CONCATENATE': CONCATENATE,
    'FIND': FIND,
    'LEFT': LEFT,
    'LEN': LEN,
    'LOWER': LOWER,
    'MID': MID,
    'MULTIPLY': MULTIPLY,
    'PROPER': PROPER,
    'RIGHT': RIGHT,
    'SUBSTITUTE': SUBSTITUTE,
    'SUM': SUM,
    'TRIM': TRIM,
    'UPPER': UPPER,
}