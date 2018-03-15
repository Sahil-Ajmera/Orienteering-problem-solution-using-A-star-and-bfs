from PIL import Image
from math import *
from queue import PriorityQueue

# Had to take z value as into consideration for calculation of distance

def readImageAndElevationFile(map, elevation_file):
    """

    :param map:
    :param elevation_file:
    :return:
    """
    # Image convert to RBG
    map_image = Image.open(map)
    map_image = map_image.convert('RGB')
    # Taking account of elevation of each point
    elevation_file = open(elevation_file)
    w, h = map_image.size
    i = -1
    elevation_info = []
    # Populate pixel list containing rgb values at each point
    pixels = list(map_image.getdata())
    pixels = [pixels[i * w:(i + 1) * w] for i in range(h)]
    i = 0
    # Populate elevation list containing elevation at each point
    for lines in elevation_file:
        elevation_info.append(lines.split())
    return map_image, elevation_info, pixels

def set_values_for_speed(speed_through_diff_paths):
    """
    
    :param time_to_go_through_diff_paths: 
    :return: 
    """""

    # Speed when going through different types of path

    speed_through_diff_paths[(248, 148, 18)] = 8
    speed_through_diff_paths[(255, 192, 0)] = 3
    speed_through_diff_paths[(255, 255, 255)] = 7
    speed_through_diff_paths[(2, 208, 60)] = 5
    speed_through_diff_paths[(2, 136, 40)] = 2
    speed_through_diff_paths[(5, 73, 24)] = 1
    speed_through_diff_paths[(0, 0, 255)] = 4
    speed_through_diff_paths[(71, 51, 3)] = 10
    speed_through_diff_paths[(0, 0, 0)] = 9
    speed_through_diff_paths[(205, 0, 101)] = 0



# Map = input('Enter the map file')
# elevation_file = input('Enter the name of the elevation file\t')
map_image, elevation_info, pixels = readImageAndElevationFile('terrain.png', 'mpp.txt')
