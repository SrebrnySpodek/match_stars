import os

from match_starts_lib.match_starts import to_file_dict_of_nearest_stars
from match_starts_lib.match_starts import read_dict_with_nearest_stars
from match_starts_lib.match_starts import find_match

def main():

    path_with_stars_file = "./"
    # if there are no dictionary files then create
    list_with_star_dict = [file for file in os.listdir(path_with_stars_file) if file.endswith("nearest_star_dict")]
    if len(list_with_star_dict) == 0:
        to_file_dict_of_nearest_stars(path_with_stars_file)
    list_with_dict_files = [file for file in os.listdir(path_with_stars_file) if file.endswith(".nearest_star_dict")]
    list_with_dict = [read_dict_with_nearest_stars(file) for file in list_with_dict_files]
    dict_1 = list_with_dict[0]
    dict_2 = list_with_dict[1]

    # print matched stars inbetween different sets
    for star, list_of_nearest in dict_1.items():
        find_match(star, list_of_nearest, dict_2)


if __name__ == "__main__":
    main()


