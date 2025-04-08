def apply_rule(cell, neighbors, generation, shock_interval):
    # Determine if Tariff Shock flips zones this tick
    shock = (generation > 0 and generation % shock_interval == 0)
    zone = cell.zone
    if shock:
        if zone == 'import_base':
            zone = 'import_recip'
        elif zone == 'import_recip':
            zone = 'import_base'

    # Standard Conway rules
    survive = neighbors in (2, 3)
    birth   = neighbors == 3

    if zone in ('export', 'market'):
        return (cell.state and survive) or (not cell.state and birth)

    if zone == 'import_base':
        # Underpopulation relief: survive with >=1 neighbor
        if cell.state:
            return 1 <= neighbors <= 3
        return birth

    if zone == 'import_recip':
        # Harsh overpopulation: die if neighbors >=3
        if cell.state:
            return neighbors < 3
        # Reproduction requires 4 neighbors
        return neighbors == 4

    return False