from mesa import Agent
import numpy as np
import random

class WalkerAgent(Agent):
    """
  Klasa agenta, która dziedziczy po klasie Agent.
  Została w niej zaimplementowana metoda,
  z której będą korzystać agenci, którzy będą się poruszać na planszy.
    """

    def __init__(self, unique_id, pos, model, moore):
        """
        :param unique_id: unikalne id dla agenta
        :param pos: pozycja na planszy
        :param model: model
        :param moore: wartość True/False, oznaczająca czy agent będzie poruszał się zgodne z sąsiedztwem moore czy nie
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        """
        Jeśli agent będzie poruszał się zgodnie z sąsiedztwem moore, to następny krok jest w obrębie jego sąsiedzta
        Jeśli natomiast agent, nie będzie poruszał sie zgodnie z sąsiedztewem moore, to następny krok jest losowy.
        :return:
        """
        if self.moore:

            next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
            next_move = self.random.choice(next_moves)
            self.model.grid.move_agent(self, next_move)
            return next_move
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
            return (next_x, next_y)
class PlantAgent(Agent):
    """
    Dziedziczy po klasie Agent, jest to klasa, która nie porusza, wydziela fermony, na zadaną ilość kratek

    """
    def __init__(self, unique_id, pos, model):
        """
        :param unique_id: unikalne id
        :param pos: pozycja na planszy
        :param model: model
        """
        super().__init__(unique_id, model)
        self.pos = pos


    def death_fermom_in_cell(self, new_fermon_cell, type):
        """
        Usunuęcie wszytskich fermonu z planszy z konkretnej pozycji, które wydzielała ta roślina
        :param cell: pozycja fermonu do usunięcia
        :param type: typ fermonu
        """
        cell = self.model.grid.get_cell_list_contents([new_fermon_cell])
        fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == type]
        for f in fermon:
            if f.plant_id == self.unique_id:
                self.model.grid._remove_agent(new_fermon_cell, f)

    def death(self, type):
        """
        Metoda uruchamiana jest gdy zostaje usunięta z planszy roślina.
        Metoda ta usuwa z planszy wszytskie fermony, które wydzielała ta roślina
        :param type: typ fermonu
        """
        # Pobranie pozycji rośliny
        x = self.pos[0]
        y = self.pos[1]
        # W zależności od intensywności fermonów,usuwane są wszytskie, które były w obrębie tej rośliny wydzielane
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
            if y + i < self.model.height:
                new_fermon_cell = (x, y + i)
                self.death_fermom_in_cell(new_fermon_cell, type)
            if y - i >= 0:
                new_fermon_cell = (x, y - i)
                self.death_fermom_in_cell(new_fermon_cell, type)
            if x + i < self.model.width :
                new_fermon_cell = (x + i, y)
                self.death_fermom_in_cell(new_fermon_cell, type)
            if x - i >= 0 :
                new_fermon_cell = (x - i, y)
                self.death_fermom_in_cell(new_fermon_cell, type)

        # Po usunięciu fermonów, które wydzielała roślina, usuwane jest sama ona
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)
class Tomato(PlantAgent):
    """
    Agent pomiodr, dziedziczy po klasie PlantAgent, nie porusza się, wydziela fermony.
    Może zostać osłabiony przez preparat lub zwierzę.
    """

    def __init__(self, unique_id, pos, model):
        """
        :param unique_id: unikalne id
        :param pos: pozycja na planszy
        :param model: model
        is_weak: Czy ageny jest osłabiony
        """
        super().__init__(unique_id, pos, model)
        self.pos = pos
        self.eaten_by_greenfly = 5
        self.step_regeneration = self.model.recovery_tomato
        self.is_weak = False

    def step(self):
        """
        Podczas metody step, agent się nie zmiena pozycji, może zostać jedynie osłabiony przez preparaty
        """
        if self.model.use_preparation_1 == True:
            if random.uniform(0, 1) < 0.15:
                if self.is_weak==False:
                    self.is_weak = True
                    self.model.tomato_weak +=1
        if self.model.use_preparation_2 == True:
            if random.uniform(0, 1) < 0.2:
                if self.is_weak==False:
                    self.is_weak = True
                    self.model.tomato_weak += 1
        # Jeśli jest osłabiona, może się zregenerować po 5 krokach
        if self.is_weak:
            self.step_regeneration -=1
            if self.step_regeneration <=0:
                self.is_weak=False
                self.step_regeneration = 5
                self.model.tomato_weak -= 1
class Salad(PlantAgent):
    """
    Agent sałata, dziedziczy po klasie PlantAgent, nie porusza się, wydziela fermony.
    Może zostać osłabiony przez preparat lub zwierzę.
    """

    def __init__(self, unique_id, pos, model):
        """
      :param unique_id: unikalne id
      :param pos: pozycja na planszy
      :param model: model
      is_weak: Czy ageny jest osłabiony
        """
        super().__init__(unique_id, pos, model)
        self.pos = pos
        self.eaten_by_snail = 4
        self.step_regeneration = self.model.recovery_salad
        self.is_weak = False

    def step(self):
        """
         Podczas metody step, agent się nie zmiena pozycji, może zostać jedynie osłabiony przez preparaty
        """
        if self.model.use_preparation_1 == True:
            if random.uniform(0, 1) < 0.15:
                if self.is_weak == False:
                    self.is_weak = True
                    self.model.salad_weak += 1
        if self.model.use_preparation_2 == True:
            if random.uniform(0, 1) < 0.2:
                if self.is_weak==False:
                    self.is_weak = True
                    self.model.salad_weak += 1
        # Jeśli jest osłabiona, może się zregenerować po 5 krokach
        if self.is_weak:
            self.step_regeneration -=1
            if self.step_regeneration <=0:
                self.is_weak=False
                self.step_regeneration = 5
                self.model.salad_weak-=1
class Fermon(Agent):
    """
    Agent Fermon, dziedziczy po klasie Agent, nie zmienia swojej pozycji, ma określony typ wydzielania fermonu
    """

    def __init__(self, unique_id, pos, model, type, plant_id):
        """
        :param unique_id: unikalne id
        :param pos: pozycja na planszy
        :param model: model
        :param type: typ fermonu
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.type = type
        self.plant_id = plant_id
