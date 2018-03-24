"""
Author : Sahil Ajmera
Fall class
"""
from PIL import Image,ImageDraw
import summer,winter
from math import *
from queue import Queue

from PriorityQueue import PQ
import operator
class Fall:
    __slots__ = 'path_color'

    def __init__(self):
        self.path_color = (0, 255, 0)

    def detect_easy_movement(self, pixels, max_rows, max_columns):
        """
        Detect the easy movement forest path and their edges
        :param map:Input map
        :return:List containing easy movement points on the map and list containing edges of easy movement areas
        """

        # List to store easy movement areas
        easy_movement_list = []


        # Typical neighbours for a point
        neighbours = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        # List to store edges of easy movement areas
        easy_movement_edge_list = []

        # List to store all points possible in the input image
        points_list = []
        for i in range(max_rows):
                for j in range(max_columns):
                    points_list.append((i, j))
                    # If the pixels values map to easy movement areas keep track in a separate list
                    if pixels[i, j] == (255, 255, 255):
                        easy_movement_list.append((i, j))

        # Finding neighbours of easy movement paths
        for points in points_list:
                for k in range(len(neighbours)):
                        pt_x_1 = points[0] + neighbours[k][0]
                        pt_y_1 = points[1] + neighbours[k][1]
                        if pt_x_1 >= 0 and\
                                        pt_x_1 < max_rows and\
                                        pt_y_1 >= 0 and\
                                        pt_y_1 < max_columns:
                            # If point in consideration is easy movement and neighbour is not easy movement ,
                            # neighbour is edge of easy movement paths
                            if pixels[points[0], points[1]] == (255, 255, 255) and pixels[pt_x_1, pt_y_1] != (255, 255, 255) and ((pt_x_1, pt_y_1) not in easy_movement_edge_list):
                                easy_movement_edge_list.append((pt_x_1, pt_y_1))

        return easy_movement_edge_list, easy_movement_list

    def bfs_fall(self, map, easy_movement_list, easy_movement_edge_list, max_rows, max_columns, pixels):
        """
        BFS for finding paths affected by falling of leaves apart from easy movement paths
        :param easy_movement_list: List containing points that are easy movement locations
        :param easy_movement_edge_list: List containing points that form edge of easy movement locations
        :return:None
        """
        neighbours = [(0, 1), (1, 0), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

        # Dictionary to keep track of explored neighbours
        explored_set = {}

        # For every edge point
        for points in easy_movement_edge_list:
            # Form a queue
            queue = []
            # Append the edge point
            queue.append((points[0], points[1]))

            # Exiting conditon 1
            while len(queue) != 0:

                # Fetch first element in the queue
                tuple_explored = queue.pop(0)

                # Check for looping only till nearest adjacent neighbours found
                if tuple_explored[0] == points[0] + 1 or \
                                tuple_explored[1] == points[1] + 1 or \
                                tuple_explored[0] == points[0] - 1 or \
                                tuple_explored[1] == points[1] - 1:
                    break
                # If fetched point already explored skip
                if tuple_explored not in explored_set:
                    explored_set[(tuple_explored[0], tuple_explored[1])] = 0
                else:
                    continue

                # Loop through all the neighbours of the fetched point
                for k in range(len(neighbours)):
                    x_value = tuple_explored[0] + neighbours[k][0]
                    y_value = tuple_explored[1] + neighbours[k][1]
                    if x_value >= 0 and\
                                    x_value < max_rows\
                            and\
                                    y_value >= 0 and\
                                    y_value < max_columns and\
                                    (x_value, y_value) not in queue and\
                                    (x_value, y_value) not in explored_set:
                        queue.append((x_value, y_value))

                        # If the neighbour is openLand or footpath it also gets covered during fall season
                        if pixels[x_value, y_value] == (0, 0, 0) or pixels[x_value, y_value] == (248, 148, 18):
                            easy_movement_list.append((x_value, y_value))
            # Pop remaining points in the queue
            while len(queue) != 0:
                tuple_explored = queue.pop(0)
                if tuple_explored[0] >= 0 and\
                                tuple_explored[0] < max_rows and\
                                tuple_explored[1] >= 0 and \
                                tuple_explored[1] < max_columns:
                    if pixels[tuple_explored[0], tuple_explored[1]] == (0, 0, 0) or pixels[
                        tuple_explored[0], tuple_explored[1]] == (248, 148, 18):
                        easy_movement_list.append((tuple_explored[0], tuple_explored[1]))

        self.draw_points_on_image_fall(map,easy_movement_list)

    def search_for_path_fall(self, object_orien, start, final):
        """
        Search for path during the fall season
        :param start:Start point
        :param final:Point to be reached
        :return:Final list containing the final path
        """


        object_orien.speed_through_different_paths[self.path_color] = 4

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
        f_value[start] = object_orien.calculateh(start[0], start[1], final[0], final[1])

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
            neighbour_list = self.getNeighbour_fall(int(point_explored[0]),
                                                    int(point_explored[1]),
                                                    object_orien.map_end_rows,
                                                    object_orien.map_end_columns,object_orien.pixels)

            # Loop through all the neighbours of fetched element
            for neighbour in neighbour_list:
                # Calculate g value for the neighbour
                calculated_g_value = cost_so_far[point_explored] + object_orien.calculateg(neighbour[0], neighbour[1],
                                                                                 point_explored[0],
                                                                                 point_explored[1])

                # Calculate h value for the neighbour
                calculated_h_value = object_orien.calculateh(neighbour[0], neighbour[1], final[0], final[1])

                # If neighbour not already in queue or neighbour calculated f value less than than its tracked f value till now
                # CHECK 7
                if neighbour not in cost_so_far or \
                                calculated_g_value + calculated_h_value < f_value[neighbour]:

                    cost_so_far[neighbour] = calculated_g_value
                    f_value[neighbour] = calculated_g_value + calculated_h_value
                    s.put(neighbour, calculated_g_value + calculated_h_value)
                    predecessor[neighbour] = point_explored

        return final_path_list

    def getNeighbour_fall(self, x, y, rows_max, columns_max, pixels):
        """
        List of neighbors of a particular x and y
        :param x:Input x
        :param y: Input y
        :param end_columns:Max value that can be attained by a y
        :param end_rows: Max value that can be attained by a x
        :return: list of neighbors of a particular x and y
        """
        list_of_neighbours = []
        end_columns = columns_max
        end_rows = rows_max

        neighbours = [(1, 0), (0, 1), (0, -1), (-1, 0)]

        for values in neighbours:
            pt_1_x = x + values[0]
            pt_1_y = y + values[1]
            if pt_1_x >= 0 and\
                            pt_1_x < end_rows and\
                            pt_1_y >= 0 and\
                            pt_1_y < end_columns and\
                            pixels[pt_1_x, pt_1_y] != (205, 0, 101) and\
                            pt_1_x < end_columns and\
                            pt_1_y < end_rows:
                list_of_neighbours.append((pt_1_x, pt_1_y))
        return list_of_neighbours


    def draw_points_on_image_fall(self,map,list):
        """
        Take a list of points and  plot it on a map and save the image
        :param map:Input map
        :param list:Input list of points
        :return:None
        """
        im = Image.open(map)
        draw = ImageDraw.Draw(im)
        for index in range(len(list)-1):
            # Paint points with sky blue color
            draw.point(list[index], fill=self.path_color)
        im.save('terrain-fall', "PNG")

    def calulate_dist(self, object_orien, final_path):
        """
        Calculates distance of final_path_found
        :param final_path:final path obtained by traversal
        :return:None
        """
        dist = 0
        for index in range(len(final_path) - 1):
            dist = dist + self.path_length(object_orien, final_path[index], final_path[index + 1])
        print("Distance:"+str(dist))

    def path_length(self, object_orien, start_point, end_point):
        """
        Returns the path_length
        :param object_orien:orienteering class object
        :param start_point:point x1,y1,z1
        :param end_point:point x2,y2,z2
        :return:distance between x1,y1,z1 and x2,y2,z2
        """
        return sqrt((start_point[0]-end_point[0])**2 +
                    (start_point[0]-end_point[1])**2 +
                    (float(object_orien.elevation_info[start_point[0]][start_point[1]]) - float(
                        object_orien.elevation_info[end_point[0]][end_point[1]])) ** 2)
