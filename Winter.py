
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
