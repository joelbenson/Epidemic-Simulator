from graphics import *
import numpy as np
import random
from collections import Counter
from disease import DiseaseState, Healthy, Deceased, Influenza, Measles, Pneumonia
import copy

class Agent:

    def __init__(self, rectangle, population_coordinates, window_coordinates, size):
        self.rectangle = rectangle
        self.population_coordinates = population_coordinates
        self.window_coordinates = window_coordinates
        self.size = size
        self.exposures = {}
        self.disease_state = DiseaseState()
        self.immunities = set()


    def draw(self, window):

        self.update_image()
        self.rectangle.draw(window)

        return

    def contract_disease(self, disease):

        #Copy disease
        new_disease = copy.deepcopy(disease)

        #Reset disease timeline
        new_disease.reset()

        #Set disease state
        self.disease_state.state = new_disease

        #Update agent immunities
        self.immunities.add(disease.get_info()['id'])

        return


    def update_image(self):

        color = self.disease_state.state.get_info()['color']
        self.rectangle.setFill(color_rgb(color[0], color[1], color[2]))
        self.rectangle.setOutline(color_rgb(color[0], color[1], color[2]))

        return


    def next_state(self):

        #Update current state as result of time
        self.disease_state.next_state()

        #Update current state as result of neighboring disease
        self.update_state()

        #Update the image and agent immunity
        self.update_image()

        return


    def update_state(self):

        #Get current disease
        current_disease = self.disease_state.state

        #Compute next state based on neighbor influence and current disease state
        if (current_disease.get_info()['name'] == 'Healthy'):

            exposures = list(self.exposures.keys())
            neighbor_disease_counts = list(self.exposures.values())

            #If no neighbor diseases, do nothing
            if (not exposures):
                return

            #Otherwise, for each disease and instance from neighbor, determine whether disease was attained
            infected = False
            for i in range(len(exposures)):

                if (infected): break

                neighbor_disease = exposures[i]

                #If agent has immunity, skip this disease
                if (neighbor_disease.get_info()['id'] in self.immunities):
                    continue

                #Test for each neighbor with disease
                for j in range(neighbor_disease_counts[i]):

                    fate = random.random()

                    if (fate < neighbor_disease.get_info()['transmission_rate']):

                        self.contract_disease(neighbor_disease)

                        infected = True

                        continue

        return


    def spread_disease(self, population):

        #Spread agent's current disease to neighbors for next time
        disease = self.disease_state.state
        transmission_range = disease.get_info()['transmission_range']

        #If disease has range, spread to neighbors
        if(transmission_range > 0):

            #Get list of neighbor indexes within range
            neighbor_indexes = self.get_neighbors_in_range(transmission_range, population)

            #For each neighbor in neighborhood, add count of current disease
            for neighbor_index in neighbor_indexes:

                neighbor_agent = population[neighbor_index]

                #Increment or initialize disease in neighbor disease save dict,
                if (disease not in neighbor_agent.exposures.keys()):

                    neighbor_agent.exposures[disease] = 1

                else:

                    neighbor_agent.exposures[disease] += 1

        return


    def get_neighbors_in_range(self, transmission_range, population):

        i, j = self.population_coordinates
        x_p, y_p = population.shape

        #Get square block within relative indexes of nieghbors
        neighborhood_shape = (transmission_range*2 + 1, transmission_range*2+1)
        neighborhood_center = (transmission_range, transmission_range)
        neighborhood_array = np.empty(shape=neighborhood_shape, dtype=object)

        for x in range(neighborhood_shape[0]):
            for y in range(neighborhood_shape[1]):
                x_index = x - neighborhood_center[0]
                y_index = y - neighborhood_center[1]
                neighborhood_array[x][y] = (x_index, y_index)

        neighbor_indexes = []

        #Iterate through indexs and check for: relative euclidean distance less than range, final index within pop.
        for x in range(neighborhood_shape[0]):
            for y in range(neighborhood_shape[1]):

                relative_index = neighborhood_array[x][y]

                neighbor_index = ((i + relative_index[0]) % x_p, (j + relative_index[1]) % y_p)
                
                #If index is the center, continue
                if (relative_index == (0, 0)):
                    continue

                within_distance = ((float(relative_index[0]**2) + float(relative_index[1]**2)) ** 0.5) <= transmission_range

                if (within_distance):

                    neighbor_indexes.append(neighbor_index)

        return neighbor_indexes
