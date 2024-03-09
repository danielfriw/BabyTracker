# This file contains the data for the percentiles graph in the app.

def percentile_calc(gender: str, age_in_months: int, length: float):
    """
    This function calculates the percentile of a baby's length given the baby's age in months and length in cm.
    lms_data is a dictionary containing the L, M, and S values for calculating the z-score.
    We calculate the z-score using the formula: z = ((length / M) ** L - 1) / (L * S)
    z_score_percentile_table is a dictionary containing the z-score and the corresponding percentile.

    :param: gender: str: baby's gender as 'f' or 'm'
    :param: age_in_months: int: baby's age in months
    :param: length: float: baby's length in cm
    """
    lms_data = boys_length_for_age if gender == 'm' else girls_length_for_age

    if age_in_months < 0 or age_in_months > 24:
        raise ValueError('Age is out of range. Please enter a valid age.')

    l = lms_data['Power [L]'][age_in_months]
    m = lms_data['Median [M]'][age_in_months]
    s = lms_data['Variation [S]'][age_in_months]

    zscore = (((length / m) ** l) - 1) / (l * s)

    z_row = int(zscore * 10) / 10
    z_col = int(zscore * 100 - int(zscore * 10) * 10)

    if z_row < -3.0:
        raise ValueError('Height is too low for given age range. Please enter a valid height.')
    if z_row > 3.0:
        raise ValueError('Height too high for given age range. Please enter a valid height.')

    percentile = z_score_percentile_table[z_row][z_col]
    return percentile


graph_data_boys = {
    'Month': list(range(25)),
    '2nd percentile': [46.09799, 50.83131, 54.42396, 57.34047, 59.72447, 61.67956, 63.34303, 64.82235, 66.18835,
                       67.48217, 68.71138, 69.88013, 70.99632, 72.06657, 73.09511, 74.08522, 75.04248, 75.96753,
                       76.86417, 77.73119, 78.5717, 79.3865, 80.17925, 80.95077, 81.70586],
    '5': [46.77032, 51.52262, 55.13442, 58.06652, 60.46344, 62.42946, 64.10314, 65.5934, 66.97163, 68.27886, 69.52286,
          70.70738, 71.84023, 72.92816, 73.97491, 74.98384, 75.96033, 76.90533, 77.8221, 78.70973, 79.57106, 80.40724,
          81.22133, 82.01447, 82.79087],
    '10': [47.45809, 52.2298, 55.8612, 58.80924, 61.21939, 63.19658, 64.88071, 66.38216, 67.77291, 69.09384, 70.35297,
           71.55363, 72.70353, 73.80954, 74.87492, 75.9031, 76.89925, 77.86466, 78.80202, 79.71074, 80.59338, 81.45143,
           82.28734, 83.1026, 83.9008],
    '25': [48.60732, 53.41147, 57.0756, 60.0503, 62.48254, 64.4784, 66.18, 67.70013, 69.1118, 70.45564, 71.74005,
           72.96769, 74.14605, 75.28228, 76.37879, 77.43914, 78.46814, 79.46765, 80.43942, 81.38338, 82.30162, 83.19621,
           84.06859, 84.92082, 85.75545],
    '50': [49.8842, 54.7244, 58.4249, 61.4292, 63.886, 65.9026, 67.6236, 69.1645, 70.5994, 71.9687, 73.2812, 74.5388,
           75.7488, 76.9186, 78.0497, 79.1458, 80.2113, 81.2487, 82.2587, 83.2418, 84.1996, 85.1348, 86.0477, 86.941,
           87.8161],
    '75': [51.16108, 56.03733, 59.7742, 62.8081, 65.28946, 67.3268, 69.0672, 70.62887, 72.087, 73.48176, 74.82235,
           76.10991, 77.35155, 78.55492, 79.72061, 80.85246, 81.95446, 83.02975, 84.07798, 85.10022, 86.09758, 87.07339,
           88.02681, 88.96118, 89.87675],
    '90': [52.31031, 57.219, 60.9886, 64.04916, 66.55261, 68.60862, 70.36649, 71.94684, 73.42589, 74.84356, 76.20943,
           77.52397, 78.79407, 80.02766, 81.22448, 82.3885, 83.52335, 84.63274, 85.71538, 86.77286, 87.80582, 88.81817,
           89.80806, 90.7794, 91.7314],
    '95': [52.99808, 57.92618, 61.71538, 64.79188, 67.30856, 69.37574, 71.14406, 72.7356, 74.22717, 75.65854, 77.03954,
           78.37022, 79.65737, 80.90904, 82.12449, 83.30776, 84.46227, 85.59207, 86.6953, 87.77387, 88.82814, 89.86236,
           90.87407, 91.86753, 92.84133],
    '98th percentile': [53.67041, 58.61749, 62.42584, 65.51793, 68.04753, 70.12564, 71.90417, 73.50665, 75.01045,
                        76.45523, 77.85102, 79.19748, 80.50128, 81.77063, 83.0043, 84.20638, 85.38012, 86.52987,
                        87.65323, 88.75241, 89.8275, 90.8831, 91.91615, 92.93123, 93.92634]
}

