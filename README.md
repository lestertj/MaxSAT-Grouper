# MaxSAT-Grouper
Finds the optimal grouping of participants. Given each participant has a known utility of being grouped with every other participant, this script finds the grouping that maximizes the utility across all participants. 

## Usage
Change the implementation of `get_pair_score(p1, p2)` to return the total utility of the pairing (p1, p2).
Then,
```
python group_solver.py
```
