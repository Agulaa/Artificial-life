from mesa import Model
from mesa.space import MultiGrid, SingleGrid
from mesa.datacollection import DataCollector

from agents import Snail, Greenfly, Salad, Tomato, Fermon, Farmer
from mesa.time import RandomActivation


class Garden(Model):


    def __init__(
        self,
        height=20,
        width=20,
        initial_tomato=20,
        initial_salad=20,
        initial_snail=10,
        initial_greenfly=10,
        preparation_1 = 10,
        preparation_2=10,
        cell_fermon = 1,
        steps = 5,
        target_tomato=20,
        target_salad=20,
        step_without_eat_snail = 10,
        step_without_eat_greenfly=10,
        reproduction_snail = 10,
        reproduction_greenfly = 10

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
        self.cell_fermon = cell_fermon
        self.steps = steps
        self.target_tomato = target_tomato
        self.target_salad = target_salad
        self.tomato = self.initial_tomato
        self.salad = self.initial_salad
        self.greenfly = self.initial_greenfly
        self.snail = self.initial_snail
        self.step_without_eat_snail = step_without_eat_snail
        self.step_without_eat_greenfly = step_without_eat_greenfly
        self.reproduction_snail = reproduction_snail
        self.reproduction_greenfly = reproduction_greenfly

        self.schedule = RandomActivation(self)

        self.grid = MultiGrid(height, width, torus=False)

        self.datacollector = DataCollector(
            {
                "Snail": "snail",
                "Greenfly": "greenfly",
                "Salad": "salad",
                "Tomato": "tomato"
            }
        )

        #Create farmer:
        farmer = Farmer(self.next_id(), self)
        self.schedule.add(farmer)

        # Create tomato:
        for i in range(self.initial_tomato):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            this_cell = self.grid.get_cell_list_contents([(x, y)])
            tomato = [obj for obj in this_cell if isinstance(obj, Tomato)]
            if len(tomato) == 0:
                empty = (x, y)
                tomato = Tomato(self.next_id(), empty, self)
                self.grid.place_agent(tomato, empty)
                self.schedule.add(tomato)
                self.put_all_fermon(tomato, "Tomato")





        # Create salad:
        for i in range(self.initial_salad):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            this_cell = self.grid.get_cell_list_contents([(x,y)])
            tomato = [obj for obj in this_cell if isinstance(obj, Tomato)]
            if len(tomato)==0:
                empty = (x,y)
                salad = Salad(self.next_id(), empty, self)
                self.grid.place_agent(salad, empty)
                self.schedule.add(salad)
                self.put_all_fermon(salad, "Salad")
            else:
                counter = 0
                while len(tomato)!=0 or counter==100:
                    x = self.random.randrange(self.width)
                    y = self.random.randrange(self.height)
                    this_cell = self.grid.get_cell_list_contents([(x, y)])
                    tomato = [obj for obj in this_cell if isinstance(obj, Tomato)]
                    counter+=1
                empty = (x, y)
                salad = Salad(self.next_id(), empty, self)
                self.grid.place_agent(salad, empty)
                self.schedule.add(salad)
                self.put_all_fermon(salad, "Salad")

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

    def put_fermon(self, new_fermon_cell, type):
        new_fermon = Fermon(self.next_id(), new_fermon_cell, self, type)
        self.grid.place_agent(new_fermon, new_fermon_cell)


    def put_all_fermon(self, position, type):
        for i in range(0, self.cell_fermon + 1):
            x = position.pos[0]
            y = position.pos[1]
            if x + i < self.width and y + i < self.height:
                new_fermon_cell = (x + i, y + i)
                self.put_fermon(new_fermon_cell, type)
            if x - i >= 0 and y + i < self.height:
                new_fermon_cell = (x - i, y + i)
                self.put_fermon(new_fermon_cell, type)
            if x - i >= 0 and y - i >= 0:
                new_fermon_cell = (x - i, y - i)
                self.put_fermon(new_fermon_cell, type)
            if x + i < self.width and y - i >= 0:
                new_fermon_cell = (x + i, y - i)
                self.put_fermon(new_fermon_cell, type)
            if x+(i-1)<self.width and y - i >= 0:
                new_fermon_cell = (x, y - i)
                self.put_fermon(new_fermon_cell, type)
            if x  and y + i <  self.height:
                new_fermon_cell = (x, y + i)
                self.put_fermon(new_fermon_cell, type)
            if x and y - i >= 0:
                new_fermon_cell = (x, y - i)
                self.put_fermon(new_fermon_cell, type)
            if x + i < self.width and y:
                new_fermon_cell = (x + i, y)
                self.put_fermon(new_fermon_cell, type)
            if x - i >= 0 and y:
                new_fermon_cell = (x - i, y)
                self.put_fermon(new_fermon_cell, type)
