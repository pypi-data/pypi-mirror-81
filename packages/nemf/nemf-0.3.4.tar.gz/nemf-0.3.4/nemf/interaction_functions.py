# interaction functions

## Default interactions (unrestricted)
def inverse_type_0(X,idx_A,idx_B,coefficient):
    """ linear response with respect to *origin/prey* compartment

    Parameters
    ----------
    X : np.array
        containing the current state of the contained quantity of each 
        compartment
    idx_A : integer
        index of the element representing the destination/predator compartment
    idx_B : integer
        index of the element representing the origin/pray compartment
    coefficient : float
        governs the slope of the linear response

    Returns
    -------
    df : float
        change in the origin and destitnation compartment. Calculated by
        coefficient*origin_compartment
    
    """
    
    A = X[idx_A] # quantity of compartment A (predator/consumer)
    B = X[idx_B] # quantity of compartment B (prey/nutrient)

    df = coefficient*B
    
    return df

def holling_type_0(X,idx_A,coefficient):
    """ linear response with respect to *destination/predator* compartment
    
    For examples see:
    `Examples <https://gist.github.com/465b/cce390f58d64d70613a593c8038d4dc6>`_

    Parameters
    ----------
    X : np.array
        containing the current state of the contained quantity of each 
        compartment
    idx_A : integer
        index of the element representing the destination/predator compartment
    idx_B : integer
        index of the element representing the origin/pray compartment
    coefficient : float
        governs the slope of the linear response

    Returns
    -------
    df : float
        change in the origin and destitnation compartment. Calculated by
        coefficient*destination_compartment
    
    """
    
    A = X[idx_A] # quantity of the linearly dependant compartment
    df = coefficient*A

    return df


def holling_type_I(X,idx_A,idx_B,coefficient):
    """ linear response with respect to both *origin/pray* and 
        *destination/predator* compartment.
    
    For examples see:
    `Examples <https://gist.github.com/465b/cce390f58d64d70613a593c8038d4dc6>`_

    Parameters
    ----------
    X : np.array
        containing the current state of the contained quantity of each 
        compartment
    idx_A : integer
        index of the element representing the destination/predator compartment
    idx_B : integer
        index of the element representing the origin/pray compartment
    coefficient : float
        governs the slope of the linear response

    Returns
    -------
    df : float
        change in the origin and destitnation compartment. Calculated by
        coefficient * origin_compartment * destination_compartment
    
    """
    
    
    A = X[idx_A] # quantity of compartment A (predator/consumer)
    B = X[idx_B] # quantity of compartment B (prey/nutrient)
    df = (coefficient*B)*A
    
    return df


def holling_type_II(X,idx_A,idx_B,food_processing_time,hunting_rate):
    """ non-linear response with respect to *origin/pray* with linear response
        with respect to *destination/predator* compartment
    
    The response with respect to the origin compartment 'B' is approximately 
    linear for small 'B' and converges towards an upper limit governed by the
    'food_processing_time' for large 'B'.
    For examples see:
    `Examples <https://gist.github.com/465b/cce390f58d64d70613a593c8038d4dc6>`_


    Parameters
    ----------
    X : np.array
        containing the current state of the contained quantity of each 
        compartment
    idx_A : integer
        index of the element representing the destination/predator compartment
    idx_B : integer
        index of the element representing the origin/pray compartment
    coefficient : float
        governs the slope of the linear response

    Returns
    -------
    df : float
        change in the origin and destitnation compartment. Calculated by
        consumption_rate = ((hunting_rate * origin_compartment) / 
        (1 + hunting_rate * food_processing_time * origin_compartment)) *
        destination_compartment
    
    """
    A = X[idx_A] # quantity of compartment A (predator/consumer)
    B = X[idx_B] # quantity of compartment B (prey/nutrient)
    
    df = ((hunting_rate * B)/
            (1+hunting_rate * food_processing_time * B))*A
    
    return df


def holling_type_III(X,idx_A,idx_B,saturation_rate,consumption_rate_limit):
    """ non-linear response with respect to *origin/pray* with linear response
        with respect to *destination/predator* compartment
    
    The response with respect to the origin compartment 'B' is approximately 
    quadratic for small 'B' and converges towards an upper limit governed by the
    'food_processing_time' for large 'B'.
    For examples see:
    `Examples <https://gist.github.com/465b/cce390f58d64d70613a593c8038d4dc6>`_


    Parameters
    ----------
    X : np.array
        containing the current state of the contained quantity of each 
        compartment
    idx_A : integer
        index of the element representing the destination/predator compartment
    idx_B : integer
        index of the element representing the origin/pray compartment
    saturation_rate : float
        first parameter of the interaction.
        governs the slope of the non lineare response for small pray 
        populations.
    consumption_rate_limit : float
        second parameter of the interaction.
        governs the upper limit of the response.

    Returns
    -------
    df : float
        change in the origin and destitnation compartment. Calculated by
        consumption_rate = ((consumption_rate_limit * saturation_rate * B**2)/
         (consumption_rate_limit + (saturation_rate*B**2)))*A
    
    """
    A = X[idx_A] # quantity of compartment A (predator/consumer)
    B = X[idx_B] # quantity of compartment B (prey/nutrient)
    
    df = ((consumption_rate_limit*saturation_rate*B**2)/
                (consumption_rate_limit+(saturation_rate*B**2)))*A


    return df


