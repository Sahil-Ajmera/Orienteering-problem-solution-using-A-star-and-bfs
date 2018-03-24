"""
Author : Sahil Ajmera
Summer class
"""
from math import *
from PriorityQueue import PQ

class Summer:

    __slots__ = 'path_color'

    def __init__(self):
        self.path_color = (255, 0, 0)

    def getNeighbour(self, x, y, rows_max, columns_max, pixels):
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

        neighbours = [(1, 0), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1), (0, -1), (-1, 0)]

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
        f_value[start] = obj.calculateh(start[0], start[1], final[0], final[1])

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
            neighbour_list = self.getNeighbour(int(point_explored[0]),int(point_explored[1]),obj.elevation_end_rows,obj.elevation_end_columns, obj.pixels)

            # Loop through all the neighbours of fetched element
            for neighbour in neighbour_list:
                # Calculate g value for the neighbour
                calculated_g_value = cost_so_far[point_explored] + obj.calculateg(neighbour[0], neighbour[1],
                                                                                 point_explored[0],
                                                                                 point_explored[1])

                # Calculate h value for the neighbour
                calculated_h_value = obj.calculateh(neighbour[0], neighbour[1], final[0], final[1])

                # If neighbour not already in queue or neighbour calculated f value less than than its tracked f value till now

                if neighbour not in cost_so_far or \
                                calculated_g_value + calculated_h_value < f_value[neighbour]:

                    cost_so_far[neighbour] = calculated_g_value
                    f_value[neighbour] = calculated_g_value + calculated_h_value
                    s.put(neighbour, calculated_g_value + calculated_h_value)
                    predecessor[neighbour] = point_explored

        return final_path_list

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
                    (float(object_orien.elevation_info[start_point[0]][start_point[1]])-float(object_orien.elevation_info[end_point[0]][end_point[1]]))**2)
