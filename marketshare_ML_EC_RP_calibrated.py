"""
This script computes the modal shares based on the current price,
egress time, and search time of parking using the calibrated model.
Version 21.10.2025
Ville Isoranta
"""
import biogeme.biogeme as bio 
from biogeme import models 
import biogeme.results as res
from IPython.core.display_functions import display
from biogeme.expressions import MonteCarlo 
"""
Imports the database used for market share analysis
"""
from data_preparation import(
    database_MASA
)

"""
Imports the utility functions for the 
calibrated model. 
"""
from EC_init_final_calibrated import (
    model_ini
)


V_ML, av,_ = model_ini()
    
"""
Defines the choice probabilities
"""  
prob_G= MonteCarlo((models.logit(V_ML, av, 1)))
prob_S= MonteCarlo((models.logit(V_ML, av, 2)))
prob_TRAN= MonteCarlo((models.logit(V_ML, av, 3)))

"""
Next a dictionary structure is generated.
The structure contains all quantities to be simulated.
"""

simulate = {
    'prob_G' : prob_G,
    'prob_S' : prob_S,
    'prob_TRAN' : prob_TRAN
}

"""
Creates the biogeme object, conducts the simulation, and
loads the beta-coefficient values from the result file. 
"""
the_biogeme_mark = bio.BIOGEME(database_MASA, simulate)
results = res.bioResults(pickle_file='file path removed')
simulated_values = the_biogeme_mark.simulate(results.get_beta_values())

"""
Displays values for a sanity check
"""
display(simulated_values)

"""
Market share of garage
"""
marketShare_G = simulated_values['prob_G'].mean()


print(
    f'Market share for Garage: {100*marketShare_G:.2f}% '

)

"""
Market share of on-street parking
"""

marketShare_S = simulated_values['prob_S'].mean()

print(
    f'Market share for on-street parking: {100*marketShare_S:.2f}% '
)

"""
Market share of public transport
"""
marketShare_TRAN = simulated_values['prob_TRAN'].mean()

print(
    f'Market share for public transport: {100*marketShare_TRAN:.2f}% '
)

