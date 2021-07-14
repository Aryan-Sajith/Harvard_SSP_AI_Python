import sys

from crossword import *


# Helper method to remove value from queue
def queue_val_remover(queue):
    for val1, val2 in queue:
        queue.remove((val1, val2))
        return val1, val2


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # First we iterate through variables within self.domains
        for variable in self.domains:
            removable_words = set()

            # Here we check for bad values and add them to a set
            for word in self.domains[variable]:
                if len(word) != variable.length:
                    removable_words.add(word)

            # Here we remove the values that didn't satisfy unary constraints for each variable in domain
            for words in removable_words:
                self.domains[variable].remove(words)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Here we initialize important values
        revise = False
        overlap = self.crossword.overlaps[x, y]

        # Here we check if an overlap exists
        if overlap is not None:

            # A set of words that might cause issues
            removable_words = set()

            # Here we check values within the x domain and create comparison
            for word in self.domains[x]:
                overlapped_x = word[overlap[0]]
                overlapped_y = {words[overlap[1]] for words in self.domains[y]}

                # Here we check for conflict(and mark revision change if exists)
                if overlapped_x not in overlapped_y:
                    removable_words.add(word)
                    revise = True

            # Here we remove bad words from x domain
            for word in removable_words:
                self.domains[x].remove(word)

        # Here we return desired revision output
        return revise

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # First we deal with the case that arcs is None
        if arcs is None:
            # Here we establish a queue as the problem requires
            queue = []
            for val1 in self.crossword.variables:
                for val2 in self.crossword.neighbors(val1):
                    queue.append((val1, val2))

        # Otherwise arcs is already good enough
        else:
            queue = []
            for arc in arcs:
                queue.append(arc)

        # Here we work on enforcing arc consistency
        while queue is not None:
            arc = queue_val_remover(queue)
            if arc is not None:
                val1 = arc[0]
                val2 = arc[1]
                if self.revise(val1, val2):
                    # Here we check for empty domains
                    if len(self.domains[val1]) == 0:
                        return False
                    for val3 in self.crossword.neighbors(val1):
                        if val3 != val2:
                            queue.append((val3, val1))
            else:
                break

        # We return true here because we haven't arrived at an empty domain
        # after having enforced arc consistency
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # We check if each variable in assignment has a key and is a non-empty string
        if set(assignment.keys()) == self.crossword.variables and all(assignment.values()):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Here we check for word length issues
        for val1 in assignment:
            first_word = assignment[val1]
            if val1.length != len(first_word):
                return False

            # Here we check for word distinction
            for val2 in assignment:
                second_word = assignment[val2]
                if val1 != val2:
                    if first_word == second_word:
                        return False
                    # Here we check for overlapping issues
                    overlapping = self.crossword.overlaps[val1, val2]
                    if overlapping is not None:
                        x, y = overlapping
                        if first_word[x] != second_word[y]:
                            return False

        # Here we return True because consistency checks have been passed
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Here we establish important values and help count ruled out neighbors
        values = {}
        variables = self.domains[var]
        neighbors = self.crossword.neighbors(var)
        for variable in variables:
            if variable in assignment:
                continue
            else:
                counter = 0
                for neighbor in neighbors:
                    if variable in self.domains[neighbor]:
                        counter += 1
                values[variable] = counter

        # Here we return sorted values for domain ordering
        return sorted(values, key=lambda key: values[key])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Here we create and fill a list of variable choices
        potential_vars = []
        for variable in self.crossword.variables:
            if variable not in assignment:
                potential_vars.append([variable, len(self.domains[variable]), len(self.crossword.neighbors(variable))])

        # Here we sort potential variables by domain choices and then return desired variable
        if potential_vars:
            potential_vars.sort(key=lambda x: (x[1], -x[2]))
            return potential_vars[0][0]

        # Here we return None since no potential variable satisfy prior conditions
        return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # First we check if the assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        # Second we utilize the prior function to pick potential variables and follow the lecture pseudocode
        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            assignment[variable] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(variable)
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
