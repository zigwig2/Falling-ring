def thermal_exchange(
    liquid_temp,
    ring_temp,
    current_depth,
    transfer_coefficient=1.0,
    capacity_coefficient_liquid=1.0,
    capacity_coefficient_ring=1.0,
):
    '''
    Computes the thermal exchange between the ring and liquid at current_depth.
    We model the interaction as point-wise between liquid_temp and ring_temp
    over (current_depth, idx) for all valid idx and update the arrays in-place.

    The temperature update is described as:
        T_r = T_r + k * (T_l - T_r) / C_r
    where the variables are:
        T_r: The temperature of the ring at a given depth
        T_l: The temperature of the liquid at a given depth
        k: The transfer coefficient
        C_r: The heat capacity coefficient of the ring

    The liquid temperature is similarly updated in-place, swapping r and l in 
        the equation using the original value of T_r before it is updated.

    Inputs:
        liquid_temp: A list of lists of floats representing the temperature of
            the liquid. Interpreted as liquid_temp[depth][p].
        ring_temp: A similar list of lists of floats representing the ring
            temperature when it is at a given depth. Has the same dimensions
            as liquid_temp.
        current_depth: An integer representing the depth.
        transfer_coefficient: A float representing the transfer coefficient, k.
        capacity_coefficient_liquid: A float representing the heat capacity
            coefficient for the liquid, C_l.
        capacity_coefficient_ring: A float representing the heat capacity
            coefficient for the ring, C_r.
    Returns:
        None (liquid_temp[current_depth] and ring_temp[current_depth] are modified)
    '''
    temp1=ring_temp[current_depth]  
    temp2=liquid_temp[current_depth]   # mis des val temp pour garder en memoir les val de ringtemp et liquidtemp qui vont etre modif
    ring_temp[current_depth]=[v+(transfer_coefficient*(temp2[i]-v)/capacity_coefficient_ring) for i,v in enumerate(ring_temp[current_depth])]
    liquid_temp[current_depth]=[v+(transfer_coefficient*(temp1[i]-v)/capacity_coefficient_liquid) for i,v in enumerate(liquid_temp[current_depth])]   # formule plus haut en list comprehention

def thermal_conduction(
    ring_temp,
    current_depth,
    transfer_coefficient=1.0,
    capacity_coefficient_ring=1.0,
):
    '''
    Computes thermal conduction within the ring at a given depth. The thermal
    conduction update is modelled as:
        T_r[p] = T_r[p] + k * (T_r[p+1] + T_r[p-1] - 2*T_r[p])/C_r
    where the variables represent:
        T_r[p]: The ring temperature at the current depth and point p on the ring
        k: The transfer coefficient
        C_r: The heat capacity coefficient of the ring

    The entire ring is updated using the original (unmodified) input values.

    Inputs:
        ring_temp: A list of lists of floats representing the ring
            temperature when it is at a given depth. Interpreted as ring_temp[depth][p]. 
        current_depth: An integer representing the depth.
        transfer_coefficient: A float representing the transfer coefficient, k.
        capacity_coefficient_ring: A float representing the heat capacity
            coefficient for the ring, C_r.
    Returns:
        None (ring_temp[current_depth] is modified)
    '''
    pass  # TODO make me
