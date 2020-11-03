from mesa import Model
from mesa.space import MultiGrid, SingleGrid
from mesa.datacollection import DataCollector

from agents import Snail, Greenfly, Salad, Tomato, Fermon
from mesa.time import RandomActivation


class Garden(Model):




    #verbose = False  # Print-monitoring



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
        self.steps = steps
        self.target = target
        self.tomato = self.initial_tomato
        self.salad = self.initial_salad
        self.greenfly = self.initial_greenfly
        self.snail = self.initial_snail

        self.schedule = RandomActivation(self)

        self.grid = MultiGrid(height, width, torus=True)

        self.datacollector = DataCollector(
            {
                "Snail": "snail",
                "Greenfly": "greenfly",
                "Salad": "salad",
                "Tomato": "tomato"
            }
        )

        # Create tomato:
        for i in range(self.initial_tomato):
            empty = self.grid.find_empty()
            if empty:
                tomato = Tomato(self.next_id(), empty, self)
                self.grid.place_agent(tomato, empty)
                self.schedule.add(tomato)

                for neighbor in self.grid.get_neighborhood(tomato.pos, True):
                    fermon = Fermon(self.next_id(),neighbor, self, type="Tomato")
                    self.grid.place_agent(fermon, neighbor)

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
                for neighbor in self.grid.get_neighborhood(salad.pos, True):
                    fermon = Fermon(self.next_id(),neighbor, self, type="Salad")
                    self.grid.place_agent(fermon, neighbor)
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
                for neighbor in self.grid.get_neighborhood(salad.pos, True):
                    fermon = Fermon(self.next_id(), neighbor, self, type="Salad")
                    self.grid.place_agent(fermon, neighbor)

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



