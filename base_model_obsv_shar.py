"""
Version: 28.9.2025
Ville Isoranta
This is the base model for replicating the sample market shares, see 
Section 4.2.1 footer 49 for more discussion
"""
import biogeme.biogeme as bio # import the Biogeme itself
from biogeme import models # import models from Biogeme
from biogeme.expressions import Beta # Required to estimate the beta-coefficients
from biogeme.nests import OneNestForNestedLogit, NestsForNestedLogit # Import NL model
from scipy.stats import chi2 # import chi-square distribution for model comparison

from data_preparation import (
        database,
        COMM_AVAI_TRAN,
        CHOI,
    )

def model_initialization_func_base ():

    """
    Only the ACSs are estimated
    to replicate the sample
    modal shares
    """
    ASC_G = Beta('ASC_G', 0, None, None, 0)
    ASC_S = Beta('ASC_S', 0, None, None, 0)
    ASC_TRA = Beta('ASC_TRA', 0, None, None, 1) # 1 as is the normalized ASC

    V_G = (
        ASC_G 
    )

    V_S = (
        ASC_S 
    )

    V_TRAN = (
        ASC_TRA  
    )

    V_comp = {1: V_G , 2: V_S , 3: V_TRAN } # Joins the choice to the utility function

    av = {1: 1, 2: 1, 3:COMM_AVAI_TRAN}  # Sets an availability condition

    return V_comp, av



V_comp, av = model_initialization_func_base()

"""
Creation of the biogeme object.
"""
logprob_base = models.loglogit(V_comp, av, CHOI)
the_biogeme_base = bio.BIOGEME (database , logprob_base) 
the_biogeme_base.modelName = 'model_base' 

"""
Orders calculation of also the 
equal market share base model
"""
the_biogeme_base.calculate_null_loglikelihood (av)

"""
Estimates the model 
"""
results_base = the_biogeme_base.estimate () 

"""
Prints summaries
"""
print ("short results comp")
print (results_base.short_summary ())

pandas_results_comp = results_base.get_estimated_parameters()

print ("full results comp")
print (pandas_results_comp)

