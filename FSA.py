class FSAError(Exception):
    pass

class FSA:
    def __init__(self, instance_id, initial_state=None, states=set(), final_states=set(), input_actions=set()):
        self.instance_id = instance_id

        if states == None:
            raise ValueError("States argument can't be None")
        self.states = set()
        self.initial_state = initial_state
        for s in states:
            self.add_state(s)

        self.final_states = set()
        for s in final_states:
            self.add_state(s, True)

        self.input_actions = set()
        for ia in input_actions:
            self.add_input_action(ia)

        if self.initial_state != None:
            self.states.add(self.initial_state)

        self.state_links = {}
        self.current_state = self.initial_state
        self.end_state = None
        self.instance_status = "created"

    def set_init_state(self, state):
        if not state in self.states:
            raise ValueError(f"State '{state}' does not exists'")
        self.initial_state = state

    def add_state(self, state, is_final=False):
        if state == None:
            raise ValueError(f"'{state}' is not an accepted value for a state")
        self.states.add(state)
        if is_final:
            self.final_states.add(state)
        if self.initial_state == None:
            self.initial_state = state
    
    def add_input_action(self, input_action):
        if input_action == None:
            raise ValueError(f"'{input_action}' is not accepted value for an input action")
        self.input_actions.add(input_action)

    def link_states(self, from_state, input_action, to_state):
        if not from_state in self.states:
            raise ValueError(f"State '{from_state}' does not exists'")
        if not to_state in self.states:
            raise ValueError(f"State '{to_state}' does not exists'")
        if not input_action in self.input_actions:
            raise ValueError(f"Input action '{input_action}' does not exists'")

        self.state_links[(from_state, input_action)] = to_state

    def do_action(self, input_action):
        if self.end_state != None or self.initial_state == None or self.current_state == None:
            raise FSAError()
        if not input_action in self.input_actions:
            raise ValueError(f"Input action '{input_action}' does not exists'")
        new_state = self.state_links[(self.current_state, input_action)]
        if new_state == None:
            raise ValueError(f"State '{self.current_state}' does not have action '{input_action}'")
        self.current_state = new_state
        self.instance_status = "running"
    
    def end_instance(self):
        if not self.current_state in self.final_states:
            raise ValueError(f"State '{self.current_state}' is not a final state")
        self.end_state = self.current_state
        self.instance_status = "ended"

    def __str__(self):
        txt = f"FSA {self.instance_id}"
        txt += f", status: {self.instance_status}"
        txt += f", state count: {len(self.states)}"
        txt += f", input action count: {len(self.input_actions)}"
        txt += f", init state: {self.initial_state}"
        txt += f", current state: {self.current_state}"
        return txt

    def describe(self):
        txt = f"FSA {self.instance_id}"
        txt += f", status: {self.instance_status}"
        txt += f", current state: {self.current_state}"
        txt += f"\n    - states({len(self.states)}): {self.states}"
        txt += f"\n    - init state: {self.initial_state}"
        txt += f"\n    - final states({len(self.final_states)}): {self.final_states}"
        txt += f"\n    - input actions({len(self.input_actions)}): {self.input_actions}"
        txt += f"\n    - state links({len(self.state_links)}): {self.state_links}"
        return txt


s1 = 1
s2 = 2
s3 = 3

a1 = "a"
a2 = "b"
a3 = "c"

fsa = FSA(instance_id=1, initial_state=s1, states={ s2 }, final_states={ s3 }, input_actions={ a1, a2, a3 })
print(fsa.describe())
fsa.link_states(s1, a1, s2)
fsa.link_states(s2, a2, s3)
fsa.link_states(s3, a3, s1)
fsa.do_action(a1)
fsa.do_action(a2)
fsa.do_action(a3)
print(fsa.describe())

