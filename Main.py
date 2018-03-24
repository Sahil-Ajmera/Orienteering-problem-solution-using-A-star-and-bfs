"""
Author : Sahil Ajmera
Orienteering problem solution using A* and Bfs
"""
from PIL import Image, ImageDraw
import summer, winter, spring, fall
from math import *


class Orienteering:

    __slots__ = 'map', 'elevation_info', 'speed_through_different_paths', 'points_info', 'pixels', 'map_end_columns', \
                'map_end_rows', 'elevation_end_rows', 'elevation_end_columns','season'

    def __init__(self, map, elevation_file, course_file):
        """
        Initialization of various parameters
        :param map:
        :param elevation_file:
        """
        self.map = map
        self.speed_through_different_paths = {}
        self.elevation_info = []
        self.points_info = []

        # Image convert to RBG
        map_image = Image.open(self.map)
        map_image = map_image.convert('RGB')

        # Taking account of elevation of each point
        elevation_file = open(elevation_file)
        w, h = map_image.size
        self.map_end_rows, self.map_end_columns = w, h

        # Populate pixel list containing rgb values at each point
        pixels_object = map_image.load()
        self.pixels = pixels_object

        # Populate elevation list containing elevation at each point
        for lines in elevation_file:
            self.elevation_info.append(lines.split())

        # Elevation info resized with original dimensions
        self.elevation_info = [[self.elevation_info[j][i] for j in range(len(self.elevation_info))] for i in
                               range(len(self.elevation_info[0]))]
        self.elevation_end_rows = len(self.elevation_info)
        self.elevation_end_columns = len(self.elevation_info[0])

        # Reading the course file
        file = open(course_file)
        for lines in file:
            self.points_info.append(lines.split())

    def set_values_for_speed(self, season):
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
        self.speed_through_different_paths[(205, 0, 101)] = 0.1


    def calculateh(self,prevx, prevy, nextx, nexty):
        """
        Calculation of h value
        :param prevx:x value of Node whose h value to be calculated
        :param prevy:y value of Node whose h value to be calculated
        :param finalx:x value of Node where we want to reach
        :param finaly:y value of Node where we want to reach
        :return:
        """

        pixel_info = self.pixels
        elevation_info = self.elevation_info
        speed_info = self.speed_through_different_paths

        if (nextx == (prevx + 1) or nextx == (prevx - 1)) and nexty == prevy:
            dist = 10.29
        elif nextx == prevx and (nexty == (prevy + 1) or nexty == (prevy - 1)):
            dist = 7.55
        else:
            dist = sqrt(( (nextx-prevx)*( 10.29 ) )**2 + ((nexty-prevy)*( 7.55 ) )**2)

        dist = sqrt(dist**2 + (float(elevation_info[nextx][nexty])-float(elevation_info[prevx][prevy]))**2)
        speed = speed_info[pixel_info[prevx, prevy]]

        if float(elevation_info[nextx][nexty]) == float(elevation_info[prevx][prevy]):
            speed = speed

        elif float(elevation_info[nextx][nexty]) - float(elevation_info[prevx][prevy]) < 0:
            elevation_diff = abs(float(elevation_info[nextx][nexty]) - float(elevation_info[prevx][prevy]))
            speed = speed * (1 + elevation_diff/100)

        elif float(elevation_info[nextx][nexty]) - float(elevation_info[prevx][prevy]) > 0:
            elevation_diff = abs(float(elevation_info[nextx][nexty]) - float(elevation_info[prevx][prevy]))
            speed = speed * (1 - elevation_diff / 100)

        time = dist / speed
        return time

    def calculateg(self, nextx, nexty, prevx, prevy):
        """
        G calculating function
        :param nextx:x value of neighbouring pixel
        :param nexty:y value of neighbouring pixel
        :param prevx:x value of node that is being explored
        :param prevy:y value of node that is being explored
        :return: g value
        """
        pixel_info = self.pixels
        elevation_info = self.elevation_info
        speed_info = self.speed_through_different_paths

        if (nextx == (prevx + 1) or nextx == (prevx - 1)) and nexty == prevy:
            dist = 10.29
        elif nextx == prevx and (nexty == (prevy + 1) or nexty == (prevy - 1)):
            dist = 7.55
        else:
            dist = sqrt(((nextx-prevx)*(10.29))**2 + ((nexty-prevy)*(7.55))**2)

        dist = sqrt(dist**2 + (float(elevation_info[nextx][nexty])-float(elevation_info[prevx][prevy]))**2)
        speed = speed_info[pixel_info[prevx,prevy]]

        if float(elevation_info[nextx][nexty]) == float(elevation_info[prevx][prevy]):
            speed = speed

        elif float(elevation_info[nextx][nexty]) - float(elevation_info[prevx][prevy]) < 0:
            elevation_diff = abs(float(elevation_info[nextx][nexty]) - float(elevation_info[prevx][prevy]))
            speed = speed *(1+ elevation_diff/100)

        elif float(elevation_info[nextx][nexty]) - float(elevation_info[prevx][prevy]) > 0:
            elevation_diff = abs(float(elevation_info[nextx][nexty]) - float(elevation_info[prevx][prevy]))
            speed = speed * (1 - elevation_diff / 100)
        time = dist / speed
        return time

    def draw_line_on_image(self,map_image, final_path, color):
        im = Image.open(map_image)
        draw = ImageDraw.Draw(im)
        draw.line(final_path, fill=color, width = 1)
        im.show()

