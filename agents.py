from mesa import Agent
import numpy as np



class WalkerAgent(Agent):

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        if self.moore:
            next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
            next_move = self.random.choice(next_moves)
            # Now move:
            self.model.grid.move_agent(self, next_move)
        else:
            x,y = self.pos
            canditate_x = np.delete(np.arange(self.model.grid.width), x)
            canditate_y = np.delete(np.arange(self.model.grid.height),y)
            next_x = self.random.choice(canditate_x)
            next_y = self.random.choice(canditate_y)
            # Now move:
            self.model.grid.move_agent(self, (next_x, next_y))


class Tomato(Agent):

    def __init__(self, unique_id, pos, model):

        super().__init__(unique_id, model)
        self.pos= pos


class Salad(Agent):

    def __init__(self, unique_id, pos, model):

        super().__init__(unique_id, model)
        self.pos = pos

class Fermon(Agent):

    def __init__(self, unique_id, pos, model, type="Salad"):
        super().__init__(unique_id, model)
        self.pos = pos
        self.type = type


class Snail(WalkerAgent):

    energy = None

    def __init__(self, unique_id, pos, model, moore=True):
        super().__init__(unique_id, pos, model, moore)
        self.step_without_eat = 10

    def step(self):
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        salad = [obj for obj in this_cell if isinstance(obj, Salad)]
        tomato = [obj for obj in this_cell if isinstance(obj, Tomato)]

        #If there are salad or tomato
        if len(salad) > 0:
            self.step_without_eat = 10
            self.model.grid._remove_agent(self.pos, salad[0])
            self.model.salad-=1
            for neighbor in self.model.grid.get_neighborhood(self.pos, True):
                cell = self.model.grid.get_cell_list_contents([neighbor])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type=="Salad"]
                if len(fermon) == 1:
                    self.model.grid._remove_agent(neighbor, fermon[0])


        if len(tomato) > 0:
            self.model.grid._remove_agent(self.pos, tomato[0])
            self.step_without_eat = 10
            self.model.tomato-=1
            for neighbor in self.model.grid.get_neighborhood(self.pos, True):
                cell = self.model.grid.get_cell_list_contents([neighbor])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == "Tomato"]
                if len(fermon) == 1:
                    self.model.grid._remove_agent(neighbor, fermon[0])
        else:
            self.step_without_eat-=1

        change_pos = False
        if self.step_without_eat >= 1:
            for neighbor in self.model.grid.get_neighborhood(self.pos, True):
                cell = self.model.grid.get_cell_list_contents([neighbor])
                fermon = [obj for obj in cell if isinstance(obj, Fermon)]
                if len(fermon)>=1:
                    self.model.grid.move_agent(self, neighbor)
                    change_pos = True
            if not change_pos:
                self.random_move()
        # Reproduction

        #Death
        else:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            self.model.snail-=1


        # print("list salad", salad)


class Greenfly(WalkerAgent):

    energy = None
    def __init__(self, unique_id, pos, model, moore=False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.step_without_eat = 10

    def step(self):
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        tomato = [obj for obj in this_cell if isinstance(obj, Tomato)]

        if len(tomato) > 0:
            self.model.grid._remove_agent(self.pos,tomato[0])
            self.step_without_eat = 10
            self.model.tomato-=1
            for neighbor in self.model.grid.get_neighborhood(self.pos, True):
                cell = self.model.grid.get_cell_list_contents([neighbor])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == "Tomato"]
                if len(fermon) == 1:
                    self.model.grid._remove_agent(neighbor, fermon[0])
        else:
            self.step_without_eat -= 1

        change_pos = False
        if self.step_without_eat>=1:
            for neighbor in self.model.grid.get_neighborhood(self.pos, True):
                cell = self.model.grid.get_cell_list_contents([neighbor])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type=="Tomato"]
                if len(fermon) >= 1:
                    self.model.grid.move_agent(self, neighbor)
                    change_pos = True
            if not change_pos:
                self.random_move()
        #Reproduction

        #Death
        else:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            self.model.greenfly-=1




