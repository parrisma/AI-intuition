import logging
import random

from lib.reflrn.interface.Agent import Agent
from lib.reflrn.interface.State import State


class TestAgent(Agent):

    def __init__(self,
                 agent_id: int,  # immutable & unique id for this agent
                 agent_name: str,  # immutable & unique name for this agent
                 lg: logging):
        self.__lg = lg
        self.__id = agent_id
        self.__name = agent_name
        return

    # Return immutable id
    #
    def id(self):
        return self.__id

    # Return immutable name
    #
    def name(self):
        return self.__name

    #
    # Environment call back when environment shuts down
    #
    def terminate(self,
                  save_on_terminate: bool = False):
        self.__lg.debug(self.__name + " Environment Termination Notification")
        return

    #
    # Environment call back when episode starts
    #
    def episode_init(self, state: State):
        self.__lg.debug(self.__name + " Episode Initialisation Notification  : ")
        return

    #
    # Environment call back when episode is completed
    #
    def episode_complete(self, state: State):
        self.__lg.debug(self.__name + " Episode Complete Notification  : ")
        return

    #
    # Environment call back to ask the agent to chose an action
    #
    # State : The current representation of the environment
    # possible_actions : The set of possible actions the agent can play from this curr_coords
    #
    @classmethod
    def chose_action(cls, state: State, possible_actions: [int]) -> int:
        # Test agent just selects a random action
        return random.choice(possible_actions)

    #
    # Environment call back to reward agent for a play chosen for the given
    # state passed.
    #
    def reward(self, state: State, next_state: State, action: int, reward_for_play: float, episode_complete: bool):
        self.__lg.debug(self.__name + " reward  : " + str(reward_for_play) + " for action " + str(action))
        if episode_complete:
            self.__lg.debug(self.__name + " Episode Completed")
        return

    #
    # Called by the environment *once* at the start of the session
    # and the action set is given as dictionary
    #
    def session_init(self,
                     actions: dict) -> None:
        self.__lg.debug(self.__name + " Session Initialisation Notification  : ")
        return

    #
    # Produce debug details when performing operations such as action prediction.
    #
    @property
    def explain(self) -> bool:
        raise NotImplementedError()

    @explain.setter
    def explain(self, value: bool):
        raise NotImplementedError()
