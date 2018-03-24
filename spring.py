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

class Spring:
    __slots__ = 'path_color'

    def __init__(self):
        self.path_color = (255, 206, 145)

    def detect_water_edges(self, pixels, max_rows, max_columns):
        """
        Detect water and its edges in the map
        :param image:The input image
        :return:The list containing water pixels and list containing points denoting boundary of water
        """
        # List to store water pixels
        water_list = []
        neighbours = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        points_list = []
        water_edges = []

        # Store points and water pixels
        for i in range(max_rows):
                for j in range(max_columns):
                    points_list.append((i, j))
                    if pixels[i, j] == (0, 0, 255):
                        water_list.append((i, j))

        # Detect water edges
        for points in points_list:
                for k in range(len(neighbours)):
                        pt_x_1 = points[0] + neighbours[k][0]
                        pt_y_1 = points[1] + neighbours[k][1]
                        # If point in consideration is water and neighbour is not water then neighbour is a edge
                        if pt_x_1 >= 0 and\
                                        pt_x_1 < max_rows and\
                                        pt_y_1 >= 0 and\
                                        pt_y_1 < max_columns:
                            if pixels[points[0], points[1]] == (0, 0, 255) and\
                                            pixels[pt_x_1, pt_y_1] != (0, 0, 255) and\
                                    ((pt_x_1, pt_y_1) not in water_edges):
                                water_edges.append((pt_x_1, pt_y_1))

        return water_edges, water_list


    def draw_points_on_image_spring(self, map, list):
        """
        Placing points with specific oolors
        :param list:list containing point
        :return:None
        """
        im = Image.open(map)
        draw = ImageDraw.Draw(im)
        for index in range(len(list) - 1):
            draw.point(list[index], fill=self.path_color)
        im.save('terrain-spring', "PNG")

    def bfs_spring(self, object_orien, water_edge_list):
        """
        Explore all the regions that will be underwater during Spring season
        :param object_orien:Main class object passed to access parameters
        :param water_edge_list:List containing water edge points
        :return:None
        """

        # Neighbours list for computing neighbours of a particular point
        neighbours = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        # List to contain points that will be underwater
        mud_list = []

        # List to keep track of points that are explored
        explored_set = {}

        # For every point that is a water edge point
        for points in water_edge_list:
                # Store the elevation of the point
                parent_elevation = float(object_orien.elevation_info[points[0]][points[1]])

                # Create a queue to store and retrieve points
                queue = []

                # Append the point to the queue
                queue.append((points[0], points[1]))

                # Exiting condition 1
                while len(queue) != 0:
                    # Pop the first element from the queue
                    tuple_explored = queue.pop(0)

                    # Check to see if we have traversed for 15 depth for the element(point)
                    if tuple_explored[0] == points[0] + 15 or \
                                    tuple_explored[1] == points[1] + 15 or \
                                    tuple_explored[0] == points[0] - 15 or \
                                    tuple_explored[1] == points[1] - 15:
                        break

                    # If the element(point) has already been explored dont explore it again
                    if tuple_explored not in explored_set:
                        explored_set[(tuple_explored[0], tuple_explored[1])] = 0
                    else:
                        continue

                    # Loop through all the neighbours of the element(point)
                    for k in range(len(neighbours)):
                        x_value = tuple_explored[0] + neighbours[k][0]
                        y_value = tuple_explored[1] + neighbours[k][1]

                        # For each neighbour check if its valid and its elevation is within 1 m of the point
                        # we are exploring
                        if x_value >= 0 and \
                                        x_value < object_orien.map_end_rows and\
                                        y_value >= 0 and \
                                        y_value < object_orien.map_end_columns and\
                                        (x_value,y_value) not in queue and \
                                        (x_value,y_value) not in explored_set and \
                                (not (float(object_orien.elevation_info[x_value][y_value]) - parent_elevation > 1)) and object_orien.pixels[x_value,y_value] !=(205,0,101) :
                            queue.append((x_value,y_value))
                            # If the neighbour satisfies above conditions check if its non-water
                            if object_orien.pixels[x_value, y_value] != (0, 0, 255):

                                # The neighbour will now be mud if it satisfies the previous conditions
                                mud_list.append((x_value, y_value))
                # Pop remaining elements out of the queue and check the same conditions as above
                while len(queue) !=0:
                    tuple_explored = queue.pop(0)

                    if tuple_explored[0] >= 0 and\
                                    tuple_explored[0] < object_orien.map_end_rows and \
                                    tuple_explored[1] >= 0 and \
                                    tuple_explored[1] < object_orien.map_end_columns and\
                            (not (float(object_orien.elevation_info[tuple_explored[0]][tuple_explored[1]]) - parent_elevation >= 1)):
                        if object_orien.pixels[tuple_explored[0], tuple_explored[1]] != (0, 0, 255):

                            mud_list.append((tuple_explored[0], tuple_explored[1]))
        self.draw_points_on_image_spring(object_orien.map, mud_list)

    def search_for_path_spring(self, object_orien, start, final):
        """
        Final path calculation during spring season
        :param start:Start point for calculation
        :param final:End point for calculation
        :return:Final path from start to end based on A* search performed
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

                # Backtracking to find the actual path from the start point to the final point
                curr = final
                while curr != start:
                    final_path_list.insert(0, curr)
                    curr = predecessor[curr]
                final_path_list.insert(0, start)
                break

            # Get the neighbours of the element fetched from the priority queue
            neighbour_list = self.getNeighbour_spring(object_orien, int(point_explored[0]), int(point_explored[1]))

            # Loop through all the neighbours of fetched element
            for neighbour in neighbour_list:
                # Calculate g value for the neighbour
                calculated_g_value = cost_so_far[point_explored] + object_orien.calculateg(neighbour[0], neighbour[1],
                                                                                           point_explored[0],
                                                                                           point_explored[1])

                # Calculate h value for the neighbour
                calculated_h_value = object_orien.calculateh(neighbour[0], neighbour[1], final[0], final[1])

                # If neighbour not already in queue or neighbour calculated f value less than than its tracked f value till now

                if neighbour not in cost_so_far or \
                                        calculated_g_value + calculated_h_value < f_value[neighbour]:
                    cost_so_far[neighbour] = calculated_g_value
                    f_value[neighbour] = calculated_g_value + calculated_h_value
                    s.put(neighbour, calculated_g_value + calculated_h_value)
                    predecessor[neighbour] = point_explored

        return final_path_list

    def getNeighbour_spring(self, object_orien, x, y):
        """
        List of neighbors of a particular x and y
        :param x:Input x
        :param y: Input y
        :param end_columns:Max value that can be attained by a y
        :param end_rows: Max value that can be attained by a x
        :return: list of neighbors of a particular x and y
        """
        list_of_neighbours = []
        end_columns = object_orien.map_end_columns
        end_rows = object_orien.map_end_rows
        pixels = object_orien.pixels

        neighbours = [(1, 0), (0, 1),(0, -1), (-1, 0)]

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
