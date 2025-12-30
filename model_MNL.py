"""
Model estimation for a the MNL-model
Ville Isoranta / 29.10.2025
"""
import biogeme.biogeme as bio 
from biogeme import models 

"""
Imports the necessary variables.
"""
from data_preparation import (
    database,
    CHOI,
    )
"""
Imports the utility functions.
"""
from MNL_model_initalization import (
    model_initialization_func,
    ) 


"""
Initializes the model through calling
the utility function initialization script
"""

V_MNL, av = model_initialization_func()

logprob_MNL = models.loglogit(V_MNL, av, CHOI)

"""
Creation of the biogeme object.
"""
the_biogeme_MNL = bio.BIOGEME (database , logprob_MNL) 

the_biogeme_MNL.modelName = 'model_mnl_fin' #gives the model a name

"""
Model with zero coefficients
"""
the_biogeme_MNL.calculate_null_loglikelihood (av)

"""
Model estimation
"""
results_MNL = the_biogeme_MNL.estimate () 

"""
Prints summaries
"""
print ("short results")
print (results_MNL.short_summary ())
pandas_results_MNL = results_MNL.get_estimated_parameters()
print ("full results")
print (pandas_results_MNL)



