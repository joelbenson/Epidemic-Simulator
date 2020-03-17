from graphics import *
import numpy as np
from population import Population
from disease import *
import random
import time


def main():

    #WINDOW PARAMETERS
    WINDOW_SIZE = (1440, 855) #1440, 855
    MAX_FRAME_RATE = 0 #0 for no frame delay

    #POPULATION AND DISEASE PARAMETERS
    POPULATION_DIMS = (140, 85)
    DISEASES = [Influenza(), Measles(), Pneumonia(), Custom()] #To change properties of custom disease,
    NUM_CASES = [1, 0, 0, 0]                                   #see end of disease.py


    #Initialize window
    window = GraphWin(title="Epidemic Simulation", width = WINDOW_SIZE[0],
                    height=WINDOW_SIZE[1], autoflush=False)

    window.setCoords(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])


    #Initialize Population
    population = Population(POPULATION_DIMS, window)

    #Initialize Population diseases
    population.init_diseases(DISEASES, NUM_CASES)

    population.draw()
    time.sleep(MAX_FRAME_RATE)

    #Repeat spread computation until user quits window
    while(not window.isClosed()):

        #Get next population state
        population.next_state()

        #Update window
        update()

        time.sleep(MAX_FRAME_RATE)

    return

if __name__ == "__main__":
    main()
