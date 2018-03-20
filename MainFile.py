"""
Author : Sahil Ajmera
Orienteering problem solution using A* and Bfs
"""
from PIL import Image, ImageDraw
from math import *
from queue import Queue

from PriorityQueue import PQ
import operator


# Priority queue not working
# h(n) not in the same terms as g(n)

class Orienteering:
    __slots__ = 'map', 'elevation_info', 'speed_through_different_paths', 'points_info', 'pixels', 'map_end_columns', 'map_end_rows'

    def __init__(self, map):
        self.map = map
        self.speed_through_different_paths = {}
        self.elevation_info = []
        self.points_info = []

    def readImageAndElevationFile(self, elevation_file):
        """
        Reading the image file and elevation file along with pixel values(RGB) at various pixels
        :param map:Input given the program
        :param elevation_file:Elevation file given for elevation info at various points
        :return:Modified image , elevation_info list containing elevations , pixels containing RGB values
        """
        # Image convert to RBG
        map_image = Image.open(self.map)
        map_image = map_image.convert('RGB')
        # Taking account of elevation of each point
        elevation_file = open(elevation_file)
        w, h = map_image.size
        self.map_end_rows, self.map_end_columns = w, h
        i = -1
        # self.pixels = [[0]*w]*h
        # Populate pixel list containing rgb values at each point
        # print(map_image.load)
        pixels_object = map_image.load()
        self.pixels = pixels_object
        # Populate elevation list containing elevation at each point
        for lines in elevation_file:
            self.elevation_info.append(lines.split())

    def set_values_for_speed(self):
        """
        Setting predefined values for speed through different terrains based on rbg value of terrain
        :param speed_through_diff_paths: Dictionary to keep speed mapped to terrain
        :return: dictionary after filling in values
        """""

        # Speed when going through different types of path
        # Open Land
        self.speed_through_different_paths[(248, 148, 18)] = 8

        # Rough Meadow
        self.speed_through_different_paths[(255, 192, 0)] = 3

        # Easy movement forest
        self.speed_through_different_paths[(255, 255, 255)] = 7

        # Slow run forest
        self.speed_through_different_paths[(2, 208, 60)] = 5

        # Walk forest
        self.speed_through_different_paths[(2, 136, 40)] = 2

        # Impassible vegetation
        self.speed_through_different_paths[(5, 73, 24)] = 1

        # Lake / Swamp / Marsh
        self.speed_through_different_paths[(0, 0, 255)] = 4

        # Paved road
        self.speed_through_different_paths[(71, 51, 3)] = 10

        # Foot path
        self.speed_through_different_paths[(0, 0, 0)] = 9

        # Out of Bounds
        self.speed_through_different_paths[(205, 0, 101)] = 0

    def getNeighbour(self, x, y):
        """
        List of neighbors of a particular x and y
        :param x:Input x
        :param y: Input y
        :param end_columns:Max value that can be attained by a y
        :param end_rows: Max value that can be attained by a x
        :return: list of neighbors of a particular x and y
        """
        list_of_neighbours = []
        end_columns = self.map_end_columns
        end_rows = self.map_end_rows
        # point below (x,y)
        pt_1_x = x + 1
        pt_1_y = y
        # Extra conditions
        if pt_1_x >= 0 and pt_1_x < end_rows and pt_1_y >= 0 and pt_1_y < end_columns and self.pixels[
            pt_1_x, pt_1_y] != (205, 0, 101) and pt_1_x < end_columns and pt_1_y < end_rows:
            list_of_neighbours.append((pt_1_x, pt_1_y))

        # point right of (x,y)
        pt_1_x = x
        pt_1_y = y + 1
        if pt_1_x >= 0 and pt_1_x < end_rows and pt_1_y >= 0 and pt_1_y < end_columns and self.pixels[
            pt_1_x, pt_1_y] != (205, 0, 101) and pt_1_x < end_columns and pt_1_y < end_rows:
            list_of_neighbours.append((pt_1_x, pt_1_y))

        # point above  (x,y)
        pt_1_x = x - 1
        pt_1_y = y
        if pt_1_x >= 0 and pt_1_x < end_rows and pt_1_y >= 0 and pt_1_y < end_columns and self.pixels[
            pt_1_x, pt_1_y] != (205, 0, 101) and pt_1_x < end_columns and pt_1_y < end_rows:
            list_of_neighbours.append((pt_1_x, pt_1_y))

        # point to the left of (x,y)
        pt_1_x = x
        pt_1_y = y - 1
        if pt_1_x >= 0 and pt_1_x < end_rows and pt_1_y >= 0 and pt_1_y < end_columns and self.pixels[
            pt_1_x, pt_1_y] != (205, 0, 101) and pt_1_x < end_columns and pt_1_y < end_rows:
            list_of_neighbours.append((pt_1_x, pt_1_y))

        # point to the bottom left of (x,y)
        pt_1_x = x + 1
        pt_1_y = y - 1
        if pt_1_x >= 0 and pt_1_x < end_rows and pt_1_y >= 0 and pt_1_y < end_columns and self.pixels[
            pt_1_x, pt_1_y] != (205, 0, 101) and pt_1_x < end_columns and pt_1_y < end_rows:
            list_of_neighbours.append((pt_1_x, pt_1_y))

        # point to the top right of (x,y)
        pt_1_x = x - 1
        pt_1_y = y + 1
        if pt_1_x >= 0 and pt_1_x < end_rows and pt_1_y >= 0 and pt_1_y < end_columns and self.pixels[
            pt_1_x, pt_1_y] != (205, 0, 101) and pt_1_x < end_columns and pt_1_y < end_rows:
            list_of_neighbours.append((pt_1_x, pt_1_y))

        # point to the top left of (x,y)
        pt_1_x = x - 1
        pt_1_y = y - 1
        if pt_1_x >= 0 and pt_1_x < end_rows and pt_1_y >= 0 and pt_1_y < end_columns and self.pixels[
            pt_1_x, pt_1_y] != (205, 0, 101) and pt_1_x < end_columns and pt_1_y < end_rows:
            list_of_neighbours.append((pt_1_x, pt_1_y))

        # point to the bottom right of (x,y)
        pt_1_x = x + 1
        pt_1_y = y + 1
        if pt_1_x >= 0 and pt_1_x < end_rows and pt_1_y >= 0 and pt_1_y < end_columns and self.pixels[
            pt_1_x, pt_1_y] != (205, 0, 101) and pt_1_x < end_columns and pt_1_y < end_rows:
            list_of_neighbours.append((pt_1_x, pt_1_y))

        return list_of_neighbours


    def read_points_to_visit(self, points_to_visit):
        """
        Reading the course file to note the control points and final destination to be visited
        :param points_to_visit:file containing the control points and final destination to be visited
        :return:List of points in a list
        """
        file = open(points_to_visit)
        for lines in file:
            self.points_info.append(lines.split())
        return self.points_info


