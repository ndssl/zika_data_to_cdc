"""
Script to clean the Colombia data from BuzzFeed Zika data repository

Run this script from the root directory
e.g., `~/git/vbi/zika_data_to_cdc'

from there you can run `python src/buzfeed/clean_parsed_colombia.py`
"""
import os
import sys
import re

import pandas as pd

sys.path.append(os.getcwd())
import src.helper as helper


def clean_and_export_municipal(municipal_data_path, places_df, data_guide_df):
    num_data = len(municipal_data_path)
    for idx, data_path in enumerate(municipal_data_path):
        print("cleaning municipal {} of {}".format(idx + 1, num_data))
        df = pd.read_csv(data_path)

        report_date = helper.get_report_date_from_filepath(data_path)
        df['report_date'] = report_date
        df['time_period'] = "NA"

        df = pd.merge(df, places_df,
                      left_on=['department', 'municipality'],
                      right_on=['alt_name1', 'alt_name2'])

        melt_columns = [x for x in df.columns if re.search('^zika_', x)]
        id_vars = [x for x in df.columns if x not in melt_columns]
        df = pd.melt(df,
                     id_vars=id_vars,
                     value_vars=melt_columns,
                     var_name='data_field_original',
                     value_name='value')

        df = pd.merge(df, data_guide_df,
                      left_on=['data_field_original'],
                      right_on=['data_field'])

        df = helper.subset_columns_for_cdc(df)
        df.to_csv('output/colombia-municipal-{}.csv'.format(report_date),
                  index=False)


def clean_and_export_regional(regional_data_path):
    pass


def main():
    places_path = '../zika/Colombia/CO_Places.csv'
    places = pd.read_csv(places_path)

    data_guide_path = '../zika/Colombia/CO_Data_Guide.csv'
    data_guide = pd.read_csv(data_guide_path)

    buzzfeed_colombia_datasets = helper.get_data_from_path(
        os.path.join('..', 'zika-data', 'data',
                     'parsed', 'colombia', '*.csv'))

    print("Datasets found: {}\n".format(buzzfeed_colombia_datasets))

    colombia_municipal = [
        x for x in buzzfeed_colombia_datasets if re.search('municipal', x)]
    colombia_regional = [
        x for x in buzzfeed_colombia_datasets if x not in colombia_municipal]

    print("municipal datasets: {}\n".format(colombia_municipal))
    print("regional datasets: {}\n".format(colombia_regional))

    clean_and_export_municipal(colombia_municipal, places, data_guide)
    clean_and_export_regional(colombia_regional)

if __name__ == '__main__':
    main()
