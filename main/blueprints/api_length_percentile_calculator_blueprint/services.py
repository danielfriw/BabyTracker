import os

import pandas as pd


def percentile_calc(gender: str, age_in_months: int, length: float):
    """
    This function calculates the percentile of a baby's length given the baby's age in months and length in cm.
    z_score_percentile_table is a dictionary containing the z-score and the corresponding percentile.
    :param: gender: str: baby's gender as 'f' or 'm'
    :param: age_in_months: int: baby's age in months
    :param: length: float: baby's length in cm
    """
    zscore = calculate_zscore(gender, age_in_months, length)
    return extract_percentile_from_zscore_table(zscore)


def calculate_zscore(gender: str, age_in_months: int, length: float):
    """
    This function calculates the z-score of a baby's length given the baby's age in months and length in cm.
    lms_data is a dictionary containing the L, M, and S values for calculating the z-score.
    We calculate the z-score using the formula: z = ((length / M) ** L - 1) / (L * S)
    :param gender:
    :param age_in_months:
    :param length:
    :return:
    """

    if age_in_months < 0 or age_in_months > 24:
        raise ValueError('Age is out of range. Please enter a valid age between 0 and 24 months.')

    lms_data = get_lms_parameters_data_by_gender(gender)

    l = lms_data['power_l'][age_in_months]
    m = lms_data['median_m'][age_in_months]
    s = lms_data['variation_s'][age_in_months]

    return (((length / m) ** l) - 1) / (l * s)


def get_lms_parameters_data_by_gender(gender: str):
    """
    This function returns the LMS parameters depending on the gender of the baby.
    """
    if gender == 'm':
        csv_file = get_static_data_file_path('lms_parameters_male.csv')
    else:
        csv_file = get_static_data_file_path('lms_parameters_female.csv')

    return pd.read_csv(csv_file).to_dict()


def get_static_data_file_path(file_name: str):
    """
    This function returns the path of the static data file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'static_data', file_name)


def extract_percentile_from_zscore_table(zscore: float):
    """
    This function returns the percentile given the z-score.
    """
    if zscore < -3.0 or zscore > 3.0:
        raise ValueError('Length is too {} for given age range. Please enter a valid Length.'.format(
            'low' if zscore < -3.0 else 'high'))

    z_row = extract_z_table_row(zscore)
    z_col = extract_z_table_col(zscore)

    z_score_percentile_table_dict = get_z_score_percentile_table_dict()
    percentile = z_score_percentile_table_dict[z_row][z_col]
    return percentile


def extract_z_table_row(zscore: float) -> float:
    """
    This function extracts the row from the z-score to be used to find the percentile in the z-score percentile table.
    z_row is the first two digits of the z-score.
    For example, for a z-score of -1.23 -> z_row = -1.2
    @param zscore: float: z-score
    @return: float: z_row
    """
    sign = -1 if zscore < 0 else 1
    return sign * float(str(abs(zscore))[:3])


def extract_z_table_col(zscore: float) -> str:
    """
    This function extracts the column from the z-score to be used to find the percentile in the z-score percentile table.
    z_col is the last decimal digit of the z-score.
    For example, for a z-score of -1.23 -> z_col = 0.03
    @param zscore: float: z-score
    @return: str: z_col
    """
    return '0.0' + str(abs(zscore))[3]


def get_z_score_percentile_table_dict():
    """
    This function returns the z-score percentile table as a dictionary where the z-score is the key and the percentile is the value.
    example (first row in table): {-3.0: {'.00': 0.13, '.01': 0.13, [...]}, [...] }
    """
    csv_file = get_static_data_file_path('z_score_percentile_table.csv')
    z_score_table = pd.read_csv(csv_file)
    z_score_table.set_index('Z', inplace=True)
    return z_score_table.to_dict(orient='index')