class Snail(WalkerAgent):
    """
    Agent ślimak, dziedziczy po klasie WalkerAgent, porusza się zgodnie ze sąsiedztwem Moora.
    """

    def __init__(self, unique_id, pos, model, moore=True):
        """
        self.step_without_eat - ilość korków bez jedzenia, która jest ustawiana przez użytwkownika
        self.reproduction_snail - wielkość reprodukcji, która jest ustawiana przez użytwkownika
        self.is_alive - zmienna boolowska, która informuje, czy ślimak żyje

        :param unique_id: unikalne id
        :param pos: pozycja na planszy
        :param model: model
        :param moore: czy porusza się zgodznie z sąsiedztwem moore'a
        """
        super().__init__(unique_id, pos, model, moore)
        self.step_without_eat = self.model.step_without_eat_snail
        self.reproduction_snail = self.model.reproduction_snail
        self.is_alive = True
        self.last_move = None


    def death(self):
        self.is_alive = False
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)
        self.model.snail -= 1

    def reproduction(self):
        snail = Snail(self.model.next_id(), self.pos, self.model)
        self.model.grid.place_agent(snail, self.pos)
        self.model.schedule.add(snail)
        self.model.snail += 1

    def step(self):

        """
        Metoda wykonywana podczas ruchu ślimaka.
        1) sprawdzenie czy zastosowane zostały preparaty przez rolnika
        2) sprawdzenie czy środek nie zabił ślimaka
        3) sprawdzenie, co znajduje się na pozycji - jeśli jest pożywienie, ślimak je zjada
        4) jeśli ślimak jest najedzony, wykonuje krok; jeśli się nie najadł to umiera
        5) jeśli owad nie umarł z głodu ani od środków owadobujczych to sprawdzenie czy się rozmanaża
        """
        # czy farmer stosuje w tym kroku jakiś preparat
        if self.model.use_preparation_2 == True:
            if random.uniform(0, 1) < 0.8:
                self.death()

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
                    self.model.salad_weak-=1
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
                if tomato[0].is_weak == False:
                    tomato[0].is_weak = True
                    self.model.tomato_weak += 1
            else:
                #jeśli nie było sałaty ani pomidora, to dekrementujemy zmienną step_without_eat
                self.step_without_eat-=1


            # jeśli ślimak jest najedzony to wykonuje kolejny krok
            change_pos = False
            remember_pos = None
            salad_pos = None
            tomato_pos = None
            # Kolejny krok wykonywany jest tam gdzie jest pomidor lub fermon lub losowo wybrany ruch
            if self.step_without_eat >= 1:
                #sprawdzamy po sąsiadach czy jest fermon, sałata lub pomidor
                for neighbor in self.model.grid.get_neighborhood(self.pos, True):
                    # blokada ruchu poprzedniego - zapobiega zablokowaniu się
                    if neighbor != self.last_move:
                        cell = self.model.grid.get_cell_list_contents([neighbor])
                        salad = [obj for obj in cell if isinstance(obj, Salad)]
                        salad_fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type == "Salad"]
                        tomato = [obj for obj in cell if isinstance(obj, Tomato)]
                        tomato_fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type=="Tomato"]
                        # ślimak w pierwszej kolejności wybiera sałatę
                        if len(salad)>=1:
                            salad_pos = neighbor
                        elif len(salad_fermon)>=1:
                            remember_pos = neighbor
                        elif len(tomato)>=1:
                            tomato_pos = neighbor
                        elif len(tomato_fermon)>=1:
                            remember_pos = neighbor
                self.last_move = self.pos
                if salad_pos:
                    self.model.grid.move_agent(self, salad_pos)
                    change_pos = True
                if not change_pos and tomato_pos:
                    self.model.grid.move_agent(self, tomato_pos)
                    change_pos = True
                if not change_pos and remember_pos:
                    self.model.grid.move_agent(self, remember_pos)
                    change_pos = True
                if not change_pos:
                    move = self.random_move()



            #Death - jeśli ślimak nie pożywił się to umiera
            else:
                self.death()


        # jeśli owad nie umarł z głodu ani od środków owadobujczych to sprawdzenie czy się rozmanaża
        if self.is_alive == True:
            # Reproduction - wiem że powinno to być wyżej bo tu już ten owad może nie żyć ale z jakegoś powodu to nie działało, będę próbować
            self.reproduction_snail -= 1
            if self.reproduction_snail == 0 and random.uniform(0, 1) < 0.5:
                self.reproduction()

            if self.reproduction_snail == 0:
                self.reproduction_snail = self.model.reproduction_snail


