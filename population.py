from graphics import *
from agent import Agent
from disease import *
import numpy as np
import random
import copy

class Population():

    def __init__(self, shape, window):

        self.shape = shape
        self.agent_array = np.empty(shape=(shape[0], shape[1]), dtype=object)
        self.window = window
        self.init_agents()


    def init_agents(self):
        window = self.window

        cell_x = window.width / self.shape[0]
        cell_y = window.height / self.shape[1]

        #Initialize agents
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):

                x = i * (window.width / self.shape[0])
                y = j * (window.height / self.shape[1])

                agent_rectangle = Rectangle(Point(x, y), Point(x + cell_x, y + cell_y))
                agent_population_coordinates = (i, j)
                agent_window_coordinates = (x, y)
                agent_size = (cell_x, cell_y)

                self.agent_array[i][j] = Agent(agent_rectangle, agent_population_coordinates, agent_window_coordinates, agent_size)

        return


    def init_diseases(self, diseases, num_cases):

        #For each disease, choose random spot for each case
        for index, disease in enumerate(diseases):
            for i in range(num_cases[index]):

                fate_x = np.random.choice(range(self.shape[0] - 1))
                fate_y = np.random.choice(range(self.shape[1] - 1))

                self.agent_array[fate_x][fate_y].contract_disease(disease)

        return


    def draw(self):

        for row in self.agent_array:
            for agent in row:
                agent.draw(self.window)

        return


    def next_state(self):

        #Spread disease
        self.spread_disease()

        #Update agent states
        self.update_agent_states()

        return


    def spread_disease(self):

        for row in self.agent_array:
            for agent in row:

                agent.spread_disease(self.agent_array)

        return


    def update_agent_states(self):

        for row in self.agent_array:
            for agent in row:

                agent.next_state()

        return
