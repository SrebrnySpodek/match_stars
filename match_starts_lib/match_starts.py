import numpy as np
import pickle
import os


def read_in_file_with_stars(file_name):
    """
    :param file_name:
    :return: list with (star_name, star_x, star_y)

    """
    f = open(file_name)
    list_with_stars = []
    for line_nr, line in enumerate(f):
        if line_nr > 2:     # omit first 3 lines in file (header)
            star_variable = line.split()
            star_name = star_variable[0]
            star_x_position = float(star_variable[1])
            star_y_position = float(star_variable[2])
            star_luminescence = float(star_variable[3])
            if star_luminescence < 15:   # only stars with luminescence <15
                list_with_stars.append((star_name, star_x_position, star_y_position))
    f.close()
    return list_with_stars


def projection(x, y):
    # 4 direction (not 2) because abs()
    direction = [(1, 1), (1, 0), (1, -1), (0, -1)]
    return np.array([abs(i[0] * x + i[1] * y) for i in direction])


def nearest_stars(the_star, list_of_stars):
    """

    :param the_star:
    :param list_of_stars:
    :return: list of nearest stars to "the star"
    """
    star_name, star_x_position, star_y_position = the_star[0], the_star[1], the_star[2]
    list_with_nearest_stars = []
    for _star_name, _star_x_position, _star_y_position in list_of_stars:
        distance_between_stars = ((star_x_position-_star_x_position)**2 + (star_y_position-_star_y_position)**2)**0.5

        proj_into = projection(star_x_position-_star_x_position, star_y_position-_star_y_position) / distance_between_stars

        list_with_nearest_stars.append((str(star_name)+"_with_"+str(_star_name),
                                        distance_between_stars,
                                        proj_into, _star_x_position, _star_y_position))
    list_with_nearest_stars.sort(key=lambda x: x[1])
    return list_with_nearest_stars


def dict_nearest_stars(list_with_stars, name_to_save, how_many_stars=5):
    """
    
    :param list_with_stars: 
    :param name_to_save: 
    :param how_many_stars:
    :return: 
    """
    dict_nearest_stars = {}
    for star in list_with_stars:
        aux_list_with_stars = list_with_stars.copy()
        aux_list_with_stars.remove(star)
        list_nearest_stars = nearest_stars(star, aux_list_with_stars)
        dist_to_nearest_star = list_nearest_stars[0][1]
        short_list_nearest = [(s[0], s[1]/dist_to_nearest_star, s[2]) for s in list_nearest_stars[:how_many_stars]]
        dict_nearest_stars[(star[0], star[1], star[2])] = short_list_nearest

    f = open(name_to_save, 'wb')
    pickle.dump(dict_nearest_stars, f)
    f.close()


def to_file_dict_of_nearest_stars(path_):
    for file in os.listdir(path_):
        if file.endswith(".out"):
            name = os.path.join(path_, file)
            print(name)
            list_with_stars = read_in_file_with_stars(name)
            dict_nearest_stars(list_with_stars, name.replace(".out", ".nearest_star_dict"))


def read_dict_with_nearest_stars(file_name):
    f = open(file_name, 'rb')
    stars_dict = pickle.load(f)
    f.close()
    return stars_dict


def check_if_match(dict_1, dict_2):
    # check if two stars with assigned list of nearest stars with features are equal
    # epsilon - how different can be
    epsilon = 0.01
    # array with difference in assigned directions
    o = np.array([abs(np.array(dict_1[i][2]) - np.array(dict_2[i][2])) for i in range(len(dict_2))])
    # sum within projection
    k = np.sort(np.sum(o, axis=1))
    # if 3 best gives difference smallest then epsilon return True
    # to be independent to scale /dist algorith won't work for low luminescent
    # if low luminescent better without /dist
    if abs(np.sum(k[:3])) > epsilon:
        return False
    else:
        return True


def find_match(star, list_with_nearest, dict_for_different_set):
    for _star, _star_nearest_list in dict_for_different_set.items():
        o = check_if_match(list_with_nearest, _star_nearest_list)
        if o:
            print(star, _star)
            print("it is a match")
            print()


if __name__ == "__main__":
    pass
