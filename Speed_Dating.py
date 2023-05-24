import random
import sys
from osbrain import Agent, run_agent, run_nameserver
from time import sleep

# List of interests
lst_in = [
    "F1", "Gaming", "Sports", "Pandas", "Books", "Movies",
    "Coding", "Art", "Theater", "Fashion", "Music", "Travelling",
    "Cooking", "Dancing", "Netflix", "Cars", "Photography", "Fitness"
]
# List of names
NAMES = ['Aarav', 'Aanya', 'Advait', 'Suresh', 'Aisha', 'Aryan', 'Diya',
             'Ishaan', 'Hari', 'Kavya', 'Mohammed', 'Vardan', 'Pranav', 'Riya',
             'Sangeetha', 'Sara', 'Shaurya', 'Shreya', 'Vihaan', 'Vivek']


# Initiator Agent
class InitiatorAgent(Agent):
    interest_count = 0
    prefs = []

    def select_prefs(self):
        self.name = random.choice(NAMES)
        NAMES.remove(self.name)  # Remove the name from the list of available names
        self.prefs = random.sample(lst_in, self.interest_count)
        print(f"InitiatorAgent {self.name} initiated with topics: {self.prefs}")


    def ask_if_like(self):
        interest = random.choice(self.prefs)
        self.log_info(f'Hey ! Do you like {interest} ?')
        self.send('ask', f'Hey ! Do you like {interest} ?')

    def receive_reply(self, message):
        sender = message.split(' ')[0]
        reply = message.split(' ')[1]
        self.log_info(f'{sender} replied {reply}')

        if reply == 'YES':
            self.send('match_notify_channel', f'{self.name} {sender}')


# Responder Agent
class ResponderAgent(Agent):
    interest_count = 0
    prefs = []

    def select_prefs(self):
        self.name = random.choice(NAMES)
        NAMES.remove(self.name)  # Remove the name from the list of available names
        self.prefs = random.sample(lst_in, self.interest_count)
        print(f"ResponderAgent {self.name} initiated with topics: {self.prefs}")

    def reply_to_question(self, message):
        asked_interest = message.split(' ')[-2]
        #self.log_info(asked_interest)

        if asked_interest in self.prefs:
            self.log_info(f'YES, I like {asked_interest}')
            self.send('reply', f'{self.name} YES')
        else:
            self.log_info(f'NO, I don\'t like {asked_interest}')
            self.send('reply', f'{self.name} NO')


# Organizer Agent
class SpeedDateOrganizer(Agent):
    def on_init(self):
        # Initialization
        print("\nSwipe, smile, match, love at first sight!\nThe Speed Dating event has begun\n")
        self.hasEnded = False
        
        self.num_couples = 0
        self.interest_count = 0
        self.current_turn = 1
        self.responder_agents = []
        self.initiator_agents = []
        self.matched = False

    def initialize_agents(self):
        # Initialize initiator and responder agents
        for i in range(self.num_couples):
            initiator_agent = run_agent(f'InitiatorAgent{i}', base=InitiatorAgent)
            responder_agent = run_agent(f'ResponderAgent{i}', base=ResponderAgent)

            initiator_agent.interest_count = self.interest_count
            responder_agent.interest_count = self.interest_count

            initiator_agent.select_prefs()
            responder_agent.select_prefs()

            match_notify_address = initiator_agent.bind('PUSH', alias="match_notify_channel")
            self.connect(match_notify_address, handler='match_confirmed')

            self.responder_agents.append(responder_agent)
            self.initiator_agents.append(initiator_agent)

            responder_agent.connect(match_notify_address, handler='reply_to_question')
            initiator_agent.connect(match_notify_address, handler='receive_reply')

    def start_dating(self):
        # Start the dating process for each turn
        if self.matched:
            self.stop()
            return

        if self.current_turn > self.num_couples:
            self.log_info('It seems like Cupid needs to work on their aim today! No love sparks flew between the couples.')
            self.stop()
            return

        self.log_info(f'\n\t ~~Turn {self.current_turn}~~')

        for i in range(self.num_couples):
            initiator_agent = self.initiator_agents[(i + self.current_turn - 1) % self.num_couples]
            initiator_agent_address = initiator_agent.bind('PUSH', alias='ask')

            responder_agent = self.responder_agents[i]
            responder_agent_address = responder_agent.bind('PUSH', alias='reply')

            responder_agent.connect(initiator_agent_address, handler='reply_to_question')
            initiator_agent.connect(responder_agent_address, handler='receive_reply')

            initiator_agent.ask_if_like()
            sleep(1)

            responder_agent.close('reply')
            initiator_agent.close('ask')

        self.current_turn += 1

    def match_confirmed(self, message):
        # Handle match confirmation
        if not self.matched:
            self.matched = True
            self.log_info(f"{message.split(' ')[0]} and {message.split(' ')[1]} proudly claim the title of the ultimate 'first-to-match' couple")


if __name__ == '__main__':
    # Main program

    # User input for the number of couples and interests
    num_couples = int(input("Enter the number of couples: "))
    interest_count = int(input("Enter the number of interests: "))

    ns_sock = run_nameserver()

    organizer_agent = run_agent('SpeedDateOrganizer', base=SpeedDateOrganizer)
    organizer_agent.num_couples = num_couples
    organizer_agent.interest_count = interest_count
    organizer_agent.initialize_agents()

    try:
        while organizer_agent.is_running():
            organizer_agent.start_dating()
    finally:
        ns_sock.shutdown()
