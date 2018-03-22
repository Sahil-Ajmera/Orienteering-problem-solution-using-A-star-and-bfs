"""
Author : Sahil Ajmera
Orienteering problem solution using A* and Bfs
CHECKS - 7
"""
from PIL import Image,ImageDraw
import summer
from math import *
from queue import Queue

from PriorityQueue import PQ
import operator


class Orienteering:

    __slots__ = 'map', 'elevation_info', 'speed_through_different_paths', 'points_info', 'pixels', 'map_end_columns', \
                'map_end_rows', 'elevation_end_rows', 'elevation_end_columns','season'

    def __init__(self, map, elevation_file, season , course_file):
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

    def set_values_for_speed(self,season):
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
        # CHECK 1
        self.speed_through_different_paths[(205, 0, 101)] = 0.1

        # CHECK 2
        if season == "winter":
            self.speed_through_different_paths[(0, 0, 200)] = 10

        # CHECK 3
        if season == "fall":
            self.speed_through_different_paths[(0, 0, 200)] = 10

        # CHECK 4
        if season == "spring":
            self.speed_through_different_paths[(0,0,0)] = 10


    def search_for_path(self, obj, start,final):
        """
        Final path calculating function
        :param start:Start point
        :param final:Point to be reached
        :return:Final path from Start to final
        """

        # To keep track of g values
        cost_so_far = {}

        # Priority queue initialization
        s = PQ()

        # To keep track of predecessors to help in backtracking
        predecessor = {}

        # Insert start point into the priority queue
        s.put(start, 0)

        # g value of start is 0
        cost_so_far[start] = 0

        # f value of start is 0 + h(start)
        f_value = {}
        f_value[start] = self.calculateh(start[0], start[1], final[0], final[1])

        final_path_list = []

        # Exiting condition when no path is found
        while not s.empty():
            # Fetch the element in the priority queue with the lowest g(n) + h(n) value
            point_explored = s.get()

            # To keep the final path
            final_path_list = []

            # Exiting condition for when there exists a path between the start point and end point supplied to this function
            if point_explored == final:

                #Backtracking to find the actual path from the start point to the final point
                curr = final
                while curr != start:
                    final_path_list.insert(0, curr)
                    curr = predecessor[curr]
                final_path_list.insert(0, start)
                break


            # Get the neighbours of the element fetched from the priority queue
            neighbour_list = obj.getNeighbour(int(point_explored[0]),int(point_explored[1]),self.elevation_end_rows,self.elevation_end_columns, self.pixels)

            # Loop through all the neighbours of fetched element
            for neighbour in neighbour_list:
                # Calculate g value for the neighbour
                calculated_g_value = cost_so_far[point_explored] + self.calculateg(neighbour[0], neighbour[1],
                                                                                 point_explored[0],
                                                                                 point_explored[1])

                # Calculate h value for the neighbour
                calculated_h_value = self.calculateh(neighbour[0], neighbour[1], final[0], final[1])

                # If neighbour not already in queue or neighbour calculated f value less than than its tracked f value till now
                # CHECK 7
                if neighbour not in cost_so_far or \
                                calculated_g_value + calculated_h_value < f_value[neighbour]:

                    cost_so_far[neighbour] = calculated_g_value
                    f_value[neighbour] = calculated_g_value + calculated_h_value
                    s.put(neighbour, calculated_g_value + calculated_h_value)
                    predecessor[neighbour] = point_explored

        return final_path_list

    def calculateh(self,prevx, prevy, nextx, nexty):
        """
        Calculation of h value
        :param prevx:x value of Node whose h value to be calculated
        :param starty:y value of Node whose h value to be calculated
        :param finalx:x value of Node where we want to reach
        :param finaly:y value of Node where we want to reach
        :return:
        """
        pixel_info = self.pixels
        elevation_info = self.elevation_info
        speed_info = self.speed_through_different_paths

        if (nextx == (prevx + 1) or nextx == (prevx - 1)) and nexty == prevy:
            dist = 7.55
        elif nextx == prevx and (nexty == (prevy + 1) or nexty == (prevy - 1)):
            dist = 10.29
        else:
            dist = sqrt(((7.55))**2 + ((10.29))**2)

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

    def calculateg(self,nextx, nexty, prevx, prevy):
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
            dist = 7.55
        elif nextx == prevx and (nexty == (prevy + 1) or nexty == (prevy - 1)):
            dist = 10.29
        else:
            dist = sqrt(((7.55))**2 + ((10.29))**2)

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

    object_orien = Orienteering(Map, elevation_file, season, course_file)
    object_orien.set_values_for_speed(season)

    # List to keep track of final path
    final_path = []

    if season == 'summer':

        summer_obj = summer.Summer()
        for i in range(len(object_orien.points_info)-1):
            start = object_orien.points_info[i]
            end = object_orien.points_info[i+1]
            startTouple = (int(start[0]), int(start[1]))
            endTouple = (int(end[0]), int(end[1]))
            final_path = final_path + object_orien.search_for_path(summer_obj, startTouple, endTouple)
        object_orien.draw_line_on_image(object_orien.map, final_path, (255, 0, 0))
    
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
            final_path = final_path + winter_obj.search_for_path_winter(object_orien,startTouple, endTouple)
        object_orien.draw_line_on_image('terrain-winter', final_path, (255, 0, 0))

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
        object_orien.draw_line_on_image('terrain-winter', final_path, (255, 0, 0))
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

if __name__ == "__main__":
    main()

    
