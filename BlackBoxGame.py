# Author: Dan Glendon
# Date: 7/29/2020
# Description: Black Box Game class that represents the black box atom game as described
# in the readme. Fire rays into a box filled with atoms, then guess where the atoms are located.


class BlackBoxGame:

    def __init__(self, atom_locations):
        self._board = [["C", "BB", "BB", "BB", "BB", "BB", "BB", "BB", "BB", "C"],
                       ["BL", "S", "S", "S", "S", "S", "S", "S", "S", "BR"],
                       ["BL", "S", "S", "S", "S", "S", "S", "S", "S", "BR"],
                       ["BL", "S", "S", "S", "S", "S", "S", "S", "S", "BR"],
                       ["BL", "S", "S", "S", "S", "S", "S", "S", "S", "BR"],
                       ["BL", "S", "S", "S", "S", "S", "S", "S", "S", "BR"],
                       ["BL", "S", "S", "S", "S", "S", "S", "S", "S", "BR"],
                       ["BL", "S", "S", "S", "S", "S", "S", "S", "S", "BR"],
                       ["BL", "S", "S", "S", "S", "S", "S", "S", "S", "BR"],
                       ["C", "BT", "BT", "BT", "BT", "BT", "BT", "BT", "BT", "C"]]
        self._score = 25
        self._guessed = []
        self._count = len(atom_locations) - 1
        self._atoms = []
        while self._count >= 0:
            (space, spot) = atom_locations[self._count]
            self._atoms.append([space, spot])
            self._board[space][spot] = "A"
            self._count -= 1

    def get_board(self):
        """
        :return: The game board.
        """
        return self._board

    def shoot_ray(self, row, column):
        """
        Fires a ray, then hands off to other functions to determine where the ray goes.
        :param row: Row that the ray is fired from
        :param column: Column that the ray is fired from
        :return: False if an invalid square, none if hit. No return if a miss
        """

        if [row, column] not in self._guessed:
            self._guessed.append([row, column])
            self._score -= 1
        direction = self.find_border(row, column)
        # print(self._guessed)

        if direction is not False:
            while direction != 0:

                # print("Row is: " + str(row) + " | Column is: " + str(column))
                direction = self.check_reflect(direction, row, column)
                if direction == "W" or direction == "E":
                    column = self.make_move_column(direction, column)
                else:
                    row = self.make_move_row(direction, row)

                if self._board[row][column] == "A":
                    return None

                if self._board[row][column] != "S":
                    direction = 0

            current_space = (row, column)
            if [row, column] not in self._guessed:
                self._guessed.append([row, column])
                self._score -= 1
            return current_space
        else:
            return False

    def make_move_row(self, direction, row):
        """
        Moves the ray to another space.
        :param direction: Direction of the ray
        :param row: Current row of the ray
        :return:
        """
        if direction == "S":
            row += 1
            return row
        else:
            row -= 1
            return row

    def make_move_column(self, direction, column):
        """
        Moves the ray to another space.
        :param direction: Direction of the ray
        :param column: Current column of the ray
        :return:
        """
        if direction == "W":
            column -= 1
            return column
        else:
            column += 1
            return column

    def check_reflect(self, direction, row, column):
        """
        A method to show whether to reflect the ray or not.
        :param direction: Which way the ray was going
        :param row: The row the ray is currently in
        :param column: The column the ray is currently in
        :return:
        """
        try:
            if self._board[row + 1][column - 1] == "A":  # Bottom Left
                if direction == "S":
                    direction = "E"
                elif direction == "W":
                    direction = "N"
            elif self._board[row - 1][column - 1] == "A":  # Top Left
                if direction == "W":
                    direction = "S"
                elif direction == "N":
                    direction = "E"
            elif self._board[row + 1][column + 1] == "A":  # Bottom Right
                if direction == "E":
                    direction = "N"
                elif direction == "S":
                    direction = "W"
            elif self._board[row - 1][column + 1] == "A":  # Top Right
                if direction == "N":
                    direction = "W"
                elif direction == "E":
                    direction = "S"
            return direction
        except IndexError:
            return direction

    def guess_atom(self, row, column):
        """
        Allows the player to guess where an atom is.
        :param row: Row where the atom is
        :param column: Column where the atom is
        :return: True if hit, false if the player has guessed the location before.
        """
        if self._board[row][column] == "A":
            self._atoms.remove([row, column])
            return True
        elif [row, column] in self._guessed:
            return False
        else:
            self._score -= 5
            self._guessed.append([row, column])

    def get_score(self):
        """
        :return: The current score the player has.
        """
        return self._score

    def atoms_left(self):
        """
        :return: The amount of atoms left to find.
        """
        return self._atoms

    def find_border(self, row, column):
        """
        Designates what kind of border the player has chosen to fire from.
        :param row: Row the player is firing from.
        :param column: Column the player is firing from.
        :return: False if the player has chosen an invalid square, otherwise,
        returns the type of edge the player is firing from.
        """
        try:
            if self._board[row][column] == "BL":
                return "E"
            elif self._board[row][column] == "BR":
                return "W"
            elif self._board[row][column] == "BT":
                return "N"
            elif self._board[row][column] == "BB":
                return "S"
            else:
                return False
        except IndexError:
            return False
