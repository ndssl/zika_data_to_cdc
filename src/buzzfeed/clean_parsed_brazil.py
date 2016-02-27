"""Clean the Brazil data from BuzzFeed

https://github.com/BuzzFeedNews/zika-data
"""

import os.path
from glob import glob
import re

import pandas as pd
import unicodedata


def strip_accents(s):
    return(''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn'))


def load_data(filepath):
    df = pd.read_csv(filepath)
    return(df)


def get_report_date(filepath,
                    dir_delim='/',
                    file_name_position=-1,
                    date_pattern=r'\d{4}-\d{2}-\d{2}',
                    date_result_position=0):
    file_name = filepath.split(dir_delim)[file_name_position]
    return(re.findall(date_pattern, file_name)[date_result_position])


def get_cdc_places_match(df, cdc_places_df, df_col_name, cdc_places_col_name):
    match = cdc_places_df[cdc_places_df[
        cdc_places_col_name].isin(df[df_col_name])]
    return(match)


def get_location(df, cdc_location_df):
    location = get_cdc_places_match(df, cdc_location_df,
                                    'state_no_accents', 'state_province')
    return(location['location'])


def get_location_type(df, cdc_location_df):
    location_type = get_cdc_places_match(df, cdc_location_df,
                                         'state_no_accents', 'state_province')
    return(location_type['location_type'])


def clean_data(df):

    df['state_no_accents'] = df['state'].apply(strip_accents)
    return df


def get_cdc_data_field_code(cdc_data_guide_df, cdc_str):
    return(cdc_data_guide_df[cdc_data_guide_df['data_field'] ==
                             cdc_str]['data_field_code'].values[0])


def main():
    here = os.path.abspath(os.path.dirname(__file__))

    cdc_brazil_places_df = pd.read_csv(os.path.join(
        here, '../../../zika/Brazil/BR_Places.csv'))
    cdc_brazil_data_guide_df = pd.read_csv(os.path.join(
        here, '../../../zika/Brazil/BR_Data_Guide.csv'))
    cdc_brazil_data_guide_right = cdc_brazil_data_guide_df[['data_field_code', 'data_field',
                                                            'unit']]

    buzzfeed_brazil_datasets = glob(
        '../../../zika-data/data/parsed/brazil/*.csv')

    num_data_sets = len(buzzfeed_brazil_datasets)
    for i, brazil_dataset in enumerate(buzzfeed_brazil_datasets):
        print("Cleaning dataset {} of {}".format(i + 1, num_data_sets))

        df = load_data(brazil_dataset)
        df = clean_data(df)

        report_date = get_report_date(brazil_dataset)
        location = get_location(df, cdc_brazil_places_df)
        location_type = get_location_type(df, cdc_brazil_places_df)

        df['report_date'] = report_date
        df['location'] = location
        df['location_type'] = location_type
        df['time_period'] = 'NA'

        df = pd.melt(df, id_vars=[  # 'no', 'state',
            'report_date', 'location', 'location_type',
            'time_period'],
            value_vars=['cases_under_investigation', 'cases_confirmed',
                        'cases_discarded', 'cases_reported_total'],
            var_name='data_field_original',
            value_name='value')

        pd.merge(df, cdc_brazil_data_guide_right,
                 left_on='data_field_original', right_on='data_field')

        df_file_path = os.path.join(
            here, '..', '..', 'output', brazil_dataset.split('/')[-1])
        df.to_csv(df_file_path)

if __name__ == "__main__":
    main()
