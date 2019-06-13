import math
from pysat.examples.rc2 import RC2, RC2Stratified
from pysat.formula import WCNF, WCNFPlus, IDPool
from pysat.card import EncType, CardEnc
import csv

MAX_P = 27
P_PER_G = 3

MAX_G = math.ceil(MAX_P / P_PER_G)

# Participant ranking matrix and settings
NEGATIVE_WEIGHT = -1000
ranking = [[NEGATIVE_WEIGHT for x in range(MAX_P)]
           for y in range(MAX_P)]

vpool = IDPool()

def import_rankings():
    '''
    Updates **global** ranking (list of lists.)
    ranking[i][j] is the score participant i gives to participant j
    '''
    file_location = "rankings.csv"
    with open(file_location) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                ranking[r][c] = int(cell)

def get_utility(p1, p2):
    '''
    Return the utility derived by p1 when paired with p2
    '''
    return ranking[p1][p2]

def belongs_var(p, g):
    return vpool.id('%d,%d' % (p, g))

def decode_index(i):
    p, g = vpool.obj(i).split(',')
    return int(p), int(g)

def z_var(p1, p2, g):
    return vpool.id('z(%d,%d,%d)' % (p1, p2, g))

def is_paired_var(p1, p2):
    return vpool.id('score(%d,%d)' % (p1, p2))

def retrieve_groupings(vars):
    if not vars:
        return
    groups = {i: [] for i in range(MAX_G)}
    for i, var in enumerate(vars):
        if i >= MAX_P * MAX_G:
            return groups
        if var < 0:
            continue
        p, g = decode_index(var)
        groups[g].append(p)
    return groups

### Exection begins here

# Ranking matrix updated from csv file
import_rankings()

wcnf = WCNFPlus()

for p in range(MAX_P):
    for g in range(MAX_G):
        # reserve top variables for membership
        belongs_var(p, g)

# Add scores
for p_i in range(MAX_P):
    for p_j in range(p_i + 1, MAX_P):
        utility_i = get_utility(p_i, p_j)
        utility_j = get_utility(p_j, p_i)

        z_list = []
        for g in range(MAX_G):
            z = z_var(p_i, p_j, g)
            belongs_i = belongs_var(p_i, g)
            belongs_j = belongs_var(p_j, g)
            # p1 && p2 <=> pair_index
            wcnf.extend([[z, -belongs_i, -belongs_j], [-z, belongs_i], [-z, belongs_j]])
            z_list.append(z)

        if utility_i == NEGATIVE_WEIGHT or utility_j == NEGATIVE_WEIGHT:
            for z in z_list:
                wcnf.append([-z])
        else:
            paired = is_paired_var(p_i, p_j)
            # any of pair indices <=> paired_var
            for z in z_list:
                wcnf.append([-z, paired])
            wcnf.append(z_list + [-paired])
            wcnf.append([-paired], weight= -(utility_i + utility_j) + 55)

# Restrict group sizes
for g in range(MAX_G):
    lits = []
    for p in range(MAX_P):
        lits.append(belongs_var(p, g))
    cnf = CardEnc.atmost(lits=lits, bound=P_PER_G, top_id=wcnf.nv, encoding=EncType.mtotalizer)
    wcnf.extend(cnf.clauses)

# Restrict one g per p
for p in range(MAX_P):
    lits = []
    for g in range(MAX_G):
        lits.append(belongs_var(p, g))
    cnf = CardEnc.atleast(lits=lits, bound=1, top_id=wcnf.nv, encoding=EncType.ladder)
    wcnf.extend(cnf.clauses)

# wcnf.to_file('grouping.wcnf')
print(sum(wcnf.wght))
print(max(wcnf.wght))
print(min(wcnf.wght))

def count_score(groups):
    score = 0
    for grp_id, group in groups.items():
        for i, p1 in enumerate(group):
            for j, p2 in enumerate(group):
                if j <= i:
                    continue
                score += get_utility(p1, p2) + get_utility(p2, p1)
    return score