class Greenfly(WalkerAgent):
    """
    Dziedziczy po klasie WalkerAgent, porusza się losowo w kierunku wydzielanych fermonów
    """

    def __init__(self, unique_id, pos, model, moore=False):
        """
        self.step_without_eat - ilość korków bez jedzenia, która jest ustawiana przez użytwkownika
        self.reproduction_greenfly - wielkość reprodukcji, która jest ustawiana przez użytwkownika
        self.is_alive - zmienna boolowska, która informuje, czy mszyca żyje

        :param unique_id: unikalne id
        :param pos: pozycja na planszy
        :param model: model
        :param moore: czy porusza się zgodznie z sąsiedztwem moore'a
        """
        super().__init__(unique_id, pos, model, moore=moore)
        self.step_without_eat = self.model.step_without_eat_greenfly
        self.reproduction_greenfly = self.model.reproduction_greenfly
        self.is_alive = True
        self.last_move = None

    def death(self):
        self.is_alive = False
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)
        self.model.greenfly -= 1

    def reproduction(self):
        greenfly = Greenfly(self.model.next_id(), self.pos, self.model)
        self.model.grid.place_agent(greenfly, self.pos)
        self.model.schedule.add(greenfly)
        self.model.greenfly += 1

    def step(self):
        """
        Metoda wykonywana podczas ruchu ślimaka.
        1) sprawdzenie czy zastosowane zostały preparaty przez rolnika
        2) sprawdzenie czy środek nie zabił ślimaka
        3) sprawdzenie, co znajduje się na pozycji - jeśli jest pożywienie, ślimak je zjada
        4) jeśli ślimak jest najedzony, wykonuje krok; jeśli się nie najadł to umiera
        5) jeśli owad nie umarł z głodu ani od środków owadobujczych to sprawdzenie czy się rozmanaża

        """
        # czy farmer stosuje w tym kroku preparat owadobujczy
        if self.model.use_preparation_1 == True:
            if random.uniform(0, 1) < 0.85:
                self.death()

        elif self.model.use_preparation_2 == True:
            if random.uniform(0, 1) < 0.2:
                self.death()

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
                    self.model.tomato_weak -=1
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
            tomato_pos = None
            # Kolejny krok jest zależy od tego, czy w sąsiedztwie jest fermon pomidora lub sam pomidor
            if self.step_without_eat>=1:
                for neighbor in self.model.grid.get_neighborhood(self.pos, True):
                    if neighbor != self.last_move:
                        cell = self.model.grid.get_cell_list_contents([neighbor])
                        tomato = [obj for obj in cell if isinstance(obj, Tomato)]
                        fermon = [obj for obj in cell if isinstance(obj, Fermon) and obj.type=="Tomato"]
                        if len(tomato)>=1:
                            tomato_pos = neighbor
                        elif len(fermon) >= 1:
                            remember_pos = neighbor
                self.last_move = self.pos
                if tomato_pos:
                    self.model.grid.move_agent(self, tomato_pos)
                    change_pos = True
                if not change_pos and remember_pos:
                    self.model.grid.move_agent(self, remember_pos)
                    change_pos = True
                if not change_pos:
                    move = self.random_move()

            #Death - jeśli mszyca nie jest najedzona - umiera
            else:
                self.death()

        #jeśli owad nie umarł z głodu ani od środków owadobujczych to sprawdzenie czy się rozmanaża
        if self.is_alive == True:
            self.reproduction_greenfly -= 1
            if self.reproduction_greenfly == 0 and random.uniform(0, 1) < 0.5:
                self.reproduction()

            if self.reproduction_greenfly == 0:
                self.reproduction_greenfly = self.model.reproduction_greenfly
