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
