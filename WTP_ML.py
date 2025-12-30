"""
WTP_ML.py
Computation of WTP 
Ville Isoranta / 29.10.2025
"""
from IPython.core.display_functions import display
import biogeme.biogeme as bio
import biogeme.results as res
from biogeme.expressions import Derive
from biogeme.expressions import MonteCarlo

"""
Imports the necessary variables.
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
Imports the utility function script
"""
from EC_init_final import (
    model_ini
) 
"""
Obtains the utility functions from the utility
function specification file
"""
V_ML, av, _ = model_ini()
"""
Extraxts each parking type's utility into own variable
"""

V_G = MonteCarlo(V_ML[1])
V_S = MonteCarlo(V_ML[2])
V_TRAN = MonteCarlo(V_ML[3])

"""
Formula for computing the WTP
(equals equation 19 in chapter 3.3.5)
"""
WTP_EG= Derive(V_G, ('EG')) / Derive(V_G, ('PG_NORM_TRIP'))
WTP_SG= Derive(V_G, ('SG')) / Derive(V_G, ('PG_NORM_TRIP'))
WTP_ES= Derive(V_S, ('ES')) / Derive(V_S, ('PS_NORM_TRIP'))
WTP_SS= Derive(V_S, ('SS')) / Derive(V_S, ('PS_NORM_TRIP'))

"""
Next a dictionary structure is generated.
The structure contains all quantities to be simulated.
"""
simulate = {
    'WTP_EG' : WTP_EG,
    'WTP_SG' : WTP_SG,
    'WTP_ES' : WTP_ES,
    'WTP_SS' : WTP_SS,
}


"""
Creates the biogeme object, conducts the simulation, and
loads the beta-coefficient values from the result file. 
"""

the_biogeme_wtp = bio.BIOGEME(database, simulate)
results = res.bioResults(pickle_file='REMOVED')
simulated_values_wtp = the_biogeme_wtp.simulate(results.get_beta_values())

"""
Displays values for a sanity check
"""
display(simulated_values_wtp)

"""
Calculates the confidence intervals (based on a simulation) from 5 to 95%
"""

betas = the_biogeme_wtp.free_beta_names
print(betas)
b = results.get_betas_for_sensitivity_analysis(betas, size = 1000, use_bootstrap=False) 
left, right = the_biogeme_wtp.confidence_intervals(b, 0.95)
"""
Computes the WTP as €/hour and takes the average of the 
simulated WTPs
"""

WTP_EG = (60*simulated_values_wtp['WTP_EG']).mean()
WTP_SG = (60*simulated_values_wtp['WTP_SG']).mean()
WTP_ES = (60*simulated_values_wtp['WTP_ES']).mean()
WTP_SS = (60*simulated_values_wtp['WTP_SS']).mean()
WTP_EG_left = (60*left['WTP_EG']).mean()
WTP_EG_right = (60*right['WTP_EG']).mean()
WTP_SG_left = (60*left['WTP_SG']).mean()
WTP_SG_right = (60*right['WTP_SG']).mean()
WTP_ES_left = (60*left['WTP_ES']).mean()
WTP_ES_right = (60*right['WTP_ES']).mean()
WTP_SS_left = (60*left['WTP_SS']).mean()
WTP_SS_right = (60*right['WTP_SS']).mean()

"""
Shows the results.
"""

print(
    f'Average WTP for EG: {WTP_EG:.3g} ' f'CI:[{WTP_EG_left:.3g}, {WTP_EG_right:.3g}]'
)
print(
    f'Average WTP for SG: {WTP_SG:.3g} ' f'CI:[{WTP_SG_left:.3g}, {WTP_SG_right:.3g}]'
)
print(
    f'Average WTP for ES: {WTP_ES:.3g} ' f'CI:[{WTP_ES_left:.3g}, {WTP_ES_right:.3g}]'
)
print(
    f'Average WTP for SS: {WTP_SS:.3g} ' f'CI:[{WTP_SS_left:.3g}, {WTP_SS_right:.3g}]'
)