class Farmer(Agent):
    """
    Agent Farmer, dziedziczy po klasie Agent, nie porusza się,
    w każdym kroku może zastosować preparaty, które mają na celu zniwelować szkodliwe owady
    """
    def __init__(self, unique_id, model):
        """
        self.dose_preparation_1 - ilość parametru pierwszego
        self.dose_preparation_2 - ilość parametru drugiego
        :param unique_id: unikalne id
        :param model: model
        """
        super().__init__(unique_id, model)
        self.dose_preparation_1 = self.model.preparation_1
        self.dose_preparation_2 = self.model.preparation_2

    def use_preparation(self):
        self.use_preparation_1 = False
        self.use_preparation_2 = False


        # jeśli mamy dawki preparatu i jeśli brakuje roślin
        if (self.dose_preparation_1 > 0 or self.dose_preparation_2 > 0) and (self.model.greenfly > self.model.tomato or self.model.snail >= self.model.tomato + self.model.salad):

            # ile owadów zostanie po zastosowaniu każdego preparatu - chcemy minimalizować
            insects1 = 0.15 * self.model.greenfly + self.model.snail
            insects2 = 0.2 * self.model.snail + 0.8 * self.model.greenfly

            # ile zrowych roślin będzie brakować po zastosowaniu każdego preparatu - chcemy minimalizować
            plants1 = max(0, self.model.target_salad - 0.85 * self.model.salad) + max(0, self.model.target_tomato - 0.85 * self.model.tomato)
            plants2 = max(0, self.model.target_salad - 0.8 * self.model.salad) + max(0, self.model.target_tomato - 0.8 * self.model.tomato)

            if insects1 + plants1 < insects2 + plants2:
                if self.dose_preparation_1 > 0:
                    self.use_preparation_1 = True
                    self.dose_preparation_1 -= 1
            else:
                if self.dose_preparation_2 > 0:
                    self.use_preparation_2 = True
                    self.dose_preparation_2 -= 1


        return self.use_preparation_1, self.use_preparation_2
            







