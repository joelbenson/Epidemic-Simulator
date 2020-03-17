from graphics import *
import numpy as np
from population import Population
from disease import *
import random
import time


def main():

    #WINDOW PARAMETERS
    WINDOW_SIZE = (1000, 800) #1440, 855
    MAX_FRAME_RATE = 0 #0 for no frame delay

    #POPULATION AND DISEASE PARAMETERS
    POPULATION_DIMS = (100, 80)
    DISEASES = [Influenza(), Measles(), Pneumonia(), Test()]
    #TO DEFINE NEW DISEASES, SEE DISEASE.PY AND DEFINE A CLASS SIMILAR TO THOSE ABOVE, AND ADD TO DISEASES LIST
    NUM_CASES = [0, 1, 0, 0]


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
    while(True):

        #Get next population state
        population.next_state()

        #Update window
        update()

        time.sleep(MAX_FRAME_RATE)

    return

if __name__ == "__main__":
    main()
