"""
Estimates the PML model for the secondary sample. 
Ville Isoranta / 29.10.2025
"""
import biogeme.biogeme as bio # import the Biogeme itself
from biogeme import models # import models from Biogeme
from biogeme.expressions import Beta, bioDraws, PanelLikelihoodTrajectory,MonteCarlo, log # Required to estimate the beta-coefficients
from biogeme.nests import OneNestForNestedLogit, NestsForNestedLogit # Import NL model
from scipy.stats import chi2 # import chi-square distribution for model comparison
import numpy as np

"""
Imports the necessary variables.
"""
from data_preparation import (
    database_full,
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
the_biogeme = bio.BIOGEME(database_full, logprob, number_of_draws = 4000, seed = 4000)
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


