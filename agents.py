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


class Snail(WalkerAgent):

    energy = None

    def __init__(self, unique_id, pos, model, moore=True):
        super().__init__(unique_id, pos, model, moore)



class Greenfly(WalkerAgent):

    energy = None

    def __init__(self, unique_id, pos, model, moore=False):
        super().__init__(unique_id, pos, model, moore=moore)