def main():
    """
    Main function
    :return:None
    """
    Map = input('Enter the map file\t')
    elevation_file = input('Enter the name of the elevation file\t')
    season = input('Enter season value\t')
    course_file = input('Enter the name of the course file\t')

    object_orien = Orienteering(Map, elevation_file, course_file)
    object_orien.set_values_for_speed(season)

    # List to keep track of final path
    final_path = []

    if season == 'summer'or season == 'Summer':

        summer_obj = summer.Summer()
        for i in range(len(object_orien.points_info)-1):
            start = object_orien.points_info[i]
            end = object_orien.points_info[i+1]
            startTouple = (int(start[0]), int(start[1]))
            endTouple = (int(end[0]), int(end[1]))
            final_path = final_path + summer_obj.search_for_path(object_orien, startTouple, endTouple)
        object_orien.draw_line_on_image(object_orien.map, final_path, (255, 0, 0))
        summer_obj.calulate_dist(object_orien,final_path)

    if season == "winter" or season == 'Winter':

        winter_obj = winter.Winter()
        water_edges_list, water_list = winter_obj.detect_water_edges(object_orien.pixels,
                                                                     object_orien.map_end_rows,
                                                                     object_orien.map_end_columns)
        winter_obj.water_bfs(object_orien.map,
                             water_edges_list,
                             object_orien.pixels,
                             object_orien.elevation_end_rows,
                             object_orien.elevation_end_columns)

        for i in range(len(object_orien.points_info)-1):
            start = object_orien.points_info[i]
            end = object_orien.points_info[i+1]
            startTouple = (int(start[0]), int(start[1]))
            endTouple = (int(end[0]), int(end[1]))
            final_path = final_path + winter_obj.search_for_path_winter(object_orien, startTouple, endTouple)
        object_orien.draw_line_on_image('terrain-winter', final_path, (255, 0, 0))
        winter_obj.calulate_dist(object_orien, final_path)

    if season == "fall" or season == 'Fall':
        fall_obj = fall.Fall()
        easy_movement_edge_list, easy_movement_list = fall_obj.detect_easy_movement(object_orien.pixels,
                                                                     object_orien.map_end_rows,
                                                                     object_orien.map_end_columns)
        fall_obj.bfs_fall(object_orien.map,
                          easy_movement_list,
                             easy_movement_edge_list,
                             object_orien.map_end_rows,
                             object_orien.map_end_columns,
                          object_orien.pixels)

        for i in range(len(object_orien.points_info) - 1):
            start = object_orien.points_info[i]
            end = object_orien.points_info[i + 1]
            startTouple = (int(start[0]), int(start[1]))
            endTouple = (int(end[0]), int(end[1]))
            final_path = final_path + fall_obj.search_for_path_fall(object_orien, startTouple, endTouple)
        object_orien.draw_line_on_image('terrain-fall', final_path, (255, 0, 0))
        fall_obj.calulate_dist(object_orien, final_path)

    if season == "spring" or season == "Spring":
        spring_obj = spring.Spring()
        water_edges_list, water_list = spring_obj.detect_water_edges(object_orien.pixels,
                                                                     object_orien.map_end_rows,
                                                                     object_orien.map_end_columns)
        spring_obj.bfs_spring(object_orien,
                              water_edges_list)

        for i in range(len(object_orien.points_info) - 1):
            start = object_orien.points_info[i]
            end = object_orien.points_info[i + 1]
            startTouple = (int(start[0]), int(start[1]))
            endTouple = (int(end[0]), int(end[1]))
            final_path = final_path + spring_obj.search_for_path_spring(object_orien, startTouple, endTouple)
        object_orien.draw_line_on_image('terrain-spring', final_path, (255, 0, 0))
        spring_obj.calulate_dist(object_orien, final_path)

if __name__ == "__main__":
    main()




