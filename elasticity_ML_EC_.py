"""
Calculation of direct elasticities for the PML model
Ville Isoranta 19.11.2025 
"""
"""
Imports necessary expressions.
"""
import biogeme.biogeme as bio 
from biogeme import models 
from biogeme.expressions import MonteCarlo
import numpy as np
from biogeme.expressions import Derive
import biogeme.results as res
from IPython.core.display_functions import display

"""
Imports necessary variables and the database from the data preparation file.
"""
from data_preparation import(
    database,
    PG_NORM_TRIP,
    PS_NORM_TRIP,
    EG,
    ES,
    SG,
    SS
)

"""
Imports utility function specifications from the utility 
function specification file.
"""
from EC_init_final import (
    model_ini
) 

V_ML, av, _ = model_ini() # imports the utility functions, and availability condition


prob_G = MonteCarlo(models.logit(V_ML, av, 1))  # retuns probability, in non-logarithmic form
prob_S = MonteCarlo(models.logit(V_ML, av, 2))
prob_TRAN = MonteCarlo(models.logit(V_ML, av, 3))

"""
This code utilizes PWSE as discussed in Section 3.3.4. 
The direct elasticites are computed using the following
equations (see Section 3.3.4).
"""
elas_PG = Derive(prob_G, 'PG_NORM_TRIP') * PG_NORM_TRIP/ prob_G
elas_PS = Derive(prob_S, 'PS_NORM_TRIP') * PS_NORM_TRIP/ prob_S
elas_EG = Derive(prob_G, 'EG') * EG / prob_G
elas_ES = Derive(prob_S, 'ES') * ES / prob_S
elas_SG = Derive(prob_G, 'SG') * SG / prob_G
elas_SS = Derive(prob_S, 'SS') * SS / prob_S

"""
Next a dictionary structure is generated.
The structure contains all quantities to be simulated.
"""

simulate = {
    'prob_G' : prob_G,
    'prob_S' : prob_S,
    'prob_TRAN' : prob_TRAN,
    'elas_PG' : elas_PG,
    'elas_PS' : elas_PS,
    'elas_EG' : elas_EG,
    'elas_ES' : elas_ES,
    'elas_SG' : elas_SG,
    'elas_SS' : elas_SS
}

"""
Creates the biogeme object, conducts the simulation, and
loads the beta-coefficient values from the result file. 
"""

the_biogeme_elas = bio.BIOGEME(database, simulate)
results = res.bioResults(pickle_file='file path removed')
simulated_values = the_biogeme_elas.simulate(results.get_beta_values())

"""
Displays values for a sanity check
"""
display(simulated_values)

"""
Next the sum of probabilities for the denominators is computed.
"""

denominator_G = simulated_values['prob_G'].sum()
denominator_S = simulated_values['prob_S'].sum()
denominator_TRAN = simulated_values['prob_TRAN'].sum()

"""
See Section 3.3.4 for the elasticity
equations used in the following expressions.
Elasticity of the price of garage
"""

direct_elas_term_PG= (
    simulated_values['prob_G']
    * simulated_values['elas_PG']
    / denominator_G
).sum()

print(
    f'Aggregate direct point elasticity for the price of garage: '
    f'{direct_elas_term_PG:.3g}'
)

"""
Elasticity of the egress time of garage
"""

direct_elas_term_EG= (
    simulated_values['prob_G']
    * simulated_values['elas_EG']
    / denominator_G
).sum()

print(
    f'Aggregate direct point elasticity for the egress time of garage: '
    f'{direct_elas_term_EG:.3g}'
)
"""
Elasticity of the search time of garage
"""

direct_elas_term_SG= (
    simulated_values['prob_G']
    * simulated_values['elas_SG']
    / denominator_G
).sum()

print(
    f'Aggregate direct point elasticity for the search time of garage: '
    f'{direct_elas_term_SG:.3g}'
)

"""
Elasticity of the price of on-street parking
"""
direct_elas_term_PS= (
    simulated_values['prob_S']
    * simulated_values['elas_PS']
    / denominator_S
).sum()

print(
    f'Aggregate direct point elasticity for the price of on-street parking: '
    f'{direct_elas_term_PS:.3g}'
)
"""
Elasticity of the egress time of on-street parking
"""
direct_elas_term_ES= (
    simulated_values['prob_S']
    * simulated_values['elas_ES']
    / denominator_S
).sum()

print(
    f'Aggregate direct point elasticity for the egress time of on-street parking: '
    f'{direct_elas_term_ES:.3g}'
)
"""
Elasticity of the search time of on-street parking
"""
direct_elas_term_SS= (
    simulated_values['prob_S']
    * simulated_values['elas_SS']
    / denominator_S
).sum()

print(
    f'Aggregate direct point elasticity for the search time of on-street parking: '
    f'{direct_elas_term_SS:.3g}'
)




