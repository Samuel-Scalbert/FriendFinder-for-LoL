# Define a function called "LP_Gains" that takes two arguments, "old_data" and "new_data"
def LP_Gains(old_data, new_data):
    # Unpack "old_data" and "new_data" tuples to get their respective tier, rank, and lp
    old_tier, old_rank, old_lp = old_data[1:]
    new_tier, new_rank, new_lp = new_data[1:]

    # Calculate the difference between the new and old LP
    lp_change = new_lp - old_lp

    # Check if the old rank is higher than the new rank and the old and new tiers are the same
    if (old_rank > new_rank) and (old_tier == new_tier):
        # Calculate the rank difference between the old and new ranks
        rank_diff = old_rank - new_rank
        # Add the rank difference times 100 to the lp_change
        lp_change += 100 * rank_diff

    # Check if the new rank is higher than the old rank and the old and new tiers are the same
    if (old_rank < new_rank) and (old_tier == new_tier):
        # Calculate the rank difference between the old and new ranks
        rank_diff = new_rank - old_rank
        # Subtract the rank difference times 100 from the lp_change
        lp_change -= 100 * rank_diff

    # Check if the old tier is different from the new tier
    if old_tier != new_tier:
        # Set the lp_change to 0 and return it
        lp_change = 0
        return lp_change

    # Return the lp_change value
    return lp_change
