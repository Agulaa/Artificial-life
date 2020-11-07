from mesa import Agent
import numpy as np
import random


class WalkerAgent(Agent):

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        if self.moore:
            next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
            next_move = self.random.choice(next_moves)
            self.model.grid.move_agent(self, next_move)
        else:
            x,y = self.pos
            canditate_x = np.arange(self.model.grid.width)
            canditate_y = np.arange(self.model.grid.height)
            next_x = self.random.choice(canditate_x)
            next_y = self.random.choice(canditate_y)
            while (x,y) == (next_x, next_y):
                next_x = self.random.choice(canditate_x)
                next_y = self.random.choice(canditate_y)
            self.model.grid.move_agent(self, (next_x, next_y))


class FermonAgent(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

    def death(self, type):
        x = self.pos[0]
        y = self.pos[1]
        for i in range(1, self.model.cell_fermon + 1):
            if x + i < self.model.width and y + i < self.model.height:
                new_fermon_cell = (x + i, y + i)
                cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
                for f in fermon:
                    self.model.grid._remove_agent(new_fermon_cell, f)

            if x - i >= 0 and y + i < self.model.height:
                new_fermon_cell = (x - i, y + i)
                cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
                for f in fermon:
                    self.model.grid._remove_agent(new_fermon_cell, f)
            if x - i >= 0 and y - i >= 0:
                new_fermon_cell = (x - i, y - i)
                cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
                for f in fermon:
                    self.model.grid._remove_agent(new_fermon_cell, f)
            if x + i < self.model.width and y - i >= 0:
                new_fermon_cell = (x + i, y - i)
                cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
                for f in fermon:
                    self.model.grid._remove_agent(new_fermon_cell, f)
            if x and y - i >= 0:
                new_fermon_cell = (x, y - i)
                cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
                for f in fermon:
                    self.model.grid._remove_agent(new_fermon_cell, f)
            if x and y + i < self.model.height:
                new_fermon_cell = (x, y + i)
                cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
                for f in fermon:
                    self.model.grid._remove_agent(new_fermon_cell, f)
            if x and y - i >= 0:
                new_fermon_cell = (x, y - i)
                cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
                for f in fermon:
                    self.model.grid._remove_agent(new_fermon_cell, f)
            if x and y + i < self.model.height:
                new_fermon_cell = (x, y + i)
                cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
                for f in fermon:
                    self.model.grid._remove_agent(new_fermon_cell, f)
            if x + i < self.model.width and y:
                new_fermon_cell = (x + i, y)
                cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
                for f in fermon:
                    self.model.grid._remove_agent(new_fermon_cell, f)
            if x - i >= 0 and y:
                new_fermon_cell = (x - i, y)
                cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
                for f in fermon:
                    self.model.grid._remove_agent(new_fermon_cell, f)

        self.model.grid._remove_agent(self.pos, self)


class Tomato(FermonAgent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, pos, model)
        self.pos = pos
        self.eaten_by_greenfly = 5
        self.is_weak = False


class Salad(FermonAgent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, pos, model)
        self.pos = pos
        self.eaten_by_snail = 4
        self.is_weak = False


class Fermon(Agent):

    def __init__(self, unique_id, pos, model, type="Salad"):
        super().__init__(unique_id, model)
        self.pos = pos
        self.type = type


class Snail(WalkerAgent):

    def __init__(self, unique_id, pos, model, moore=True):
        super().__init__(unique_id, pos, model, moore)
        self.step_without_eat = self.model.step_without_eat_snail
        self.reproduction_snail = self.model.reproduction_snail


    def step(self):
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        salad = [obj for obj in this_cell if isinstance(obj, Salad)]
        tomato = [obj for obj in this_cell if isinstance(obj, Tomato)]

        if len(salad) > 0:
            #Jeśli sałata była na polu, to ślimak się najadł
            self.step_without_eat = self.model.step_without_eat_snail
            #Jeśli sałata jest osłabiona to wystarczy jeden ślimak żeby ją zjeść
            if salad[0].is_weak:
                salad[0].death("Salad")
                self.model.salad -= 1
            else:
                #Sałata musi być zjedzona przez podaną liczbę ślimaków
                salad[0].eaten_by_snail-=1
                if salad[0].eaten_by_snail<=0:
                    salad[0].death("Salad")
                    self.model.salad -= 1

        if len(tomato) > 0:
            #Ślimak najada się listkami pomidorów i jedynie osłaba pomidory
            self.step_without_eat = self.model.step_without_eat_snail
            tomato[0].is_weak = True

        else:
            #jeśli nie było sałaty ani pomidora, to dekrementujemy zmienną step_without_eat
            self.step_without_eat-=1


        change_pos = False
        remember_pos = None

        # Kolejny krok wykonywany jest tam gdzie jest pomidor lub fermon lub losowo wybrany ruch
        if self.step_without_eat >= 1:
            #sprawdzamy po sąsiadach czy jest fermon, sałata lub pomidor
            for neighbor in self.model.grid.get_neighborhood(self.pos, True):
                cell = self.model.grid.get_cell_list_contents([neighbor])
                salad = [obj for obj in cell if isinstance(obj, Salad)]
                tomato = [obj for obj in cell if isinstance(obj, Tomato)]
                salad_fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == "Salad"]
                tomato_fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type=="Tomato"]
                # ślimak w pierwszej kolejności wybiera sałatę
                if len(salad)>=1:
                    self.model.grid.move_agent(self, neighbor)
                    change_pos = True
                elif len(tomato)>=1:
                    self.model.grid.move_agent(self, neighbor)
                    change_pos = True
                elif len(salad_fermon)>=1:
                    remember_pos = neighbor
                elif len(tomato_fermon)>=1:
                    remember_pos = neighbor
            if remember_pos and not change_pos:
                self.model.grid.move_agent(self, remember_pos)
                change_pos = True
            if not change_pos:
                self.random_move()

        #Death
        else:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            self.model.snail-=1

        # Reproduction - wiem że powinno to być wyżej bo tu już ten owad może nie żyć ale z jakegoś powodu to nie działało, będę próbować
        self.reproduction_snail -= 1
        if self.reproduction_snail == 0 and random.uniform(0, 1) < 0.3:
            snail = Snail(self.model.next_id(), self.pos, self.model)
            self.model.grid.place_agent(snail, self.pos)
            self.model.schedule.add(snail)

        if self.reproduction_snail == 0:
            self.reproduction_snail = self.model.reproduction_snail




