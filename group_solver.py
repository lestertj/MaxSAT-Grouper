import math
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.card import EncType, CardEnc

MAX_P = 30
P_PER_G = 3

MAX_G = math.ceil(MAX_P / P_PER_G)

def get_pair_score(p1, p2):
	'''
	Return the total utility of the pairing (p1, p2)
	'''
	return 1

def get_index(p, g):
	return g * MAX_P + p + 1

def decode_index(i):
	g = (i-1) // MAX_P
	p = (i-1) % MAX_P
	return p, g

def get_pairing_index(p1, p2):
	result = MAX_P * MAX_G
	for i in range(p1):
		result += MAX_P - i - 1
	return result + p2

def retrieve_groupings(vars):
	groups = {i: [] for i in range(MAX_G)}
	for i, var in enumerate(vars):
		if i >= MAX_P * MAX_G:
			return groups
		if var < 0:
			continue
		p, g = decode_index(var)
		groups[g].append(p)
	return groups

wcnf = WCNF()

# Add scores
for p1 in range(MAX_P):
	for p2 in range(p1 + 1, MAX_P):
		pair_index = get_pairing_index(p1, p2)
		for g in range(MAX_G):
			# p1 && p2 -> pair_index
			wcnf.extend([[-pair_index, get_index(p1, g)], [-pair_index, get_index(p2, g)]])
		wcnf.append([pair_index], weight=-get_pair_score(p1, p2))

# Restrict group sizes
for g in range(MAX_G):
	lits = []
	for p in range(MAX_P):
		lits.append(get_index(p, g))
	cnf = CardEnc.equals(lits=lits, bound=P_PER_G, top_id=max(MAX_P * MAX_G, wcnf.nv), encoding=EncType.seqcounter)
	wcnf.extend(cnf.clauses)

# Restrict one g per p
for p in range(MAX_P):
	lits = []
	for g in range(MAX_G):
		lits.append(get_index(p, g))
	cnf = CardEnc.equals(lits=lits, bound=1, top_id=max(MAX_P * MAX_G, wcnf.nv), encoding=EncType.seqcounter)
	wcnf.extend(cnf.clauses)

with RC2(wcnf) as rc2:
	for i in range(1):
		m = rc2.compute()
		print('Total utility: %d' % (-rc2.cost))
		print('The groupings are:')
		print(retrieve_groupings(m))
