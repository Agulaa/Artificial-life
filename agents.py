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

    def death_fermom_in_cell(self, new_fermon_cell, type):
        cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
        fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
        for f in fermon:
            self.model.grid._remove_agent(new_fermon_cell, f)

    def death(self, type):
        x = self.pos[0]
        y = self.pos[1]
        for i in range(0, self.model.cell_fermon + 1):
            if x + i < self.model.width and y + i < self.model.height:
                new_fermon_cell = (x + i, y + i)
                self.death_fermom_in_cell(new_fermon_cell, type)
            if x - i >= 0 and y + i < self.model.height:
                new_fermon_cell = (x - i, y + i)
                self.death_fermom_in_cell(new_fermon_cell, type)
            if x - i >= 0 and y - i >= 0:
                new_fermon_cell = (x - i, y - i)
                self.death_fermom_in_cell(new_fermon_cell, type)
            if x + i < self.model.width and y - i >= 0:
                new_fermon_cell = (x + i, y - i)
                self.death_fermom_in_cell(new_fermon_cell, type)
            if x + (i - 1) < self.model.width and y - i >= 0:
                new_fermon_cell = (x, y - i)
                self.death_fermom_in_cell(new_fermon_cell, type)
            if x and y + i < self.model.height:
                new_fermon_cell = (x, y + i)
                self.death_fermom_in_cell(new_fermon_cell, type)
            if x and y - i >= 0:
                new_fermon_cell = (x, y - i)
                self.death_fermom_in_cell(new_fermon_cell, type)
            if x + i < self.model.width and y:
                new_fermon_cell = (x + i, y)
                self.death_fermom_in_cell(new_fermon_cell, type)
            if x - i >= 0 and y:
                new_fermon_cell = (x - i, y)
                self.death_fermom_in_cell(new_fermon_cell, type)

        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)

class Tomato(FermonAgent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, pos, model)
        self.pos = pos
        self.eaten_by_greenfly = 5
        self.is_weak = False

    def step(self):
        if self.model.use_preparation_1 == True:
            if random.uniform(0, 1) < 0.15:
                self.is_weak = True
        if self.model.use_preparation_2 == True:
            if random.uniform(0, 1) < 0.2:
                self.is_weak = True

class Salad(FermonAgent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, pos, model)
        self.pos = pos
        self.eaten_by_snail = 4
        self.is_weak = False

    def step(self):
        if self.model.use_preparation_1 == True:
            if random.uniform(0, 1) < 0.15:
                self.is_weak = True
        if self.model.use_preparation_2 == True:
            if random.uniform(0, 1) < 0.2:
                self.is_weak = True

class Fermon(Agent):

    def __init__(self, unique_id, pos, model, type):
        super().__init__(unique_id, model)
        self.pos = pos
        self.type = type


class Snail(WalkerAgent):

    def __init__(self, unique_id, pos, model, moore=True):
        super().__init__(unique_id, pos, model, moore)
        self.step_without_eat = self.model.step_without_eat_snail
        self.reproduction_snail = self.model.reproduction_snail
        self.is_alive = True



    def step(self):

        # czy farmer stosuje w tym kroku jakiś preparat
        if self.model.use_preparation_2 == True:
            print('snail_2')
            if random.uniform(0, 1) < 0.8:
                self.is_alive = False
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                self.model.snail -= 1

        # czy owad zginął od środków owadobujczyć
        if self.is_alive == True:
            #Najpierw sprawdzamy co jest w komórce, w której znajduje się ślimak
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            salad = [obj for obj in this_cell if isinstance(obj, Salad)]
            tomato = [obj for obj in this_cell if isinstance(obj, Tomato)]
            #Jeśli sałata to się pożywia
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
            #jeśli pomidor to też się pożywia
            if len(tomato) > 0:
                #Ślimak najada się listkami pomidorów i jedynie osłaba pomidory
                self.step_without_eat = self.model.step_without_eat_snail
                tomato[0].is_weak = True

            else:
                #jeśli nie było sałaty ani pomidora, to dekrementujemy zmienną step_without_eat
                self.step_without_eat-=1


            # jeśli ślimak jest najedzony to wykonuje kolejny krok
            change_pos = False
            remember_pos = None
            # Kolejny krok wykonywany jest tam gdzie jest pomidor lub fermon lub losowo wybrany ruch
            if self.step_without_eat >= 1:
                #sprawdzamy po sąsiadach czy jest fermon, sałata lub pomidor
                for neighbor in self.model.grid.get_neighborhood(self.pos, True):
                    cell = self.model.grid.get_cell_list_contents([neighbor])
                    salad = [obj for obj in cell if isinstance(obj, Salad)]
                    salad_fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == "Salad"]
                    tomato = [obj for obj in cell if isinstance(obj, Tomato)]
                    tomato_fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type=="Tomato"]
                    # ślimak w pierwszej kolejności wybiera sałatę
                    if len(salad)>=1:
                        self.model.grid.move_agent(self, neighbor)
                        change_pos = True
                    elif len(salad_fermon)>=1:
                        remember_pos = neighbor
                    elif len(tomato)>=1:
                        self.model.grid.move_agent(self, neighbor)
                        change_pos = True
                    elif len(tomato_fermon)>=1:
                        remember_pos = neighbor

                if not change_pos and remember_pos:
                    self.model.grid.move_agent(self, remember_pos)
                    change_pos = True
                if not change_pos:
                    self.random_move()

            #Death - jeśli ślimak nie pożywił się to umiera
            else:
                self.is_alive = False
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                self.model.snail-=1

        # jeśli owad nie umarł z głodu ani od środków owadobujczych to sprawdzenie czy się rozmanaża
        if self.is_alive == True:
            # Reproduction - wiem że powinno to być wyżej bo tu już ten owad może nie żyć ale z jakegoś powodu to nie działało, będę próbować
            self.reproduction_snail -= 1
            if self.reproduction_snail == 0 and random.uniform(0, 1) < 0.5:
                snail = Snail(self.model.next_id(), self.pos, self.model)
                self.model.grid.place_agent(snail, self.pos)
                self.model.schedule.add(snail)
                self.model.snail+=1

            if self.reproduction_snail == 0:
                self.reproduction_snail = self.model.reproduction_snail