vals = '-1 2 -3 -4 -5 -6 -7 -8 -9 -10 -11 -12 13 -14 -15 -16 -17 -18 -19 -20 -21 -22 -23 -24 -25 26 -27 28 -29 -30 -31 -32 -33 -34 -35 -36 -37 -38 -39 -40 -41 42 -43 -44 -45 -46 -47 -48 -49 50 -51 -52 -53 -54 55 -56 -57 -58 -59 -60 -61 -62 -63 -64 -65 66 -67 -68 -69 -70 -71 -72 -73 74 -75 -76 -77 -78 -79 -80 -81 -82 -83 -84 -85 -86 -87 88 -89 -90 -91 -92 -93 94 -95 -96 -97 -98 -99 -100 -101 102 -103 -104 -105 -106 -107 -108 -109 -110 -111 -112 -113 -114 115 -116 -117 -118 -119 -120 -121 -122 -123 -124 -125 126 -127 -128 -129 -130 131 -132 -133 -134 -135 -136 -137 -138 -139 -140 -141 -142 -143 144 -145 -146 -147 -148 -149 -150 151 -152 -153 154 -155 -156 -157 -158 -159 -160 -161 -162 -163 -164 -165 -166 -167 168 -169 -170 -171 -172 173 -174 -175 -176 -177 -178 -179 -180 -181 -182 183 -184 -185 -186 -187 -188 -189 -190 -191 -192 -193 194 -195 -196 -197 -198 -199 -200 -201 -202 -203 204 -205 -206 -207 -208 -209 -210 -211 -212 -213 -214 215 -216 -217 -218 -219 -220 -221 -222 -223 224 -225 -226 -227 -228 229 -230 -231 -232 -233 -234 -235 -236 -237 -238 -239 -240 -241 -242 243 -244 -245 -246 -247 -248 -249 -250 -251 -252 -253 -254 -255 -256 -257 -258 -259 -260 -261 -262 -263 -264 -265 -266 -267 -268 -269 -270 -271 -272 -273 -274 -275 -276 -277 -278 -279 -280 -281 -282 -283 -284 -285 -286 -287 -288 -289 -290 -291 -292 -293 -294 -295 -296 -297 -298 -299 -300 -301 -302 -303 -304 -305 -306 -307 -308 -309 -310 -311 -312 -313 -314 315 -316 -317 -318 -319 -320 -321 -322 323 -324 -325 -326 -327 -328 -329 -330 -331 -332 -333 -334 -335 -336 -337 -338 -339 -340 -341 -342 -343 -344 -345 -346 -347 -348 -349 -350 -351 -352 -353 -354 -355 -356 -357 -358 -359 -360 -361 -362 -363 -364 -365 -366 -367 -368 -369 -370 -371 -372 -373 -374 -375 -376 -377 -378 -379 -380 -381 -382 -383 -384 -385 -386 -387 -388 -389 -390 -391 -392 -393 -394 -395 -396 -397 -398 -399 -400 -401 -402 -403 -404 -405 -406 -407 -408 -409 -410 -411 -412 -413 -414 -415 -416 -417 -418 -419 -420 -421 -422 -423 -424 425 -426 -427 -428 -429 -430 -431 -432 433 -434 -435 -436 -437 -438 -439 -440 -441 -442 -443 -444 -445 -446 -447 -448 -449 -450 -451 -452 -453 -454 -455 -456 -457 -458 -459 -460 -461 -462 -463 -464 -465 -466 -467 -468 -469 -470 -471 -472 -473 -474 -475 -476 -477 -478 -479 -480'.split(' ')
groups = retrieve_groupings(map(int, vals))
print(groups)
print(count_score(groups))

# with RC2Stratified(wcnf) as rc2:
#     for i in range(1):
#         m = rc2.compute()
#         print(m)
#         print('Total utility: %d' % (rc2.cost))
#         print('The groupings are:')
#         print(retrieve_groupings(m))
