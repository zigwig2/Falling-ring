#! /usr/bin/env python3

def get_interval(
    query,
    values,
):
    '''
    In the sorted list 'values', find the interval that contains 'query':
    so that values[i] <= query < values[i+1].
    Consider corner cases explained in the document.

    Inputs:
        query: the temperature to find an interval for
        values: a sorted list of temperatures

    Outputs:
        i: int: the index corresponding to the smaller temperature of the interval's boundaries.
    '''
    if query<values[0]:
        return 0
    elif query>=values[len(values)-1]:
        return len(values)-1
    
    for i in range(0,len(values)):
        if query>=values[i] and query<values[i+1]:
            return i


def interpolate_color(
    query,
    values,
    colors,
):
    '''
    Assigns a color to a given 'query' temperature, by mixing up two colors.
    First, 'i' will be chosen so that values[i] <= query < values[i+1].
    Then, linearly mix the colors at colors[i] and colors[i+1]:
    For instance, for a 'query' that is 60% of the way from values[i] to values[i+1],
    return the color that is made of 60% of colors[i+1] and 40% of colors[i].
    Consider corner cases explained in the document. 

    Inputs:
        query: the temperature to get a color for
        values: A sorted list of temperatures defining points in the colormap
        colors: A list of colors corresponding to each temperature in 'values'

    Outputs:
        color: [float,float,float]: the color that corresponds to 'query'
    '''
    L=[]
    i = get_interval(query, values)
    if query < values[0]:
        return colors[0]
    if query >= values[-1]:
        return colors[-1]
    else:
        P = (query-values[i])/(values[i+1]-values[i])
        for j in range(0,3):
            P_color=(1-P) * colors[i][j] + P * colors[i+1][j]
            L.append(P_color)
        return L


def map_to_color(
    in_data,
    out_data,
    values,
    colors,
):
    '''
    Maps the 2D in_data list to colors using the interpolate_color function. 

    Inputs:
        in_data: 2D array of temperatures (height by width)
        out_data: 3D array of colors (height by width by color channel)
        values: A sorted list of temperatures defining points in the colormap
        colors: A list of colors corresponding to each temperature in 'values'

    Outputs:
        None (out_data is modified)
    '''
    l=[]
    for i in range(0,len(in_data)):
        for j in range (0,len(in_data[i])):
            for f in range(0,3):
                l.append(interpolate_color(in_data[i][j],values,colors)[f])
                out_data[i][j]=l
            l=[]
    return out_data

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
    temp=tuple(ring_temp[current_depth])
    for i in range(len(temp)-1):
        ring_temp[current_depth][i]+=(transfer_coefficient*(temp[i+1]+temp[i-1]-2*temp[i]))/capacity_coefficient_ring
    ring_temp[current_depth][-1]+=(transfer_coefficient*(temp[0]+temp[-2]- 2*temp[-1]))/capacity_coefficient_ring