class Greenfly(WalkerAgent):

    def __init__(self, unique_id, pos, model, moore=False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.step_without_eat = self.model.step_without_eat_greenfly
        self.reproduction_greenfly = self.model.reproduction_greenfly
        self.is_alive = True

    def step(self):

        # czy farmer stosuje w tym kroku preparat owadobujczy
        if self.model.use_preparation_1 == True:
            print('greenfly_1')
            if random.uniform(0, 1) < 0.85:
                self.is_alive = False
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                self.model.greenfly -= 1

        elif self.model.use_preparation_2 == True:
            print('greenfly_2')
            if random.uniform(0, 1) < 0.2:
                self.is_alive = False
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                self.model.greenfly -= 1

        #czy owad zginął od środków owadobujczyć
        if self.is_alive == True:

            #Sprawdzanie co jest na podanej komóre, na której jest mszyca - jeśli jest pomidor - to się posila
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            tomato = [obj for obj in this_cell if isinstance(obj, Tomato)]
            if len(tomato) > 0:
                #jeśli jest pomidor to mszyca się najada
                self.step_without_eat = self.model.step_without_eat_greenfly
                #Jeśli pomidor jest osłabiony to jak zaatakuje go jedna mszyca to pomidor umiera
                if tomato[0].is_weak:
                    tomato[0].death("Tomato")
                    self.model.tomato-=1
                #Jeśli pomidor nie był osłabiony, to muszą go zaatakować 5 mszyc, więc inkrementujemy wartość dla pomidora
                else:
                    tomato[0].eaten_by_greenfly-=1
                    if tomato[0].eaten_by_greenfly<=0:
                        tomato[0].death("Tomato")
                        self.model.tomato -= 1
            else:
                #jeśli nie było pomidorów to dekremenyujemy zmienną step_without_eat
                self.step_without_eat -= 1

            # Zmiana swojej pozycji, jeśli mszyca jest w stanie dalej żyć - tzn jest najedzona
            change_pos = False
            remember_pos = None
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
                        remember_pos = neighbor
                        #self.model.grid.move_agent(self, neighbor)
                        #change_pos = True
                if not change_pos and remember_pos:
                    self.model.grid.move_agent(self, remember_pos)
                    change_pos = True

                if not change_pos:
                    self.random_move()

            #Death - jeśli mszyca nie jest najedzona - umiera
            else:
                self.is_alive = False
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                self.model.greenfly -= 1

        #jeśli owad nie umarł z głodu ani od środków owadobujczych to sprawdzenie czy się rozmanaża
        if self.is_alive == True:
            # Reproduction - wiem że powinno to być wyżej bo tu już ten owad może nie żyć ale z jakegoś powodu to nie działało, będę próbować
            self.reproduction_greenfly -= 1
            if self.reproduction_greenfly == 0 and random.uniform(0, 1) < 0.5:
                greenfly = Greenfly(self.model.next_id(), self.pos, self.model)

                self.model.grid.place_agent(greenfly, self.pos)
                self.model.schedule.add(greenfly)
                self.model.greenfly += 1

            if self.reproduction_greenfly == 0:
                self.reproduction_greenfly = self.model.reproduction_greenfly





class Farmer(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dose_preparation_1 = self.model.preparation_1
        self.dose_preparation_2 = self.model.preparation_2

    def use_preparation(self):
        self.use_preparation_1 = False
        self.use_preparation_2 = False

#(todo programowowanie ilorazowe??)

        # jeśli mamy dawki preparatu i jeśli brakuje roślin
        if (self.dose_preparation_1 > 0 or self.dose_preparation_2 > 0) and (self.model.target_tomato > self.model.tomato or self.model.target_salad > self.model.salad):

            # ile owadów zostanie po zastosowaniu każdego preparatu - chcemy minimalizować
            insects1 = 0.15 * self.model.greenfly + self.model.snail
            insects2 = 0.2 * self.model.snail + 0.8 * self.model.greenfly

            # ile zrowych roślin będzie brakować po zastosowaniu każdego preparatu - chcemy minimalizować
            plants1 = max(0, self.model.target_salad - 0.85 * self.model.salad) + max(0, self.model.target_tomato - 0.85 * self.model.tomato)
            plants2 = max(0, self.model.target_salad - 0.8 * self.model.salad) + max(0, self.model.target_tomato - 0.8 * self.model.tomato)

            if insects1 + plants1 < insects2 + plants2:
                if self.dose_preparation_1 > 0:
                    self.use_preparation_1 = True
            else:
                if self.dose_preparation_2 > 0:
                    self.use_preparation_2 = True


        return self.use_preparation_1, self.use_preparation_2
            