graph_data_girls = {
    'Month': list(range(25)),
    '2nd percentile': [45.4223043, 49.7787718, 52.9949775, 55.5927758, 57.7609922, 59.5953753, 61.1982833, 62.656588,
                       64.0198138, 65.3120157, 66.5466965, 67.7294251, 68.8650363, 69.9583854, 71.0135941, 72.0315003,
                       73.016649, 73.9729301, 74.9001595, 75.8018023, 76.6778157, 77.5310529, 78.363609, 79.1728908,
                       79.9618054],
    '5': [46.08383, 50.4728, 53.71811, 56.34038, 58.52969, 60.38286, 62.00319, 63.47888, 64.85973, 66.16996, 67.42304,
          68.62467, 69.77953, 70.89228, 71.96683, 73.00432, 74.00908, 74.98475, 75.93146, 76.8524, 77.74783, 78.62035,
          79.47174, 80.3, 81.10777],
    '10': [46.76056, 51.18277, 54.45785, 57.10515, 59.31604, 61.18844, 62.82658, 64.32005, 65.71894, 67.0476, 68.31951,
           69.54048, 70.71503, 71.84762, 72.94195, 73.99947, 75.0243, 76.01981, 76.98644, 77.92712, 78.84242, 79.73466,
           80.60531, 81.453, 82.28006],
    '25': [47.89133, 52.3691, 55.69393, 58.38306, 60.63, 62.53451, 64.20243, 65.72562, 67.15464, 68.51411, 69.81746,
           71.07075, 72.2782, 73.44396, 74.57133, 75.66234, 76.72069, 77.74936, 78.74927, 79.72293, 80.67144, 81.59662,
           82.49946, 83.3796, 84.23889],
    '50': [49.1477, 53.6872, 57.0673, 59.8029, 62.0899, 64.0301, 65.7311, 67.2873, 68.7498, 70.1435, 71.4818, 72.771,
           74.015, 75.2176, 76.3817, 77.5099, 78.6055, 79.671, 80.7079, 81.7182, 82.7036, 83.6654, 84.604, 85.5202,
           86.4153],
    '75': [50.40407, 55.0053, 58.44067, 61.22274, 63.5498, 65.52569, 67.25977, 68.84898, 70.34496, 71.77289, 73.14614,
           74.47125, 75.7518, 76.99124, 78.19207, 79.35746, 80.49031, 81.59264, 82.66653, 83.71347, 84.73576, 85.73418,
           86.70854, 87.6608, 88.59171],
    '90': [51.53484, 56.19163, 59.67675, 62.50065, 64.86376, 66.87176, 68.63562, 70.25455, 71.78066, 73.2394, 74.64409,
           76.00152, 77.31497, 78.58758, 79.82145, 81.02033, 82.1867, 83.32219, 84.42936, 85.50928, 86.56478, 87.59614,
           88.60269, 89.5874, 90.55054],
    '95': [52.21157, 56.9016, 60.41649, 63.26542, 65.65011, 67.67734, 69.45901, 71.09572, 72.63987, 74.11704, 75.54056,
           76.91733, 78.25047, 79.54292, 80.79657, 82.01548, 83.20192, 84.35725, 85.48434, 86.584, 87.65937, 88.71045,
           89.73626, 90.7404, 91.72283],
    '98th percentile': [52.8730957, 57.5956282, 61.1396225, 64.0130242, 66.4188078, 68.4648247, 70.2639167, 71.918012,
                        73.4797862, 74.9749843, 76.4169035, 77.8125749, 79.1649637, 80.4768146, 81.7498059, 82.9882997,
                        84.1943511, 85.3690699, 86.5156405, 87.6345977, 88.7293843, 89.7997471, 90.844391, 91.8675092,
                        92.8687946]
}


