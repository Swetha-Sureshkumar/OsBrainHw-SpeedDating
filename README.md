# Speed Dating Simulation
This is a mini-system implemented using the osBrain platform to simulate a speed dating event. The simulation consists of two types of agents: initiators and responders.

## Overview
1.The number of initiators and responders is equal, and it can be configured as a parameter of the simulation.
2.The simulation includes an organizer agent responsible for assigning initiators their interlocutors.
3.Initiators initiate conversations by sending messages to their assigned responders.
4.Responders passively wait for messages and reply accordingly.
5.The conversation is a simple message exchange, where initiators ask a random question based on their assigned interests, and responders reply with a "Yes" or "No" answer.
6.Each initiator and responder is assigned a set of random interests from a predefined list.
7.The organizer agent periodically assigns new interlocutors to initiators, signaling the start of a new round.
8.If an initiator receives a confirmation message from a responder, they notify the organizer agent.
9.The organizer agent gracefully shuts down the simulation when the first match is found, announcing the agents who matched.

Please note that the osBrain platform is required to run the simulation. Make sure to install the necessary dependencies before running the code.

Enjoy the speed dating simulation!

