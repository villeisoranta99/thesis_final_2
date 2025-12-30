"""
Model initialization for a the PML-model presented in Equations 6-8
in Section 3.3.2
Ville Isoranta / 17.11.2025
"""
import biogeme.biogeme as bio 
from biogeme import models 
from biogeme.expressions import PanelLikelihoodTrajectory,MonteCarlo, log 

"""
Imports the necessary variables.
"""
from data_preparation import (
    database_SP_PA,
    CHOI,
    )
"""
Imports the script to specify utility fuctions
"""
from EC_init_final import (
    model_ini
)
"""
Initializes the model through calling
the utility function initialization script
"""
V_ML, av, CHOI = model_ini()

obsprob = models.logit(V_ML, av, CHOI)
    
"""
Calculated likelihood for one individual over the repeated
choices (i.e. 9 choice situations)
"""
condprobIndiv = PanelLikelihoodTrajectory(obsprob)
    
"""
Integrates using Monte-Carlo
"""

logprob = log(MonteCarlo(condprobIndiv))
"""
Creation of the biogeme object.
Sets a seed for replicability.  
"""
the_biogeme = bio.BIOGEME(database_SP_PA, logprob, number_of_draws = 4000, seed = 4000)
the_biogeme.modelName = 'ML_final'
the_biogeme.calculate_null_loglikelihood (av)

"""
Estimates the model 
"""
results = the_biogeme.estimate()
"""
Prints summaries
"""
print('Null loglikelihood')
print(results.data.nullLogLike)
print(results.short_summary())
pandas_results = results.get_estimated_parameters()
pandas_results
print(pandas_results)

