import random

COST_OF_CHILD = 0.50
MIN_TRUST = -0.99
MAX_TRUST = 0.99
INHERITANCE_NOISE = 0.50
INITIAL_TRUST_MIN = -0.99
INITIAL_TRUST_MAX = 0.99

class Individual:
    def __init__(self, mother = 0, father = 0):
        if mother == 0:
            self._init_no_parents()
        else:
            self._init_with_parents(mother, father)
        self.num_children = 0
        self.num_surviving_children = 0

    def _init_no_parents(self):
        self.sex = random.choice(['M', 'F'])
        self.quality = random.uniform(0.01, 0.99)
        self.signaling_effort = random.uniform(0.01, 0.1)
        self.trust = random.uniform(INITIAL_TRUST_MIN, INITIAL_TRUST_MAX)
        self.signal, self.value = self._calculate_signal_and_value()
        self.arbitrary = random.uniform(-0.99, 0.99)

    def _init_with_parents(self, mother, father):
        self.sex = random.choice(['M', 'F'])
        self.quality = random.uniform(0.01, 0.99)
        # self.quality = self._inherit_trait(mother.quality, father.quality)
        self.signaling_effort = self._inherit_trait(mother.signaling_effort, father.signaling_effort)
        self.trust = self._inherit_trust(mother.trust, father.trust)
        self.signal, self.value = self._calculate_signal_and_value()
        self.arbitrary = self._inherit_trust(mother.arbitrary, father.arbitrary)

    def _inherit_trait(self, mother_trait, father_trait):
        trait = (mother_trait + father_trait + random.uniform(-INHERITANCE_NOISE, INHERITANCE_NOISE)) / 2
        trait = max(0, trait) # don't go below 0.01
        trait = min(1, trait) # don't go above 0.99
        return trait

    def _inherit_trust(self, mother_trait, father_trait):
        trait = (mother_trait + father_trait + random.uniform(-INHERITANCE_NOISE, INHERITANCE_NOISE)) / 2
        # trait = max(MIN_TRUST, trait) # don't go below MIN_TRUST
        # trait = min(MAX_TRUST, trait) # don't go above MAX_TRUST
        return trait

    def _calculate_signal_and_value(self):
        # Straight lines
        signal = self.signaling_effort * self.quality
        value = self.quality * (1 - self.signaling_effort)

        # Curved lines
        # value = self.quality * (1 - self.signaling_effort)
        # signal = -((value/self.quality) ** 2) + 1
        return signal, value