import os
from maze import *
from turtle import *
from datetime import datetime
import math

"""Solver for the turtle maze assignment"""
"""2019-03-19, Fredrik Julin, Maze solver"""
"""
    --README SECTION--
    Note: One of the hardest problems with this assignment is that the agent returns
    to face the same position after moving in any direction. It makes implementing
    very simple algorithms by using rules such as "left hand rule" and so on harder. Another problem
    is that the agent does not return "False" when making an invalid move when cirle level goes below
    50, it simply returns true. Also we do not have access to the grid and its positions in
    the maze which means we cannot perform informed searches where the environment is fully observable.
    The algorithm I have implemented takes inspiration from tremauxs algorithm. See the link for a cool
    explanation and interactive example -> http://blog.jamisbuck.org/2014/05/12/tremauxs-algorithm.html

    NOTE: I did change the Backward() function in the maze.py slightly(added an else statement and a
    return False). This is because if not the function will return True even though the agent enters an
    invalid position as explained earlier in this initial comment section. Enjoy!
"""
#Variables
deadend = set() #Set with all the deadends
partiallyExplored = {} #Dictionary with all the partially explored junctions positions
visitedStack = [] # list used as a stack to be able to backtrack and check the last move made
    
#1 = left, 2 = forward, 3 = right, 4 = backward
#Updates a dictionary that binds a unique position to a list of numbers representing
#the directions in the maze. If we have been at all of them, we mark the junction as a deadend
#and use the backtrack() function in escape() to go back the way we came.
def updateExplored(position, closedDirection):
    explored = partiallyExplored.get(position)
    if explored == None:
        newEntry = {position : [closedDirection]}
        partiallyExplored.update(newEntry)
    else: 
        if closedDirection not in explored:
            explored.append(closedDirection)
            newEntry = {position : explored}
            partiallyExplored.update(newEntry)
            if (1 in explored) and (2 in explored) and (3 in explored) and (4 in explored):
                deadend.add(position)
                print("Updated position: {} as a deadend".format(position))
                del partiallyExplored[position]

#Returns true is we hit a deadend, false otherwise
def isDeadend(position):
    if position in deadend:
        return True
    return False

#1 = left, 2 = forward, 3 = right, 4 = backward
#Returns true if the given direction has not been explored yet
#Arguments: position(agents current position)
def isNotExplored(position, direction):
    isExplored = partiallyExplored.get(position)
    if isExplored is None:
        return True
    if(direction not in isExplored):
        return True
    return False

#1 = left, 2 = forward, 3 = right, 4 = backward
#Tries to move in a direction. If the direction has been visited before or it is 
#the same passage as the one we came from, we skip it. If all passages has been explored
#we should never enter this function but get stuck in the isDeadEnd and start backtracking()
#Arguments: position(the agents current position), cameFrom(an integer representing last the last move)
def move(position, cameFrom):
    if isNotExplored(position, 1): #If left passage has not been explored
        if(cameFrom != 3): # And we did not come from the Right
            updateExplored(position,1)
            if(Left(agent)): #Then we try move left
                print("Moving left")
                visitedStack.append(1)
                return True
        updateExplored(position, 1) #We say this junction has been explored to the left

    if isNotExplored(position, 2): #If forward passage has not been explored
        if(cameFrom != 4): #And we did not come from the backward
            updateExplored(position, 2)
            if(Backward(agent)): #Then try move forward
                print("Moving backward")
                visitedStack.append(2)
                return True
        updateExplored(position, 2) #We say this junction has been explored forward

    if isNotExplored(position, 3): #If the Right passage has not been explored
        if(cameFrom != 1): #And we did not come from the Left
            updateExplored(position,3)
            if(Right(agent)): #Then try move Right
                print("Moving Right")
                visitedStack.append(3)#Add Right to our last visited location onto the stack
                return True
        updateExplored(position, 3) #We say this junction has been explored to the right

    if isNotExplored(position, 4): #If backward has not been explored
        if(cameFrom != 2): #And we did not come from the forward passage
            updateExplored(position,4)
            if(Forward(agent)): #Then try move Backward
                print("Moving Forward")
                visitedStack.append(4) #Add backward to our last visited location onto the stack
                return True
        updateExplored(position, 4) #We say this junction has been explored backwards

#1 = left, 2 = forward, 3 = right, 4 = backward
#Retraces the steps if a deadend is hit or a place that has been marked twice
def backtrack():
    cameFrom = visitedStack.pop()
    if cameFrom == 1:
        Right(agent)
        agentPosition = (math.floor(agent.xcor()), math.floor(agent.ycor()))
        updateExplored(agentPosition, 1)
    if cameFrom == 2:
        Forward(agent)
        agentPosition = (math.floor(agent.xcor()), math.floor(agent.ycor()))
        updateExplored(agentPosition, 2)
    if cameFrom == 3:
        Left(agent)
        agentPosition = (math.floor(agent.xcor()), math.floor(agent.ycor()))
        updateExplored(agentPosition, 3)
    if cameFrom == 4:
        Backward(agent)
        agentPosition = (math.floor(agent.xcor()), math.floor(agent.ycor()))
        updateExplored(agentPosition, 4)

#Main function to get out of the maze, see ultility functions for more info on
#how these smaller parts operate
def escape():
    while not isSuccess(): #While we are still in the maze
        agentPosition = (math.floor(agent.xcor()), math.floor(agent.ycor())) #Get agent x,y position
        if(isDeadend(agentPosition)): #Have we hit a deadend?
            print("Hit a deadend, turning back!")
            backtrack() #Let's go back!
            continue #Backtracking finishes, lets jump to the next iteration
        else:
            if visitedStack:
                lastMove = visitedStack.pop() #Grab the last move we made
                visitedStack.append(lastMove) #Put it back on the stack for further use
                move(agentPosition, lastMove) #Try move in a certain direction   
            else:                             
                move(agentPosition, None)     #First move we make(No earlier movement done)
    print("WE DID IT!")


if __name__ == '__main__':
    # Maze
    screen = Screen()
    sampleMaze()

    # Agent Init
    agent = Turtle()
    init_agent(agent)
    start = datetime.now()
    escape()
    finish = datetime.now()

    # Result
    print(os.path.basename(__file__).split('.')[0])
    print('Result   : Pass') if isSuccess() else print('Result   : Fail')
    print('Duration :', finish-start)
    input() #Just to stop the program so we can see the maze