def sloppy_feeding(holling_type,coeff,*args):
    """ calls holling_type functions with an extra "efficiency" coefficient.
        the inverse of the efficiency is then supposed to flow into
        a different compartment """
        
    if holling_type == '0':
        X, idx_A, coefficient = args
        return coeff*holling_type_0(X, idx_A, coefficient)
    elif holling_type == 'I':
        X, idx_A, idx_B, coefficient = args
        return coeff*holling_type_I(X, idx_A, idx_B, coefficient)
    elif holling_type == 'II':
        X, idx_A, idx_B, food_processing_time, hunting_rate  = args
        return coeff*holling_type_II(X, idx_A, idx_B, 
                                     food_processing_time, hunting_rate)
    elif holling_type == 'III':
        X, idx_A, idx_B, saturation_rate, consumption_rate_limit = args
        return coeff*holling_type_III(X, idx_A, idx_B, 
                                      saturation_rate, consumption_rate_limit)
    else:
        raise ValueError("The defined holling_type is not available. "
            +"Use one of the following: ['0','I','II','III']")
    

def nutrient_limited_growth(X,idx_A,idx_B,growth_rate,half_saturation):
    """ non-linear response with respect to *destination/predator* compartment

    Similar to holling_type_II and is a reparameterization of holling II.
    The response with respect to the origin compartment 'B' is approximately 
    linear for small 'B' and converges towards an upper limit governed by the
    'growth_rate' for large 'B'.
    For examples see:
    `Examples <https://gist.github.com/465b/cce390f58d64d70613a593c8038d4dc6>`_


    Parameters
    ----------
    X : np.array
        containing the current state of the contained quantity of each 
        compartment
    idx_A : integer
        index of the element representing the destination/predator compartment
    idx_B : integer
        index of the element representing the origin/pray compartment
    growth_rate : float
        first parameter of the interaction.
        governs the upper limit of the response.
    half_saturation : float
        second parameter of the interaction.
        governs the slope of the response.

    Returns
    -------
    df : float
        change in the origin and destitnation compartment. Calculated by
        consumption_rate = ((hunting_rate * origin_compartment) / (1 + 
        hunting_rate * food_processing_time * origin_compartment)) * 
        destination_compartment
    
    """
    A = X[idx_A] # quantity of compartment A (predator/consumer)
    B = X[idx_B] # quantity of compartment B (prey/nutrient)

    df = growth_rate*(B/(half_saturation+B))*A

    return df


### referencing interaction functions
""" It is helpfull from a mechanistic point of view to not only
    represent the relation between parameters but also its 'context'.
    Hence, a linear mortality might be represented with a lin_mort()
    function which then maps to a standard linear function to better
    represent its usage and increase readability """

linear_mortality = inverse_type_0
remineralisation = holling_type_I
exudation = inverse_type_0
excretion = inverse_type_0
stress_dependant_exudation = holling_type_I


## Non-Negative versions of the previous (default) interactions

def non_negative_inverse_type_0(X,idx_A,idx_B,coefficient):
    
    B = X[idx_B] # quantity of compartment B (prey/nutrient)

    if B < 0:
        df = 0
        return df
    
    df = coefficient*B
    return df

def non_negative_holling_type_0(X,idx_A,coefficient):
    
    A = X[idx_A] # quantity of the linearly dependant compartment
    
    if A < 0:
        df = 1e-9    
    df = coefficient*A
    
    return df


def non_negative_holling_type_I(X,idx_A,idx_B,coefficient):
    
    A = X[idx_A] # quantity of compartment A (predator/consumer)
    B = X[idx_B] # quantity of compartment B (prey/nutrient)
    
    if (B < 0):
        df = 0
        return df
    elif (A < 0):
        A = 1e-9    

    df = (coefficient*B)*A
    
    return df


def non_negative_holling_type_II(X,idx_A,idx_B,
                                 food_processing_time,hunting_rate):

    A = X[idx_A] # quantity of compartment A (predator/consumer)
    B = X[idx_B] # quantity of compartment B (prey/nutrient)
    
    if (B < 0):
        df = 0
        return df
    elif (A < 0):
        A = 1e-9    

    df = ((hunting_rate * B)/
            (1+hunting_rate * food_processing_time * B))*A
    
    return df
    

def non_negative_nutrient_limited_growth(X,idx_A,idx_B,
                                         growth_rate,half_saturation):
    A = X[idx_A] # quantity of compartment A (predator/consumer)
    B = X[idx_B] # quantity of compartment B (prey/nutrient)

    if (B < 0):
        df = 0
        return df
    elif (A < 0):
        A = 1e-9    
    
    df = growth_rate*(B/(half_saturation+B))*A
    
    return df


def non_negative_dual_nutrient_limited_growth(X,idx_A,idx_B,growth_rate,
                                              half_saturation,second_nutrient,
                                              second_half_saturation):

    A = X[idx_A] # quantity of compartment A (predator/consumer)
    B = X[idx_B] # quantity of compartment B (prey/nutrient)
    
    if (B < 0):
        df = 0
        return df
    elif (X[second_nutrient] < 0):
        df = 0
        return df
    elif (A < 0):
        A = 1e-9    
    
    df = (growth_rate*(B/(half_saturation+B))
          *(X[second_nutrient]/(second_half_saturation+X[second_nutrient]))*A)
      
    return df



non_negative_linear_mortality = non_negative_inverse_type_0
non_negative_remineralisation = non_negative_holling_type_I
non_negative_exudation = non_negative_inverse_type_0
non_negative_excretion = non_negative_inverse_type_0
non_negative_stress_dependant_exudation = non_negative_holling_type_I
