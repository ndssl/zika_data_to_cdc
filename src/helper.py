import re
import glob
import os

import unicodedata


def strip_accents(s):
    """
    Remove accents from string and replace with closest ascii text

    Code taken from stackoverflow:
    http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string

    Parameters
    ----------
    s : str
        String with accents

    Returns
    -------
    str
        String with accents replaced with closest ascii character
    """
    return(''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn'))


def get_data_from_path(path_with_pattern=None,
                       path_only=None, data_pattern='*.csv'):
    """
    Finds all files from `path` that match the `data_pattern`
    """
    if path_with_pattern is not None:
        return glob.glob(path_with_pattern)
    elif path_only is not None:
        get_data_from_path(
            path_with_pattern=os.path.join(path_only, data_pattern))


def get_report_date_from_filepath(filepath,
                                  date_pattern=r'\d{4}.*\d{2}.*\d{2}',
                                  date_result_position=0):
    """
    Parse the filepath to get the date

    Parameters
    ----------
    filepath : str
        filepath to be parsed
    date_pattern : str, optional
        by default, `r'\d{4}.*\d{2}.*\d{2}'`
        regex pattern for the date in `filepath`
    data_result_position : int, optional
        By default, `0'.
        Returns the position of matches from `re.findall`

    Returns
    -------
    string
        string match for `date_pattern`
    """
    return re.findall(date_pattern, filepath)[date_result_position]
