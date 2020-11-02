from mesa import Model
from mesa.space import Grid
from mesa.datacollection import DataCollector

from agents import Snail, Greenfly, Salad, Tomato
from mesa.time import RandomActivation


class Garden(Model):




    verbose = False  # Print-monitoring



    def __init__(
        self,
        height=20,
        width=20,
        initial_tomato=100,
        initial_salad=100,
        initial_snail=50,
        initial_greenfly=50,
        preparation_1 = 50,
        preparation_2=30,
        fermon = 4,
        steps = 5,
        target=40

    ):

        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_tomato = initial_tomato
        self.initial_salad = initial_salad
        self.initial_snail = initial_snail
        self.initial_greenfly = initial_greenfly
        self.preparation_1 = preparation_1
        self.preparation_2 = preparation_2
        self.fermon = fermon
        self.steps = steps,
        self.target = target



        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=True)
        self.datacollector = DataCollector(
            {
                "Snail": lambda m: m,
                "Greenfly": lambda m:  m,
                "Salad": lambda m: m,
                "Tomato": lambda m: m
            }
        )

        # Create tomato:
        for i in range(self.initial_tomato):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            tomato = Tomato(self.next_id(), (x, y), self)
            self.grid.place_agent(tomato, (x, y))
            self.schedule.add(tomato)

        # Create tomato:
        for i in range(self.initial_salad):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            salad = Salad(self.next_id(), (x, y), self)
            self.grid.place_agent(salad, (x, y))
            self.schedule.add(salad)

        # Create snail
        for i in range(self.initial_snail):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            snail = Snail(self.next_id(), (x, y), self)
            self.grid.place_agent(snail, (x, y))
            self.schedule.add(snail)

        # Create greenfly
        for i in range(self.initial_greenfly):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            greenfly = Greenfly(self.next_id(), (x, y), self)
            self.grid.place_agent(greenfly, (x, y))
            self.schedule.add(greenfly)



        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)




    @staticmethod
    def count_type(model, tree_condition):
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