# LMS Parameters for Girls: Length-for-age
girls_length_for_age = {
    'Age [months]': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
    'Power [L]': [1] * 25,
    'Median [M]': [49.1477, 53.6872, 57.0673, 59.8029, 62.0899, 64.0301, 65.7311, 67.2873, 68.7498, 70.1435, 71.4818,
                   72.7710, 74.0150, 75.2176, 76.3817, 77.5099, 78.6055, 79.6710, 80.7079, 81.7182, 82.7036, 83.6654,
                   84.6040, 85.5202, 86.4153],
    'Variation [S]': [0.03790, 0.03640, 0.03568, 0.03520, 0.03486, 0.03463, 0.03448, 0.03441, 0.03440, 0.03444, 0.03452,
                      0.03464, 0.03479, 0.03496, 0.03514, 0.03534, 0.03555, 0.03576, 0.03598, 0.03620, 0.03643, 0.03666,
                      0.03688, 0.03711, 0.03734]
}
# LMS Parameters for Boys: Length-for-age
boys_length_for_age = {
    'Age [months]': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
    'Power [L]': [1] * 25,
    'Median [M]': [49.8842, 54.7244, 58.4249, 61.4292, 63.8860, 65.9026, 67.6236, 69.1645, 70.5994, 71.9687, 73.2812,
                   74.5388, 75.7488, 76.9186, 78.0497, 79.1458, 80.2113, 81.2487, 82.2587, 83.2418, 84.1996, 85.1348,
                   86.0477, 86.9410, 87.8161],
    'Variation [S]': [0.03795, 0.03557, 0.03424, 0.03328, 0.03257, 0.03204, 0.03165, 0.03139, 0.03124, 0.03117, 0.03118,
                      0.03125, 0.03137, 0.03154, 0.03174, 0.03197, 0.03222, 0.03250, 0.03279, 0.03310, 0.03342, 0.03376,
                      0.03410, 0.03445, 0.03479]
}

# Z score table

