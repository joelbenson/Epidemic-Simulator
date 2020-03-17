import random

class DiseaseState():

    def __init__(self):
        self.state = Healthy()

    def next_state(self):

        #Get next disease state period
        disease = self.state

        #If disease is Healthy or Deceased, return
        if disease.name in ['Healthy', 'Deceased']:
            return

        #Get period of disease
        disease.clock += 1
        try:
            disease.period = disease.period_dict[disease.clock]
        except:
            disease.period = 'convalescence'

        #Update disease intensity, contagiousness, color, death probability, recovery_probability
        disease.update_intensity()
        disease.contagiousness = disease.properties['transmission_rate'] * disease.intensity
        disease.update_color()
        disease.update_death_probability()
        disease.update_recovery_probability()
        disease.contagiousness

        #Test for recovery
        fate = random.random()
        if (fate < disease.recovery_probability):

            self.state = Healthy()

        #Test for death
        fate = random.random()
        if (fate < disease.death_probability):
            self.state = Deceased()

        return


class Disease():

    def __init__(self):
        self.name = None
        self.strain = None
        self.id = None
        self.properties = {}
        self.clock = 0

    def init_period_dict(self):

        incubation_period = self.properties['incubation_period']
        illness_period = self.properties['illness_period']
        convalescence_period = self.properties['convalescence_period']

        period_dict = {}

        i = 1

        for j in range(incubation_period):

            period_dict[i] = 'incubation'
            i += 1

        for j in range(illness_period):

            period_dict[i] = 'illness'
            i += 1

        for j in range(convalescence_period):

            period_dict[i] = 'convalescence'
            i += 1

        self.period_dict = period_dict

    def test_mutation(self):

        fate = random.random()

        if (fate < self.properties['mutation_rate']):

            self.mutate()

        return

    def mutate(self):

        MUTATION_AMOUNT = 0.005

        #Generate random strain id
        self.strain = ''.join(str(random.choice(range(1000))))
        self.id = self.name + self.strain

        #For each property, add random value within range of mutation amount (including negative)
        for key in self.properties.keys():

            if (key == 'color'):

                COLOR_CHANGE_RATE = 80
                fate = (
                    random.choice([-COLOR_CHANGE_RATE, COLOR_CHANGE_RATE]),
                    random.choice([-COLOR_CHANGE_RATE, COLOR_CHANGE_RATE]),
                    random.choice([-COLOR_CHANGE_RATE, COLOR_CHANGE_RATE]),
                )

                self.properties['color'] = (
                    min(max(int(self.properties['color'][0] + fate[0]), 0), 255),
                    min(max(int(self.properties['color'][1] + fate[1]), 0), 255),
                    min(max(int(self.properties['color'][2] + fate[2]), 0), 255)
                )
            elif (key == 'transmission_range'):

                fate = random.choice([-1, 0, 1])

                self.properties[key] += fate
                self.properties[key] = max(self.properties[key], 0)

                pass

            elif (key == 'mutation_rate'):

                pass

            else:
                #Get random number between -0.05 and 0.05
                fate = -MUTATION_AMOUNT + (MUTATION_AMOUNT*2)*random.random()

                self.properties[key] += fate
                #Mask to range [0, 1]
                self.properties[key] = min(max(0, self.properties[key]), 1)

        return

    def update_intensity(self):

        #If in incubation, make it fraction of way through
        if (self.period == 'incubation'):

            self.intensity = float(self.clock) / (self.properties['incubation_period'] + 1)

        #If illness, make intensity full
        elif (self.period == 'illness'):

            self.intensity = 1

        #If convalescence, have it decrease regularly to end
        elif (self.period == 'convalescence'):

            self.intensity *= (1 - (1.0 / self.properties['convalescence_period']))

        return

    def update_color(self):

        property_r, property_g, property_b = self.properties['color']

        #Use disease intensity to weight disese color and blank color
        i = self.intensity
        j = 1 - i

        color = (int(i * property_r + j * 255), int(i * property_g + j * 255), int(i * property_b + j * 255))
        self.color = (min([max([0, color[0]]), 255]), min([max([0, color[1]])]), min([max([0, color[2]])]))

        return

    def update_death_probability(self):

        #If in illness period, adjust probability so expected death holds
        if (self.period == 'illness'):

            self.death_probability = self.properties['death_rate'] / self.properties['convalescence_period']

        else: self.death_probability = 0

        return

    def update_recovery_probability(self):

        #If in convalescence period, adjust probability so expected length of period holds
        if (self.period == 'convalescence'):

            self.recovery_probability = 1.0 / self.properties['convalescence_period']

        else: self.recovery_probability = 0

        return

    def reset(self):

        #Reset disease clock
        self.clock = 0

        #Possibly mutate
        self.test_mutation()

        return


