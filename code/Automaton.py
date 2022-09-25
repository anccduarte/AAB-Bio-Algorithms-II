
class Automaton:

	def __init__(self, pat):
		self.pat = pat
		self.automaton = self.__build_automaton()

	def __build_automaton(self):
		automaton = {i: {} for i in range(len(self.pat) + 1)}
		for i in automaton:
			prefix = self.pat[:i+1]
			for c in set(self.pat):
				for j in range(i + 1):
					if prefix.find(self.pat[j:i] + c) == 0:
						automaton[i][c] = i + 1 - j
						break
		return automaton

	def find_pattern(self, text):
		state = 0
		positions = []
		for i, c in enumerate(text):
			state = self.automaton[state].get(c, 0)
			if state == len(self.pat):
				positions += [i - len(self.pat) + 1]
		return positions

p1 = Automaton("pattern")
text = "where is the pattern in this text? the pattern is 'pattern'..."
print(p1.find_pattern(text))

