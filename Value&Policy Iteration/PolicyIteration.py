
from enum import Enum, auto
import numpy as np

A = 0.90
B = 1 - A
C = 0.61
D = 1 - C
E = 0.94
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
                    0, # reward for ending up in Standing
                    -1, # Fallen
                    2, # Moving
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

def policyIteration2(policy, values):
    states = [State.STANDING, State.FALLEN, State.MOVING]
    iterations = 1
    while True:
        # Policy Evaluation
        delta = np.inf
        # Pretty sure this was the exit condition, both solutions
        # rounded to the same answer.
        theta = EPSILON # * (1 - DISCOUNT)/DISCOUNT
        while delta >= theta:
            delta = 0
            for state in states:
                temp = values[state.value-1]
                values[state.value-1] = np.sum(
                        np.multiply(
                            np.array(transit(state, policy[state.value-1])),
                            np.add(
                                np.array(reward(state, policy[state.value-1])),
                                DISCOUNT * np.array(values)
                            )
                        )
                    )
                delta = max([delta, np.abs(temp - values[state.value-1])])
        
        # Policy Improvement
        policyStable = True
        for state in states:
            temp = policy[state.value-1]
            maxResult = []
            for action in actions(state):
                maxResult.append(np.sum(
                    np.multiply(
                        np.array(transit(state, action)),
                        np.add(
                            np.array(reward(state, action)),
                            DISCOUNT * np.array(values)
                        )
                    )
                ))
            policy[state.value-1] = actions(state)[np.argmax(maxResult)]
            if policy[state.value-1] != temp:
                policyStable = False
        print(f"Iteration {iterations}")
        iterations += 1
        if policyStable:
            return policy, values


def main():
    v = [0,0,0]
    policy = [Action.SLOW, Action.SLOW, Action.SLOW]
    # for _ in range(20):
    #     v, newPolicy = policyIteration(policy, v)
    #     # Iterate until the policy no longer changes
    #     if newPolicy == policy:
    #         break
    #     policy = newPolicy
    policy,v = policyIteration2(policy,v)
    print(f"Values are {v}, and policy {policy}")

if __name__ == "__main__":
    main()