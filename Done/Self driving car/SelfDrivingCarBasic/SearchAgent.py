import random
import math
from environment import Agent, Environment
from simulator import Simulator
import sys
from searchUtils import searchUtils

class SearchAgent(Agent):
    """ An agent that drives in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env,location=None):
        super(SearchAgent, self).__init__(env)     # Set the agent in the evironment 
        self.valid_actions = self.env.valid_actions  # The set of valid actions
        self.state_sequence=[]
        self.openList = [] 
        self.closedList = [] 
        self.searchutil = searchUtils(env)

    def getNextState(self,state,action):
        #//returns the next state of the car if it takes action a in state s
        return self.env.applyAction(self,state,action)

    def retrievePathFromState(self,state):
        #//retrieves the path taken to reach state s
        return self.searchutil.retrievePathFromState(state)

    def get_hVal(self,start,goal):
        #//computes the heuristic cost from start to goal state
        locstart=start["location"]
        locgoal=goal["location"]
        #forward-2x so use /2 while computing distance to goal
        return (1.0*math.fabs(locstart[0]-locgoal[0])+math.fabs(locstart[1]-locgoal[1]))/2

    def updateHeuristicValue(self,nextState,ghval):
        #//updates the heuristic value of nextState as ghval (g is black number, h is red number)
         if(self.searchutil.isPresentStateInList(nextState, self.closedList)==0 and self.searchutil.isPresentStateInPriorityList(nextState, self.openList)==0):
             self.openList=self.searchutil.insertStateInPriorityQueue(self.openList, nextState, ghval)

                        #If present in openlist, check if the value needs to be updated. If yes, update the value and reinsert into queue
                        #at the correcct position
                        
         elif self.searchutil.isPresentStateInPriorityList(nextState, self.openList):
             self.openList=self.searchutil.checkAndUpdateStateInPriorityQueue(self.openList,nextState,ghval)
   
    def getBestStateToMove(self):
        #//returns the best state to move based on current gval+hval
        current = self.openList[0]
        self.openList.remove(current)
        self.closedList.append(current[0])   
        return current[0]
  
    def isGoal(self,current):
        #//returns true if current state is the goal state
        goalState =self.env.getGoalState()
        return current["location"] == goalState["location"]
        
    def isThrereAnUnexploredState(self):
        #//returns true if there is an unexplored state
        return len(self.openList) > 0
        
    def aStarSearch(self,startstate,goalState):
        #//car doesn't move if this function is empty
        #//only path and startstate were here originally
        #//visibility is 5 cells in all directions
        #//assume no obstacles are present outside the visibility range
        #// arrange the 7 functions such that you can do an A* search
        
        path=[]
        #Initialize startState gval to 0 
        startstate["gVal"]=0
       
        #update the heuristic value for current state - call updateHeuristicValue function with current state and gval+hval
        #//1.Update the heuristic value for the startstate (calculate the diff between start state and next state iirc)
        #//So essentially we're calculating g + h for start state
        self.updateHeuristicValue(startstate,startstate["gVal"]+self.get_hVal(startstate,goalState))
        
        #2.Loop till there is no unexplored state.
        #while():
        while (self.isThrereAnUnexploredState()):
                #3.get best state to move  and store it in a variable currentState
                #//Whichever has the least cost
                currentState = self.getBestStateToMove()
               
                #4.Check if currentState is goal, if yes retrieve path by passing currentState to the function, store the result in path variable and break the loop.
                if self.isGoal(currentState):
                    path = self.retrievePathFromState(currentState)
                    break
                
                #5.Iterate overall valid actions and get the next state which will be obtained on taking that action in currentState.
                #//generate next possible state
                #6.for act in self.valid_actions:
                for act in self.valid_actions:
                #//list of all actions that are possible
                    nextState = self.getNextState(currentState, act)
                 
                    #7.Update the gval for nextState as currentState gval +1
                    nextState["gVal"] = currentState["gVal"]+1
                       
                    #8.Update the heuristic value for next state by passing nextState and nextState's gval+hval
                    self.updateHeuristicValue(nextState, nextState["gVal"]+ self.get_hVal(nextState,goalState))
        
        #//9. Return the computed path
        return path

    def computePath(self):
        startstate = self.state
        goalstate =self.env.getGoalState()
       
        self.state_sequence=[]
        self.openList = [] 
        self.closedList = [] 
        self.state_sequence = self.aStarSearch(startstate,goalstate)
        self.env.optimalpath = self.state_sequence


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action. """
        action = None
        if len(self.state_sequence) >=2:
            action = self.env.getAction(self.state_sequence[0],self.state_sequence[1])
        self.state = self.env.act(self,action)        
        return
        

def run(filename):
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    env = Environment(config_file=filename,fixmovement=True)
    
    agent = env.create_agent(SearchAgent)
    env.set_primary_agent(agent)
    
    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    sim = Simulator(env, update_delay=2,display=True)
    
    ##############
    # Run the simulator
    ##############
    sim.run()


if __name__ == '__main__':
    run(sys.argv[1])
