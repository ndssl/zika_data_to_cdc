"""
Unit tests for `helper.py`
"""
import os
import sys

sys.path.append(os.getcwd())
import src.helper as helper


def strip_accents_test():
    c = helper.strip_accents('hello')
    e = 'hello'
    assert c == e

    c = helper.strip_accents('Piauí')
    e = 'Piaui'
    assert c == e

    s = 'Maranhão'
    c = helper.strip_accents(s)
    e = 'Maranhao'
    assert c == e
    # print(s, c, e, file=sys.stderr)


def get_report_date_from_filepath_test():
    test_cases = [
        '/home/dchen/git/vbi/zika-data/data/parsed/brazil/brazil-microcephaly-2016-01-23-table-1.csv',
        '/home/dchen/git/vbi/zika-data/data/parsed/colombia/colombia-2016-01-22.csv',
        '/home/dchen/git/vbi/zika-data/data/parsed/colombia/colombia-municipal-2016-01-09.csv']

    expected_results = ['2016-01-23', '2016-01-22', '2016-01-09']

    for i, test_case in enumerate(test_cases):
        c = helper.get_report_date_from_filepath(test_case)
        e = expected_results[i]
        assert c == e
