import random

class DiseaseState():

    def __init__(self):
        self.state = Healthy()


    def next_state(self):

        #Tick disease clock
        self.state.clock += 1

        #Test for recovery
        fate = random.random()
        if (fate < self.state.get_info()['recovery_rate']):
            self.state = Healthy()
            return

        #Test for deceased
        fate = random.random()
        if (fate < self.state.get_info()['death_rate']):
            self.state = Deceased()
            return

        return



class Disease():

    def __init__(self):
        self.name = None
        self.strain = None
        self.id = None
        self.properties = {}
        self.clock = 0

    def get_info(self):

        return {
            'name': self.name,
            'strain': self.strain,
            'id': self.id,
            'color': self.properties['color'],
            'transmission_range': self.properties['transmission_range'],
            'transmission_rate': self.properties['transmission_rate'],
            'recovery_rate': self.properties['recovery_rate'],
            'death_rate': self.properties['death_rate'],
            'mutation_rate': self.properties['mutation_rate']
        }

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
                print(fate)

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

    def reset(self):

        #Reset disease clock
        self.clock = 0

        #Possibly mutate
        self.test_mutation()

        return

class Healthy(Disease):

    def __init__(self, strain=''):
        super().__init__()
        self.name = 'Healthy'
        self.strain = strain
        self.id = self.name + '-' + self.strain
        self.properties ={
            'color': (255, 255, 255),
            'transmission_range': 0,
            'transmission_rate': 0,
            'recovery_rate': 1,
            'death_rate': 0,
            'mutation_rate': 0
        }


class Deceased(Disease):

    def __init__(self, strain=''):
        super().__init__()
        self.name = 'Deceased'
        self.strain = strain
        self.id = self.name + '-' + self.strain
        self.properties ={
            'color': (0, 0, 0),
            'transmission_range': 0,
            'transmission_rate': 0,
            'recovery_rate': 0,
            'death_rate': 1,
            'mutation_rate': 0
        }


class Influenza(Disease):

    def __init__(self, strain=''):
        super().__init__()
        self.name = 'Influenza'
        self.strain = strain
        self.id = self.name + '-' + self.strain
        self.properties ={
            'color': (0, 0, 255),
            'transmission_range': 2,
            'transmission_rate': 0.25,
            'recovery_rate': 0.125,
            'death_rate': 0.00004,
            'mutation_rate': 0.0005
        }
        self.test_mutation()

class Measles(Disease):

    def __init__(self, strain=''):
        super().__init__()
        self.name = 'Measles'
        self.strain = strain
        self.id = self.name + '-' + self.strain
        self.properties ={
            'color': (238,130,238),
            'transmission_range': 5,
            'transmission_rate': 0.9,
            'recovery_rate': 0.111,
            'death_rate': 0.15,
            'mutation_rate': 0.00009
        }
        self.test_mutation()

class Pneumonia(Disease):

    def __init__(self, strain=''):
        super().__init__()
        self.name = 'Measles'
        self.strain = strain
        self.id = self.name + '-' + self.strain
        self.properties ={
            'color': (255, 105, 180),
            'transmission_range': 2,
            'transmission_rate': 0.25,
            'recovery_rate': 0.07,
            'death_rate': 0.075,
            'mutation_rate': 0.0005

        }
        self.test_mutation()

class Test(Disease):

    def __init__(self, strain=''):
        super().__init__()
        self.name = 'Measles'
        self.strain = strain
        self.id = self.name + '-' + self.strain
        self.properties ={
            'color': (122, 122, 122),
            'transmission_range': 3,
            'transmission_rate': 1,
            'recovery_rate': 0.3,
            'death_rate': 0,
            'mutation_rate': 0

        }
        self.test_mutation()
