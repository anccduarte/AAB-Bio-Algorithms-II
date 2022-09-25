
# RECURSIVE HAMILTONIAN PATHS

def new_arr(el, arr):
	# contains all arr's elements except for the first occurrence of el
	new_arr = []
	ct = 0
	for c in arr:
		if ct > 0 or c != el: new_arr += [c]
		if c == el: ct += 1
	return new_arr

def rebuild_frag_seqs(frag, frag_arr):
	# base case
	if frag_arr == []: return [[]]
	# recursive calls
	prob = []
	for f in frag_arr:
		if frag[1:] == f[:-1]:
			new_frags = new_arr(f, frag_arr)
			sub_prob = rebuild_frag_seqs(f, new_frags)
			if sub_prob != []:
				prob += [[f] + path for path in sub_prob]
	return prob

def rebuild_all_seqs(frags):
	# rebuild seqs starting from any fragment
	all_poss = []
	for frag in frags:
		new_frags = new_arr(frag, frags)
		all_poss += [[frag] + path for path in rebuild_frag_seqs(frag, new_frags)]
	# join seqs and add them to all_seqs if not already in it
	all_seqs = []
	for poss in all_poss:
		seq = poss[0] + "".join([c[-1] for c in poss])
		if seq not in all_seqs:
			all_seqs += [seq]
	# return all possible sequences
	return all_seqs

seq = "ATCGGTAGTCAGTAGTCAGATG"
frags = [seq[i:i+3] for i in range(len(seq) - 2)]

print(rebuild_all_seqs(frags))

