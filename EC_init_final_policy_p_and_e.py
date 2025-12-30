"""
This is the script for computing the joint policy scenario
of price and egress time chnages 
discussed in Section 4.2.5 in Figures 12 and 13.
The search time is set to 1 minute for all
decision-makers
"""

import biogeme.biogeme as bio 
from biogeme import models 
from biogeme.expressions import Beta, bioDraws, PanelLikelihoodTrajectory,MonteCarlo, log 
import numpy as np

def model_ini_p_e(p, e):
    from data_preparation import (
        WEEKS,
        COMM_FREQ_CAR,
        COMM_DURA_TRAN,
        COMM_AVAI_TRAN,
        DRIV_EXPE_TWOP,
        AGE_35,
        AGE_55,
        GEND_WOME,
        INCO_HIGH,
        EDUC_HIGH,
        CHOI
        )
    np.random.seed(seed=1010) # Seet so that results can be replicated

    """
    Defines the beta-parameters to be estimated .
    Syntax is of form: Name, default value, a lower bound, a upper bound, a flag which is
    0 if the parameter is to be estimated and 1 if it is not estimated.
    """
    """
    ASCs that are normally distributed.
    """
   
    ASC_G = Beta('ASC_G', 0, None, None, 0)
    ASC_G_S = Beta('ASC_G_S', 1, None, None, 0)
    ASC_G_RND = ASC_G + ASC_G_S * bioDraws('ASC_G_RND', 'NORMAL_MLHS_ANTI') #_MLHS_ANTI
        
    ASC_S = Beta('ASC_S', 0, None, None, 0)
    ASC_S_S = Beta('ASC_S_S', 1, None, None, 0)
    ASC_S_RND = ASC_S + ASC_S_S * bioDraws('ASC_S_RND', 'NORMAL_MLHS_ANTI')
        
    ASC_TRA = Beta('ASC_TRA', 0, None, None, 1) # 1 as is the normalized ASC

    """
    The error components that are normally distributed.
    """
    
    EC_CAR = Beta('EC_CAR', 0, None, None, 1) # Do not evaluate so that mean stays at 0
    EC_CAR_S = Beta('EC_CAR_S', 5, None, None, 0)
    EC_CAR_RND = EC_CAR_S * bioDraws('ESC_CAR_RND', 'NORMAL_MLHS_ANTI')

    EC_TRA = Beta('EC_TRA', 0, None, None, 1) # Do not evaluate so that mean stays at 0
    EC_TRA_S = Beta('EC_TRA_S', 5, None, None, 0)
    EC_TRA_RND = EC_TRA_S * bioDraws('ESC_TRA_RND', 'NORMAL_MLHS_ANTI')

    """
    The policy variables.
    """

    B_P = Beta('B_P', 0, None, None, 0)
    B_E = Beta('B_E', 0, None, None, 0)
    B_S = Beta('B_S', 0, None, None, 0)
    
    """
    The other covariates.
    """

    B_COMM_DURA_TRAN = Beta('B_COMM_DURA_TRAN', 0, None, None, 0)
    B_DRIV_EXPE = Beta('B_DRIV_EXPE', 0, None, None, 0)
    B_EDUC_HIGH = Beta('B_EDUC_HIGH', 0, None, None, 0)
    B_GEND_WOME = Beta('B_GEND_WOME', 0, None, None, 0)
    B_INCO_HIGH = Beta('B_INCO_HIGH', 0, None, None, 0)
    B_AGE_35 = Beta('B_AGE_35', 0, None, None, 0)
    B_AGE_55 = Beta('B_AGE_55', 0, None, None, 0)

    """
    Calibration constant to allow the model
    to replicate the RP-modal shares
    as discussed in Section 3.3.6.
    """ 
    CONST = Beta('CONST', 0.781, None, None, 1)

    """
    The utility functions as specified in equations 27-29 in Section 3.3.6. The 
    calibration constant was added to utility function of both car
    alternative as discussed in Section 3.3.6.
    """

    V1_ML = (
            ASC_G_RND  + CONST +
            B_P * (p/((COMM_FREQ_CAR*2)*WEEKS)) +
            B_E * e +
            B_S * 1 + 
            B_AGE_35 * AGE_35 +
            B_AGE_55 * AGE_55 +
            B_EDUC_HIGH * EDUC_HIGH +
            B_GEND_WOME * GEND_WOME +
            B_DRIV_EXPE * DRIV_EXPE_TWOP +
            B_INCO_HIGH * INCO_HIGH +
            EC_CAR_RND 
        )
    """
    The price is transformed
    into trip-based cost with Equation 5 as in all
    other specifications. However, for computational
    ease it is calculated in this specification
    within the utility function. In most other specifications
    (specifications not using database_MASA)
    the price coefficient is computed already 
    in the data_preparation.py file and therefore
    the Equation 5 is not visible in the utility
    functions.
    """
    V2_ML = (
            ASC_S_RND  + CONST +
            B_P * (p/((COMM_FREQ_CAR*2)*WEEKS)) +
            B_E * e +
            B_S * 1 + 
            B_AGE_35 * AGE_35 +
            B_AGE_55 * AGE_55 +
            B_EDUC_HIGH * EDUC_HIGH +
            B_GEND_WOME * GEND_WOME +
            B_DRIV_EXPE * DRIV_EXPE_TWOP +
            B_INCO_HIGH * INCO_HIGH +
            EC_CAR_RND 
        )

    V3_ML = (
            ASC_TRA +
            B_COMM_DURA_TRAN * (COMM_DURA_TRAN) +
            EC_TRA_RND
        )
        
    V_ML = {1: V1_ML , 2: V2_ML , 3: V3_ML } # Joins the choice to the utility function

    av = {1: 1, 2: 1, 3:COMM_AVAI_TRAN} # Sets an availability condition

    return V_ML, av, CHOI  