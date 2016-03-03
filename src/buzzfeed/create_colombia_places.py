import os
import sys
import re

import numpy as np
import pandas as pd
import unicodedata

sys.path.append(os.getcwd())
import src.helper as helper


@np.vectorize
def clean_string(x, column, municipality_clean=['Bogota']):
    title_case = x.title().strip()
    # no_accents = unicodedata.normalize('NFKD', title_case).\
    # encode('ascii','ignore')
    no_accents = helper.strip_accents(title_case)
    unknown = re.sub(r'.*Municipio Desconocido$', 'Unknown', no_accents)

    s = unknown
    if column == 'municipality':
        for municipality in municipality_clean:
            regex = r'^{}\s?-\s?'.format(municipality)
            remove_prepend_department = re.sub(regex, '', s)
        dashed = re.sub(r'\s*-\s*', '_', remove_prepend_department)
        s = re.sub(r' ', '_', dashed)
        return(s)
    else:
        s = re.sub(r' ', '_', s)
        return(s)


def main():
    buzzfeed_municipal_colombia_datasets = helper.get_data_from_path(
        os.path.join('..', 'zika-data', 'data',
                     'parsed', 'colombia', '*municipal*.csv'))
    print(buzzfeed_municipal_colombia_datasets)

    all_department_municipality = pd.DataFrame()
    for data_path in buzzfeed_municipal_colombia_datasets:
        df = pd.read_csv(data_path)
        department_municipality = df[['department', 'municipality']]
        all_department_municipality = pd.concat([all_department_municipality,
                                                 department_municipality],
                                                ignore_index=True)
    print("all_department_municipality shape: {}".format(
        all_department_municipality.shape))

    all_department_municipality['state_province'] = clean_string(
        all_department_municipality['department'], 'department')

    all_department_municipality['district_county_municipality'] = clean_string(
        all_department_municipality['municipality'], 'municipality')

    # print(all_department_municipality.
    #       ix[all_department_municipality['municipality'].
    #          str.
    #          match('.*-.*'), :])

    all_department_municipality['country'] = "Colombia"
    all_department_municipality['location_type'] = "state"
    all_department_municipality['city'] = "NA"
    all_department_municipality['alt_name1'] = \
        all_department_municipality['department']
    all_department_municipality['alt_name2'] = \
        all_department_municipality['municipality']
    all_department_municipality['location'] = \
        all_department_municipality['country'] + '-' + \
        all_department_municipality['state_province'] + '-' + \
        all_department_municipality['district_county_municipality']

    co_places = all_department_municipality[['location',
                                             'location_type',
                                             'country',
                                             'state_province',
                                             'district_county_municipality',
                                             'city',
                                             'alt_name1',
                                             'alt_name2']].\
        drop_duplicates()

    co_places.to_csv('output/CO_Places.csv', index=False)
if __name__ == '__main__':
    main()
