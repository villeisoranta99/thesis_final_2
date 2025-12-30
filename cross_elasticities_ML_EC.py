"""
Calculation of cross elasticities for the PML model
Ville Isoranta 19.11.2025
Results shown in Sections 4.2.3 and 4.2.4
"""
"""
Imports necessary expressions.
"""
import biogeme.biogeme as bio 
from biogeme import models 
from biogeme.expressions import Derive
import biogeme.results as res
import numpy as np
from IPython.core.display_functions import display
from biogeme.expressions import MonteCarlo 


"""
Imports necessary variables and the daabase from the data preparation file.
"""
from data_preparation import (
    database,
    PG_NORM_TRIP,
    PS_NORM_TRIP,
    EG,
    ES,
    SG,
    SS,
)

"""
Imports utility function specifications from the utility 
function specification file.
"""
from EC_init_final import (
    model_ini
    ) 

V_ML, av, CHOI = model_ini() # imports the utility functions, availability condition and choice

prob_G = MonteCarlo(models.logit(V_ML, av, 1)) # retuns probability, in non-logarithmic form
prob_S = MonteCarlo(models.logit(V_ML, av, 2))
prob_TRAN = MonteCarlo(models.logit(V_ML, av, 3))

"""
This code utilizes PWSE as discussed in Section 3.3.4.
Public transport cross elasticities with respect to parking attributes are
calculated next.
"""
cela_PG_TRAN = Derive(prob_TRAN, 'PG_NORM_TRIP') * (PG_NORM_TRIP / prob_TRAN)
cela_PS_TRAN = Derive(prob_TRAN, 'PS_NORM_TRIP') * (PS_NORM_TRIP / prob_TRAN)
cela_EG_TRAN = Derive(prob_TRAN, 'EG') * (EG / prob_TRAN)
cela_ES_TRAN = Derive(prob_TRAN, 'ES') * (ES / prob_TRAN)
cela_SG_TRAN = Derive(prob_TRAN, 'SG') * (SG / prob_TRAN)
cela_SS_TRAN = Derive(prob_TRAN, 'SS') * (SS / prob_TRAN)

"""
Parking cross elasticities with respect to parking attributes are
calculated using the following 
equations (See Section 3.3.4).
"""

cela_PG_S = Derive(prob_S, 'PG_NORM_TRIP') * (PG_NORM_TRIP/ prob_S)
cela_EG_S = Derive(prob_S, 'EG') * (EG / prob_S)
cela_SG_S = Derive(prob_S, 'SG') * (SG / prob_S)
cela_PS_G = Derive(prob_G, 'PS_NORM_TRIP') * (PS_NORM_TRIP / prob_G)
cela_ES_G = Derive(prob_G, 'ES') * (ES / prob_G)
cela_SS_G = Derive(prob_G, 'SS') * (SS / prob_G)

"""
Next a dictionary structure is generated.
The structure contains all quantities to be simulated.
"""

simulate = {
    'prob_G' : prob_G,
    'prob_S' : prob_S,
    'prob_TRAN' : prob_TRAN,
    'cela_PG_TRAN' : cela_PG_TRAN,
    'cela_PS_TRAN' : cela_PS_TRAN,
    'cela_EG_TRAN' : cela_EG_TRAN,
    'cela_ES_TRAN' : cela_ES_TRAN,
    'cela_SG_TRAN' : cela_SG_TRAN,
    'cela_SS_TRAN' : cela_SS_TRAN,
    'cela_PG_S' : cela_PG_S,
    'cela_EG_S' : cela_EG_S,
    'cela_SG_S' : cela_SG_S,
    'cela_PS_G' : cela_PS_G,
    'cela_ES_G' : cela_ES_G,
    'cela_SS_G' : cela_SS_G,
}

"""
Creates the biogeme object, conducts the simulation, and
loads the beta-coefficient values from the result file. 
"""

the_biogeme_celas = bio.BIOGEME(database, simulate)
the_biogeme_celas.modelName = "Cross_elasticities_final"
betas = the_biogeme_celas.free_beta_names
results = res.bioResults(pickle_file='file path removed')
betaValues = results.get_beta_values(betas)

"""
Displays values for a sanity check
"""

simulated_values_cross = the_biogeme_celas.simulate(betaValues)
display(simulated_values_cross)

"""
Next the sum of probabilities for the denominators is computed.
"""

denominator_G = simulated_values_cross['prob_G'].sum()
denominator_S = simulated_values_cross['prob_S'].sum()
denominator_TRAN = simulated_values_cross['prob_TRAN'].sum()


