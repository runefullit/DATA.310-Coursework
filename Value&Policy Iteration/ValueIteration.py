
from enum import Enum, auto
import numpy as np

A = 0.64
B = 1 - A
C = 0.69
D = 1 - C
E = 0.99
F = 1 - E
DISCOUNT = 0.2
EPSILON = 0.01

class State(Enum):
    STANDING = auto()
    FALLEN = auto()
    MOVING = auto()

class Action(Enum):
    
    FAST = auto()
    SLOW = auto()

class StateDoesNotExistException(Exception):
    pass

class IllegalActionException(Exception):
    pass

def valueIteration(values):
    """Value iterate on given Markov decision problem."""
    states = [State.STANDING, State.FALLEN, State.MOVING]
    newValues = [0,0,0]
    for state in states:
        actionVals = []
        for action in actions(state):
            actionVals.append(np.sum(np.multiply(
                np.array(transit(state, action)),
                np.add(
                    np.array(reward(state, action)),
                    DISCOUNT * np.array(values)
                )    
            )))
        newValues[state.value - 1] = max(actionVals)
    return newValues

def actions(state):
    """Return a list of possible actions given state"""
    match state:
        case State.STANDING | State.MOVING:
            return [Action.FAST, Action.SLOW]
        case State.FALLEN:
            return [Action.SLOW]
        case other:
            raise StateDoesNotExistException

def transit(state,action):
    """Return a list of probabilities for next state after action."""
    match state:
        case State.STANDING:
            if action == Action.FAST:
                return [
                    0, # Probablility of returning to State.Standing
                    B, # Porobability of landing in Fallen
                    A, # Probability of landing in Moving
                ]
            elif action == Action.SLOW:
                return [
                    0,
                    0,
                    1
                ]
            else:
                raise IllegalActionException
        case State.FALLEN:
            if action == Action.SLOW:
                return [
                    C,
                    D,
                    0
                ]
            else:
                raise IllegalActionException
        case State.MOVING:
            if action ==  Action.FAST:
                return [
                    0,
                    F,
                    E
                ]
            elif action == Action.SLOW:
                return [
                    0,
                    0,
                    1
                ]
            else:
                raise IllegalActionException

def reward(state, action):
    """Return the rewards for the end states given action"""
    match state:
        case State.STANDING:
            if action == Action.FAST:
                return [
                    0, # Probablility of returning to State.Standing
                    -1, # Probability of landing in Fallen
                    2, # Probability of landing in Moving
                ]
            elif action == Action.SLOW:
                return [
                    0,
                    0,
                    1
                ]
            else:
                raise IllegalActionException
        case State.FALLEN:
            if action == Action.SLOW:
                return [
                    1,
                    -1,
                    0
                ]
            else:
                raise IllegalActionException
        case State.MOVING:
            if action ==  Action.FAST:
                return [
                    0,
                    -1,
                    2
                ]
            elif action == Action.SLOW:
                return [
                    0,
                    0,
                    1
                ]
            else:
                raise IllegalActionException

    
    


def main():

    v = [0,0,0]
    i = 0
    while True:
        vNew = valueIteration(v)
        theta = np.abs(np.array(vNew) - np.array(v))
        print(theta)
        v = vNew
        i += 1
        # Making sure that all states are iterated to exhaustion.
        if np.max(theta) <= EPSILON:
            break
    print(f"After {i} iterations, values are {v}")

if __name__ == "__main__":
    main()