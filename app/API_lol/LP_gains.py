def LP_Gains(old_data, new_data):
    old_tier, old_rank, old_lp = old_data[1:]
    new_tier, new_rank, new_lp = new_data[1:]

    lp_change = new_lp - old_lp

    if (old_rank > new_rank) and (old_tier == new_tier):
        rank_diff = old_rank - new_rank
        lp_change += 100 * rank_diff

    if (old_rank < new_rank) and (old_tier == new_tier):
        rank_diff = new_rank - old_rank
        lp_change -= 100 * rank_diff

    if old_tier != new_tier:
        lp_change = 0
        return lp_change

    return lp_change