z_score_percentile_table = {
    -3.0: [0.13, 0.13, 0.13, 0.12, 0.12, 0.11, 0.11, 0.11, 0.10, 0.10],
    -2.9: [0.19, 0.18, 0.18, 0.17, 0.16, 0.16, 0.15, 0.15, 0.14, 0.14],
    -2.8: [0.26, 0.25, 0.24, 0.23, 0.23, 0.22, 0.21, 0.21, 0.20, 0.19],
    -2.7: [0.35, 0.34, 0.33, 0.32, 0.31, 0.30, 0.29, 0.28, 0.27, 0.26],
    -2.6: [0.47, 0.45, 0.44, 0.43, 0.41, 0.40, 0.39, 0.38, 0.37, 0.36],
    -2.5: [0.62, 0.60, 0.59, 0.57, 0.55, 0.54, 0.52, 0.51, 0.49, 0.48],
    -2.4: [0.82, 0.80, 0.78, 0.75, 0.73, 0.71, 0.70, 0.68, 0.66, 0.64],
    -2.3: [1.07, 1.04, 1.02, 0.99, 0.96, 0.94, 0.91, 0.89, 0.87, 0.84],
    -2.2: [1.39, 1.36, 1.32, 1.29, 1.26, 1.22, 1.19, 1.16, 1.13, 1.10],
    -2.1: [1.79, 1.74, 1.70, 1.66, 1.62, 1.58, 1.54, 1.50, 1.46, 1.43],
    -2.0: [2.28, 2.22, 2.17, 2.12, 2.07, 2.02, 1.97, 1.92, 1.88, 1.83],
    -1.9: [2.87, 2.81, 2.74, 2.68, 2.62, 2.56, 2.50, 2.44, 2.39, 2.33],
    -1.8: [3.59, 3.52, 3.44, 3.36, 3.29, 3.22, 3.14, 3.07, 3.01, 2.94],
    -1.7: [4.46, 4.36, 4.27, 4.18, 4.09, 4.01, 3.92, 3.84, 3.75, 3.67],
    -1.6: [5.48, 5.37, 5.26, 5.16, 5.05, 4.95, 4.85, 4.75, 4.65, 4.55],
    -1.5: [6.68, 6.55, 6.43, 6.30, 6.18, 6.06, 5.94, 5.82, 5.71, 5.59],
    -1.4: [8.08, 7.93, 7.78, 7.64, 7.49, 7.35, 7.22, 7.08, 6.94, 6.81],
    -1.3: [9.68, 9.51, 9.34, 9.18, 9.01, 8.85, 8.69, 8.53, 8.38, 8.23],
    -1.2: [11.51, 11.31, 11.12, 10.94, 10.75, 10.57, 10.38, 10.20, 10.03, 9.85],
    -1.1: [13.57, 13.35, 13.14, 12.92, 12.71, 12.51, 12.30, 12.10, 11.90, 11.70],
    -1.0: [15.87, 15.63, 15.39, 15.15, 14.92, 14.69, 14.46, 14.23, 14.01, 13.79],
    -0.9: [18.41, 18.14, 17.88, 17.62, 17.36, 17.11, 16.85, 16.60, 16.35, 16.11],
    -0.8: [21.19, 20.90, 20.61, 20.33, 20.05, 19.77, 19.49, 19.22, 18.94, 18.67],
    -0.7: [24.20, 23.89, 23.58, 23.27, 22.97, 22.66, 22.36, 22.07, 21.77, 21.48],
    -0.6: [27.43, 27.09, 26.76, 26.44, 26.11, 25.79, 25.46, 25.14, 24.83, 24.51],
    -0.5: [30.85, 30.50, 30.15, 29.81, 29.46, 29.12, 28.77, 28.43, 28.10, 27.76],
    -0.4: [34.46, 34.09, 33.72, 33.36, 33.00, 32.64, 32.28, 31.92, 31.56, 31.21],
    -0.3: [38.21, 37.83, 37.45, 37.07, 36.69, 36.32, 35.94, 35.57, 35.20, 34.83],
    -0.2: [42.07, 41.68, 41.29, 40.91, 40.52, 40.13, 39.74, 39.36, 38.97, 38.59],
    -0.1: [46.02, 45.62, 45.22, 44.83, 44.43, 44.04, 43.64, 43.25, 42.86, 42.47],
    0.0: [50.00, 50.40, 50.80, 51.20, 51.60, 51.99, 52.39, 52.79, 53.19, 53.59],
    0.1: [53.98, 54.38, 54.78, 55.17, 55.57, 55.96, 56.36, 56.75, 57.14, 57.54],
    0.2: [57.93, 58.32, 58.71, 59.10, 59.48, 59.87, 60.26, 60.64, 61.03, 61.41],
    0.3: [61.79, 62.17, 62.55, 62.93, 63.31, 63.68, 64.06, 64.43, 64.80, 65.17],
    0.4: [65.54, 65.91, 66.28, 66.64, 67.00, 67.36, 67.72, 68.08, 68.44, 68.79],
    0.5: [69.15, 69.50, 69.85, 70.19, 70.54, 70.88, 71.23, 71.57, 71.90, 72.24],
    0.6: [72.58, 72.91, 73.24, 73.57, 73.89, 74.22, 74.54, 74.86, 75.18, 75.49],
    0.7: [75.80, 76.12, 76.42, 76.73, 77.04, 77.34, 77.64, 77.94, 78.23, 78.52],
    0.8: [78.81, 79.10, 79.39, 79.67, 79.96, 80.23, 80.51, 80.79, 81.06, 81.33],
    0.9: [81.59, 81.86, 82.12, 82.38, 82.64, 82.89, 83.15, 83.40, 83.65, 83.89],
    1.0: [84.13, 84.38, 84.61, 84.85, 85.08, 85.31, 85.54, 85.77, 85.99, 86.21],
    1.1: [86.43, 86.65, 86.86, 87.08, 87.29, 87.49, 87.70, 87.90, 88.10, 88.30],
    1.2: [88.49, 88.69, 88.88, 89.07, 89.25, 89.44, 89.62, 89.80, 89.97, 90.15],
    1.3: [90.32, 90.49, 90.66, 90.82, 90.99, 91.15, 91.31, 91.47, 91.62, 91.77],
    1.4: [91.92, 92.07, 92.22, 92.36, 92.51, 92.65, 92.79, 92.92, 93.06, 93.19],
    1.5: [93.32, 93.45, 93.57, 93.70, 93.82, 93.94, 94.06, 94.18, 94.30, 94.41],
    1.6: [94.52, 94.63, 94.74, 94.85, 94.95, 95.05, 95.15, 95.25, 95.35, 95.45],
    1.7: [95.54, 95.64, 95.73, 95.82, 95.91, 95.99, 96.08, 96.16, 96.25, 96.33],
    1.8: [96.41, 96.49, 96.56, 96.64, 96.71, 96.78, 96.86, 96.93, 97.00, 97.06],
    1.9: [97.13, 97.19, 97.26, 97.32, 97.38, 97.44, 97.50, 97.56, 97.62, 97.67],
    2.0: [97.73, 97.78, 97.83, 97.88, 97.93, 97.98, 98.03, 98.08, 98.12, 98.17],
    2.1: [98.21, 98.26, 98.30, 98.34, 98.38, 98.42, 98.46, 98.50, 98.54, 98.57],
    2.2: [98.61, 98.65, 98.68, 98.71, 98.75, 98.78, 98.81, 98.84, 98.87, 98.90],
    2.3: [98.93, 98.96, 98.98, 99.01, 99.04, 99.06, 99.09, 99.11, 99.13, 99.16],
    2.4: [99.18, 99.20, 99.22, 99.25, 99.27, 99.29, 99.31, 99.32, 99.34, 99.36],
    2.5: [99.38, 99.40, 99.41, 99.43, 99.45, 99.46, 99.48, 99.49, 99.51, 99.52],
    2.6: [99.53, 99.55, 99.56, 99.57, 99.59, 99.60, 99.61, 99.62, 99.63, 99.64],
    2.7: [99.65, 99.66, 99.67, 99.68, 99.69, 99.70, 99.71, 99.72, 99.73, 99.74],
    2.8: [99.74, 99.75, 99.76, 99.77, 99.77, 99.78, 99.79, 99.80, 99.80, 99.81],
    2.9: [99.81, 99.82, 99.83, 99.83, 99.84, 99.84, 99.85, 99.85, 99.86, 99.86],
    3.0: [99.87, 99.87, 99.87, 99.88, 99.88, 99.89, 99.89, 99.89, 99.90, 99.90]
}
