import numpy as np


class Vector:
    """ implementation of Eucledian vector"""

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __str__(self):
        return "(" + str(self.x) + " " + str(self.y) + ")"

    # equivalent of Vector(0.0, 0.0)
    def nul(self):
        self.x, self.y = 0.0, 0.0

    # calculates the Eucledian distance between 2 vectors
    def dist(self, other):
        x_dist = self.x - other.x
        y_dist = self.y - other.y
        return np.sqrt(x_dist * x_dist + y_dist * y_dist)

    # transforms the vector to a tuple containing integer values
    # the offset is added to the components of the vector
    def tuple_int(self, offset=0.0):
        return int(self.x + offset), int(self.y + offset)

    # creates a vector with random initial values
    @staticmethod
    def random():
        return Vector(np.random.uniform(0, 2.0) - 1.0, np.random.uniform(0, 2.0) - 1.0)


class Obstacle:
    """ the Obstacle is a rectangle whit which the Rocket can collide
        self.a (type Vector) - contains the point for the upper left corner of the rectangle
        self.b (type Vector) - contains the point for the lower right corner of the rectangle
    """

    def __init__(self, x1, y1, x2, y2):
        self.a = Vector(x1, y1)
        self.b = Vector(x2, y2)

    # return true if the rocket's position is inside the obstacle's rectangle
    def do_collide(self, rocket):
        return self.a.x < rocket.location.x and self.a.y < rocket.location.y and \
                self.b.x > rocket.location.x and self.b.y > rocket.location.y

    # transforms the vector to a tuple containing integer values
    # the offset is added to the components of the vector
    def tuple_int(self, offset):
        return self.a.tuple_int(offset), self.b.tuple_int(offset)


class Rocket:

    def __init__(self, length):

        self.location = Vector()
        self.acceleration = Vector()
        self.velocity = Vector()

        self.forces = []
        self.length = length

        # this flag is set to False after the rocket did collide with an obstacle
        self.is_alive = True

        for i in range(0, length):
            self.forces.append(Vector.random())

    # calculates the fitness of a Rocket
    # it is recommended to be called after every force vector was added to the rocket
    def fitness(self, target):

        # the fitness value is basically the distance of the rocket from the target point
        # because we want the have a smaller fitness value for larger distances,
        # the inverse value of the distance is used
        inv_dist_to_target = 1.0 / self.location.dist(target)

        # if a collision was detected with an obstacle, penalize the fitness value
        fitness_rate = 1.0
        if not self.is_alive:
            fitness_rate = 0.0000000000000000001

        return inv_dist_to_target * fitness_rate

    # does the recombination between to elements of the population
    def crossover(self, other):

        # a new child is created
        child = Rocket(self.length)

        # generate a random midpoint
        midpoint = np.random.random_integers(1, other.length)

        for i in range(0, other.length):

            # do the recombination by taking force vectors from both elements
            if i < midpoint:
                child.forces[i] = self.forces[i]
            else:
                child.forces[i] = other.forces[i]

        return child

    # mutates the current force vector according to the current mutation rate
    def mutate(self, mutation_rate):
        for i in range(0, self.length):
            rand_value = np.random.rand()
            if rand_value < mutation_rate:
                self.forces[i] = Vector.random()

    # applies a force vector to the rocket's acceleration
    def apply_force(self, force):
        self.acceleration += force

    # applies a force vector to the rocket's acceleration
    # the force value is taken from the self.forces array
    def apply_force_at(self, at):
        self.acceleration += self.forces[at]

    # updates the location of the rocket
    def update(self):

        # update the velocity of the rocket
        self.velocity += self.acceleration

        # update the location of the rocket
        self.location += self.velocity

        # the acceleration of the rocket is set to 0.0
        self.acceleration.nul()
