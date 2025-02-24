

def calculate_singles(hits, doubles, triples, home_runs):
    if hits > 0:
        return hits - doubles - triples - home_runs
    return 0


def calculate_batting_average(hits, at_bats):
    if at_bats > 0:
        return hits/at_bats
    return 0


def calculate_slugging_percentage(singles, doubles, triples, home_runs, at_bats):
    if at_bats > 0:
        return (singles + 2*doubles + 3*triples + 4*home_runs) / at_bats
    return 0


def calculate_batting_balls_in_play(hits, home_runs, at_bats, strikeouts, sacrifice_flys):
    total = at_bats - strikeouts - home_runs + sacrifice_flys
    if total > 0:
        return (hits - home_runs) / total
    return 0