"""
See Section 3.3.4 for the elasticity
equations used in the following expressions.
Public transport - price of garage cross elastity
"""
cross_elas_term_PG_TRAN= (
    simulated_values_cross['prob_TRAN']
    * simulated_values_cross['cela_PG_TRAN']
    / denominator_TRAN
).sum()

print(
    f'Aggregate cross point elasticity of public transport wrt price of garage: '
    f'{cross_elas_term_PG_TRAN:.3g}'
)

"""
Public transport - egress time of garage cross elastity
"""
cross_elas_term_EG_TRAN= (
    simulated_values_cross['prob_TRAN']
    * simulated_values_cross['cela_EG_TRAN']
    / denominator_TRAN
).sum()

print(
    f'Aggregate cross point elasticity of public transport wrt egress time of garage: '
    f'{cross_elas_term_EG_TRAN:.3g}'
)

"""
Public transport - search time of garage cross elastity
"""

cross_elas_term_SG_TRAN= (
    simulated_values_cross['prob_TRAN']
    * simulated_values_cross['cela_SG_TRAN']
    / denominator_TRAN
).sum()

print(
    f'Aggregate cross point elasticity of public transport wrt search time of garage: '
    f'{cross_elas_term_SG_TRAN:.3g}'
)

"""
Public transport - price of on-street parking cross elastity
"""

cross_elas_term_PS_TRAN= (
    simulated_values_cross['prob_TRAN']
    * simulated_values_cross['cela_PS_TRAN']
    / denominator_TRAN
).sum()

print(
    f'Aggregate cross point elasticity of public transport wrt price of on-street parking: '
    f'{cross_elas_term_PS_TRAN:.3g}'
)

"""
Public transport - egress time of on-street parking cross elastity
"""

cross_elas_term_ES_TRAN= (
    simulated_values_cross['prob_TRAN']
    * simulated_values_cross['cela_ES_TRAN']
    / denominator_TRAN
).sum()

print(
    f'Aggregate cross point elasticity of public transport wrt egress time of on-street parking: '
    f'{cross_elas_term_ES_TRAN:.3g}'
)
"""
Public transport - search time of on-street parking cross elastity
"""

cross_elas_term_SS_TRAN= (
    simulated_values_cross['prob_TRAN']
    * simulated_values_cross['cela_SS_TRAN']
    / denominator_TRAN
).sum()

print(
    f'Aggregate cross point elasticity of public transport wrt search time of on-street parking: '
    f'{cross_elas_term_SS_TRAN:.3g}'
)

"""
On-street parking - price of garage cross elastity
"""

cross_elas_term_PG_S= (
    simulated_values_cross['prob_S']
    * simulated_values_cross['cela_PG_S']
    / denominator_S
).sum()

print(
    f'Aggregate cross point elasticity of on-street parking wrt price of garage: '
    f'{cross_elas_term_PG_S:.3g}'
)

"""
On-street parking - egress time of garage cross elastity
"""

cross_elas_term_EG_S= (
    simulated_values_cross['prob_S']
    * simulated_values_cross['cela_EG_S']
    / denominator_S
).sum()

print(
    f'Aggregate cross point elasticity of on-street parking wrt egress time of garage: '
    f'{cross_elas_term_EG_S:.3g}'
)

"""
On-street parking - search time of garage cross elastity
"""

cross_elas_term_SG_S= (
    simulated_values_cross['prob_S']
    * simulated_values_cross['cela_SG_S']
    / denominator_S
).sum()

print(
    f'Aggregate cross point elasticity of on-street parking wrt search time of garage: '
    f'{cross_elas_term_SG_S:.3g}'
)

"""
Garage - price of on-street parking cross elastity
"""

cross_elas_term_PS_G= (
    simulated_values_cross['prob_G']
    * simulated_values_cross['cela_PS_G']
    / denominator_G
).sum()

print(
    f'Aggregate cross point elasticity of garage wrt price of on-street parking: '
    f'{cross_elas_term_PS_G:.3g}'
)

"""
Garage - egress time of on-street parking cross elastity
"""

cross_elas_term_ES_G= (
    simulated_values_cross['prob_G']
    * simulated_values_cross['cela_ES_G']
    / denominator_G
).sum()

print(
    f'Aggregate cross point elasticity of garage wrt egress time of on-street parking: '
    f'{cross_elas_term_ES_G:.3g}'
)

"""
Garage - search time of on-street parking cross elastity
"""

cross_elas_term_SS_G= (
    simulated_values_cross['prob_G']
    * simulated_values_cross['cela_SS_G']
    / denominator_G
).sum()

print(
    f'Aggregate cross point elasticity of garage wrt search time of on-street parking: '
    f'{cross_elas_term_SS_G:.3g}'
)



