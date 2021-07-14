import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # Here we check for equality of cells and count, meaning all cells in set are mines
        if len(self.cells) == self.count:
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # Here we check for a count of 0, meaning that all cells in set are safe
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Here we establish an updated set of cells or decrease count if we find the mine
        updated_cells = set()
        for value in self.cells:
            if value != cell:
                updated_cells.add(value)
            else:
                self.count -= 1

        # Here we update the new cells list
        self.cells = updated_cells

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Here we establish an updated set of cells(no mines so count is unchanged)
        updated_cells = set()
        for value in self.cells:
            if value != cell:
                updated_cells.add(value)

            # Here we update the cells list
            self.cells = updated_cells


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Here we mark cell as safe and add to completed moves set
        self.mark_safe(cell)
        self.moves_made.add(cell)

        # Here we add a new sentence to the AI's knowledge based on finding neighbors
        x, y = cell
        neighbors = []
        count_temp = count
        for row in range(x - 1, x + 2):
            for col in range(y - 1, y + 2):
                if (0 <= row < self.height) \
                        and (0 <= col < self.width) \
                        and (row, col) != cell \
                        and (row, col) not in self.safes \
                        and (row, col) not in self.mines:
                    neighbors.append((row, col))
                if (row, col) in self.mines:
                    count_temp -= 1
        sentence = Sentence(neighbors, count_temp)
        self.knowledge.append(sentence)

        # Here we make inferences based on the knowledge base
        inferences = []
        for sentence_a in self.knowledge:
            # Here we check if the sentences(during iteration) are the same and move on
            if sentence_a == sentence:
                continue
            # Here we check for a subset by comparing two sentences one way
            elif sentence.cells.issubset(sentence_a.cells):
                cell_difference = sentence_a.cells - sentence.cells
                # Here we check for safes
                if sentence_a.count == sentence.count:
                    for safe in cell_difference:
                        self.mark_safe(safe)
                # Here we check for mines
                elif len(cell_difference) == sentence_a.count - sentence.count:
                    for mine in cell_difference:
                        self.mark_mine(mine)
                # If mines and safes have passed, then we add an inference
                else:
                    inferences.append(
                        Sentence(cell_difference, sentence_a.count - sentence.count)
                    )
            # Here we check for subset by checking two sentences the other way around
            elif sentence_a.cells.issubset(sentence.cells):
                cell_difference = sentence.cells - sentence_a.cells
                # Here we check for safes
                if sentence_a.count == sentence.count:
                    for safeFound in cell_difference:
                        self.mark_safe(safeFound)
                # Here we check for mines
                elif len(cell_difference) == sentence.count - sentence_a.count:
                    for mineFound in cell_difference:
                        self.mark_mine(mineFound)
                # If mines and safes have passed, then we add an inference
                else:
                    inferences.append(
                        Sentence(cell_difference, sentence.count - sentence_a.count)
                    )
        # Here we add inferences gathered to the knowledge base
        self.knowledge.extend(inferences)

        # Here we remove sentences that repeat
        sentences_unrepeated = []
        for sentence in self.knowledge:
            if sentence not in sentences_unrepeated:
                sentences_unrepeated.append(sentence)
        self.knowledge = sentences_unrepeated

        # Here we remove sentences that already provide information regarding mines/safes
        sentences_useful = []
        for sentence in self.knowledge:
            sentences_useful.append(sentence)
            # Here we check if the sentence provides mine information(and remove)
            if sentence.known_mines():
                for mine in sentence.known_mines():
                    self.mark_mine(mine)
                sentences_useful.remove(sentence)
            # Here we check if the sentence provides safe information(and remove)
            elif sentence.known_safes():
                for safe in sentence.known_safes():
                    self.mark_safe(safe)
                sentences_useful.remove(sentence)
        self.knowledge = sentences_useful

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Here we check if a move within the safe cells and not already made
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

        # here we couldn't find a move that was safe, so we return none
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Here we establish moves on the board
        viable_moves = set()
        for x in range(self.height):
            for y in range(self.width):
                if (x, y) not in self.mines and (x, y) not in self.moves_made:
                    viable_moves.add((x, y))
        # Here we return none if no viable moves exist
        if len(viable_moves) == 0:
            return None
        # Here we use the random library to pick a random tuple/move from the viable ones
        move = random.choice(tuple(viable_moves))
        return move
