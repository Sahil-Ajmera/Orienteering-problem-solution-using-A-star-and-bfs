from PIL import Image,ImageDraw
import summer,winter
from math import *
from queue import Queue

from PriorityQueue import PQ
import operator

class Winter:
    __slots__ = 'path_color'

    def __init__(self):
        self.path_color = (178, 255, 255)

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
                        # If neighbour is not water then point is a edge
                        if pt_x_1 >= 0 and\
                                        pt_x_1 < max_rows and\
                                        pt_y_1 >= 0 and\
                                        pt_y_1 < max_columns:
                            if pixels[points[0],points[1]] == (0, 0, 255) and\
                                            pixels[pt_x_1,pt_y_1] != (0, 0, 255) and\
                                    ((pt_x_1, pt_y_1) not in water_edges):
                                water_edges.append((pt_x_1, pt_y_1))

        return water_edges, water_list

    def water_bfs(self, map, water_edges_list,pixels, max_rows, max_columns):
        """
        Bfs code to detect walkable ice region during winter
        :param water_edges_list:List containing edges of water
        :return:None
        """

        # 8 neighbours possible for a particular point
        neighbours = [(0, 1), (1, 0), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

        # List containing walkable ice path
        safe_water_list = []

        # For every point that is a water edge
        for points in water_edges_list:

            # List to keep the points
            queue = []

            # Dictionary keeping track of explored points
            explored_set = {}

            # Adding the initial point to queue
            queue.append((points[0], points[1]))

            # If the inital point is water add it to walkable ice path
            if pixels[points[0], points[1]] == (0, 0, 255):
                safe_water_list.append((points[0], points[1]))

            # BFS Implementation
            while len(queue) != 0:
                # Take the first element from the queue
                tuple_explored = queue.pop(0)

                # Check for whether 7 pixel depth reached or not
                if tuple_explored[0] == points[0] + 7 or \
                                tuple_explored[1] == points[1] + 7 or \
                                tuple_explored[0] == points[0] - 7 or \
                                tuple_explored[1] == points[1] - 7:
                    break

                # If the point already explored we dont need to explore it again
                if tuple_explored not in explored_set:
                    explored_set[(tuple_explored[0], tuple_explored[1])] = 0
                else:
                    continue

                # Loop through all neighbours of the point we are exploring
                for k in range(len(neighbours)):
                    x_value = tuple_explored[0] + neighbours[k][0]
                    y_value = tuple_explored[1] + neighbours[k][1]
                    # If the neighbour is valid and has not yet been explored or added to the queue add it
                    if x_value >= 0 and\
                                    x_value < max_rows and\
                                    y_value >= 0 and\
                                    y_value < max_columns and\
                                    (x_value,y_value) not in queue and\
                                    (x_value, y_value) not in explored_set:
                        queue.append((x_value,y_value))
                        if pixels[x_value, y_value] == (0, 0, 255):
                            safe_water_list.append((x_value, y_value))

            # Empty any remaining points present in the queue with same conditions
            while len(queue) != 0:
                tuple_explored = queue.pop(0)
                if tuple_explored[0] >= 0 and\
                                tuple_explored[0] < max_rows and\
                                tuple_explored[1] >= 0 and\
                                tuple_explored[1] < max_columns:
                    if pixels[tuple_explored[0], tuple_explored[1]] == (0, 0, 255):
                        safe_water_list.append((tuple_explored[0], tuple_explored[1]))
        self.draw_points_on_image(map, safe_water_list)

    def draw_points_on_image(self,map,list):
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
        im.save('terrain-winter', "PNG")


    def search_for_path_winter(self, object_orien, start, final):
        """
        Search for path during the winter season
        :param start:Start point
        :param final:Point to be reached
        :return:Final list containing the final path
        """
        object_orien.speed_through_different_paths[(178, 255, 255)] = 4
        object_orien.speed_through_different_paths[(0, 0, 255)] = 0.1

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
            neighbour_list = self.getNeighbour_winter(object_orien, int(point_explored[0]), int(point_explored[1]))

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

    def getNeighbour_winter(self, obj, x, y):
        """
        List of neighbors of a particular x and y
        :param x:Input x
        :param y: Input y
        :param end_columns:Max value that can be attained by a y
        :param end_rows: Max value that can be attained by a x
        :return: list of neighbors of a particular x and y
        """
        list_of_neighbours = []
        end_columns = obj.map_end_columns
        end_rows = obj.map_end_rows

        neighbours = [(1, 0), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1), (0, -1), (-1, 0)]

        for values in neighbours:
            pt_1_x = x + values[0]
            pt_1_y = y + values[1]
            if pt_1_x >= 0 and\
                            pt_1_x < end_rows and\
                            pt_1_y >= 0 and\
                            pt_1_y < end_columns and\
                            obj.pixels[
            pt_1_x, pt_1_y] != (205, 0, 101) and\
                            pt_1_x < end_columns and\
                            pt_1_y < end_rows and\
                            obj.pixels[
            pt_1_x, pt_1_y] != (0, 0, 255):
                list_of_neighbours.append((pt_1_x, pt_1_y))

        return list_of_neighbours