class Greenfly(WalkerAgent):

    def __init__(self, unique_id, pos, model, moore=False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.step_without_eat = self.model.step_without_eat_greenfly
        self.reproduction_greenfly = self.model.reproduction_greenfly

    def step(self):
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        tomato = [obj for obj in this_cell if isinstance(obj, Tomato)]

        if len(tomato) > 0:
            #jeśli jest pomidor to mszyca się najada
            self.step_without_eat = self.model.step_without_eat_greenfly
            #Jeśli pomidor jest osłabiony to jak zaatakuje go jedna mszyca to umiera
            if tomato[0].is_weak:
                tomato[0].death("Tomato")
                self.model.tomato-=1
            #Jeśli pomidor nie był osłabiony, to muszą go zaatakować 5 mszyc
            else:
                tomato[0].eaten_by_greenfly-=1
                if tomato[0].eaten_by_greenfly<=0:
                    tomato[0].death("Tomato")
                    self.model.tomato -= 1
        else:
            #jeśli nie było pomidorów to dekremenyujemy zmienną step_without_eat
            self.step_without_eat -= 1

        change_pos = False
        remeber_pos = None
        # Kolejny krok jest zależy od tego, czy w sąsiedztwie jest fermon pomidora lub sam pomidor
        if self.step_without_eat>=1:
            for neighbor in self.model.grid.get_neighborhood(self.pos, True):
                cell = self.model.grid.get_cell_list_contents([neighbor])
                tomato = [obj for obj in cell if isinstance(obj, Tomato)]
                fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type=="Tomato"]
                if len(tomato)>=1:
                    self.model.grid.move_agent(self, neighbor)
                    change_pos = True
                elif len(fermon) >= 1:
                    remeber_pos = neighbor
            if remeber_pos and not change_pos:
                self.model.grid.move_agent(self, remeber_pos)
                change_pos = True
            if not change_pos:
                self.random_move()

        #Death
        else:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            self.model.greenfly-=1

        # Reproduction - wiem że powinno to być wyżej bo tu już ten owad może nie żyć ale z jakegoś powodu to nie działało, będę próbować
        self.reproduction_greenfly -= 1
        if self.reproduction_greenfly == 0 and random.uniform(0, 1) < 0.3:
            greenfly = Greenfly(self.model.next_id(), self.pos, self.model)
            self.model.grid.place_agent(greenfly, self.pos)
            self.model.schedule.add(greenfly)

        if self.reproduction_greenfly == 0:
            self.reproduction_greenfly = self.model.reproduction_greenfly


class Farmer(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dose_preparation_1 = self.model.preparation_1
        self.dose_preparation_2 = self.model.preparation_2
        self.use_preparation_1 = False
        self.use_preparation_2 = False

    def make_decision(self):

        if (self.model.tomato < self.model.target_tomato or self.model.salad < self.model.target_salad):

            

            return 0


        return 0