def main():
    # Map = input('Enter the map file')
    # elevation_file = input('Enter the name of the elevation file\t')
    object_orien = Orienteering('terrain.png')
    object_orien.readImageAndElevationFile('mpp.txt')
    object_orien.set_values_for_speed()
    # points_to_visit = input('Enter the file containing points to visit')
    object_orien.points_info = object_orien.read_points_to_visit('red.txt')
    startx = int(object_orien.points_info[0][0])
    starty = int(object_orien.points_info[0][1])

    # Check
    im = 'terrain.png'
    dist = 0
    final_path = []

    object_orien.draw_winter()
    # water_edges_list,water_list=object_orien.detect_water_edges('terrain.png')
    # object_orien.water_bfs(water_edges_list)


    # for i in range(len(object_orien.points_info)-1):
    #     start = object_orien.points_info[i]
    #     end = object_orien.points_info[i+1]
    #     startTouple = (int(start[0]),int(start[1]))
    #     endTouple = (int(end[0]),int(end[1]))
    #     #print('start',startTouple)
    # print('end',endTouple)
    #    final_path = final_path + object_orien.search_for_path(startTouple,endTouple)
    # print(final_path)

    # for index in range(len(final_path) - 1):
    #      dist = dist + object_orien.path_length(int(final_path[index][0]), int(final_path[index][1]), int(final_path[index + 1][0]),int(final_path[index + 1][1]))
    #      print(dist)
    # im = object_orien.draw_line_on_image(im, final_path)
    # im.show()


if __name__ == "__main__":
    main()




