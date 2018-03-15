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



# Map = input('Enter the map file')
# elevation_file = input('Enter the name of the elevation file\t')
map_image, elevation_info, pixels = readImageAndElevationFile('terrain.png', 'mpp.txt')
