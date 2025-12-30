"""
Model estimation for a the NL-model presented in 
appendix J. 
Ville Isoranta / 28.9.2025
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
from NL_model_initialization import (
    model_initialization_func,
    ) 


"""
Initializes the model through calling
the utility function initialization script
"""

V_NL, nest_NL, av = model_initialization_func()

"""
Model definition
"""
logprob_NL = models.lognested(V_NL, av, nest_NL, CHOI) #defines the model

"""
Creation of the biogeme object.
"""
the_biogeme_NL = bio.BIOGEME (database , logprob_NL) 
the_biogeme_NL.modelName = 'model_nlall_FIN' 

"""
Model with zero coefficients
"""
the_biogeme_NL.calculate_null_loglikelihood (av)

"""
Model estimation
"""
results_NL = the_biogeme_NL.estimate ()

"""
Prints summaries
"""
print ("short results")
print (results_NL.short_summary ())
pandas_results_NL= results_NL.get_estimated_parameters()

print ("full results")
print (pandas_results_NL)

"""
Prints the error term correlation between alternatives
"""

print("Error term correlation comp")
corr_comp = nest_NL.correlation(
    parameters=results_NL.get_beta_values(),
    alternatives_names={1: 'G', 2: 'S', 3: 'TRAN'},
)
print(corr_comp)

"""
Check whether the scale
parameter value is significantly different from one
"""

mu_NL=pandas_results_NL.loc['MU', 'Value']

std_err_NL = pandas_results_NL.loc['MU', 'Rob. Std err']

print("T-test statistic_comp, actually Wald (Par-hyphotesized value of param)^2/var(par) " \
"as sd = sqrt(var) the t test statistic equals the wald statistic")
"""
Under large samples wald's chisq-
distribution can be approximated with a t-test.
"""
t_test_NL = (mu_NL-1) / std_err_NL
print(t_test_NL)