class Healthy(Disease):

    def __init__(self):
        super().__init__()
        self.name = 'Healthy'
        self.strain = None
        self.id = 'Healthy'
        self.color = (255, 255, 255)
        self.period = None
        self.intensity = None
        self.recovery_probability = None
        self.death_probability = None
        self.properties ={
            'color': (255, 255, 255),
            'transmission_range': None,
            'transmission_rate': None,
            'incubation_period': None,
            'illness_period': None,
            'convalescence_period': None,
            'death_rate': None,
            'mutation_rate': None
        }
        self.clock = 0

class Deceased(Disease):

    def __init__(self):
        super().__init__()
        self.name = 'Deceased'
        self.strain = None
        self.id = None
        self.color = (0, 0, 0)
        self.period = None
        self.intensity = None
        self.recovery_probability = None
        self.death_probability = None
        self.properties ={
            'color': (0, 0, 0),
            'transmission_range': None,
            'transmission_rate': None,
            'incubation_period': None,
            'illness_period': None,
            'convalescence_period': None,
            'death_rate': None,
            'mutation_rate': None
        }
        self.clock = 0

class Influenza(Disease):

    def __init__(self, strain=''):
        super().__init__()
        self.name = 'Influenza'
        self.strain = strain
        self.id = self.name + '-' + self.strain
        self.color = (255, 255, 255)
        self.period = 0
        self.intensity = 0
        self.contagiousness = 0
        self.recovery_probability = 0
        self.death_probability = 0
        self.properties ={
            'color': (0, 0, 255),
            'transmission_range': 2,
            'transmission_rate': 0.25,
            'incubation_period': 2,
            'illness_period': 3,
            'convalescence_period': 3,
            'death_rate': 0.00004,
            'mutation_rate': 0.00005
        }
        self.test_mutation()
        self.init_period_dict()
        self.clock = 0

class Measles(Disease):

    def __init__(self, strain=''):
        super().__init__()
        self.name = 'Measles'
        self.strain = strain
        self.id = self.name + '-' + self.strain
        self.color = (255, 255, 255)
        self.period = 0
        self.intensity = 0
        self.contagiousness = 0
        self.recovery_probability = 0
        self.death_probability = 0
        self.properties ={
            'color': (238, 130, 238),
            'transmission_range': 5,
            'transmission_rate': 0.9,
            'incubation_period': 10,
            'illness_period': 10,
            'convalescence_period': 4,
            'death_rate': 0.15,
            'mutation_rate': 0.00005
        }
        self.test_mutation()
        self.init_period_dict()
        self.clock = 0

class Pneumonia(Disease):

    def __init__(self, strain=''):
        super().__init__()
        self.name = 'Test'
        self.strain = strain
        self.id = self.name + '-' + self.strain
        self.color = (255, 255, 255)
        self.period = 0
        self.intensity = 0
        self.contagiousness = 0
        self.recovery_probability = 0
        self.death_probability = 0
        self.properties ={
            'color': (255, 105, 180),
            'transmission_range': 2,
            'transmission_rate': 0.25,
            'incubation_period': 14,
            'illness_period': 7,
            'convalescence_period': 7,
            'death_rate': 0.075,
            'mutation_rate': 0.00005
        }
        self.test_mutation()
        self.init_period_dict()
        self.clock = 0

class Test(Disease):

    def __init__(self, strain=''):
        super().__init__()
        self.name = 'Test'
        self.strain = strain
        self.id = self.name + '-' + self.strain
        self.color = (255, 255, 255)
        self.period = 0
        self.intensity = 0
        self.contagiousness = 0
        self.recovery_probability = 0
        self.death_probability = 0
        self.properties ={
            'color': (255, 0, 0),
            'transmission_range': 2,
            'transmission_rate': 1,
            'incubation_period': 10,
            'illness_period': 10,
            'convalescence_period': 10,
            'death_rate': 0,
            'mutation_rate': 0
        }
        self.test_mutation()
        self.init_period_dict()
        self.clock = 0
