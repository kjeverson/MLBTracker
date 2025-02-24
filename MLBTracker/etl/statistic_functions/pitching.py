
def calculate_whip(hits, walks, ip):
    if ip > 0:
        return (hits + walks) / ip
    return 0


def calculate_win_percentage(wins, losses):
    total = wins + losses
    if total > 0:
        return wins / total
    return 0


def calculate_k9(strikeouts, ip):
    if ip > 0:
        return (strikeouts / ip) * 9
    return 0


def calculate_bb9(walks, ip):
    if ip > 0:
        return (walks / ip) * 9
    return 0


def get_innings_pitched(innings, innings_outs):
    return float(f'{innings}.{innings_outs}')