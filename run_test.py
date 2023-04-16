import unittest
import os

from match_starts_lib.match_starts import to_file_dict_of_nearest_stars
from match_starts_lib.match_starts import read_dict_with_nearest_stars
from match_starts_lib.match_starts import find_match


class TestStringMethods(unittest.TestCase):

    def test_match(self):
        file_name_1 = "SMC24_131127_1_J.out"
        file_name_2 = "SMC24_131127_1_K.out"
        file_dict_name_1 = file_name_1.replace(".out", ".nearest_star_dict")
        file_dict_name_2 = file_name_2.replace(".out", ".nearest_star_dict")
        if not os.path.exists(file_dict_name_1):
            to_file_dict_of_nearest_stars(file_name_1)
        if not os.path.exists(file_dict_name_2):
            to_file_dict_of_nearest_stars(file_name_2)

        dict_1 = read_dict_with_nearest_stars(file_dict_name_1)
        dict_2 = read_dict_with_nearest_stars(file_dict_name_2)
        list_with_matched_stars = []
        for star, list_of_nearest in dict_1.items():
            list_with_matched_stars.append(find_match(star, list_of_nearest, dict_2))
        correct = [(6, 8), (2, 5), (22, 47)]
        answer = [(float(s[0][0]), float(s[1][0])) for s in list_with_matched_stars if not(s is None)]
        for good_match in correct:
            self.assertIn(good_match, answer)

if __name__ == '__main__':
    unittest.main()
