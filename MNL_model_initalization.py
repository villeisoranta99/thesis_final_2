"""
This script initializes the MNL model's
utility functions.
Version: 28.9.2025
Ville Isoranta
"""
from biogeme.expressions import Beta 

"""
Imports necessary variables.
"""
from data_preparation import (
        COMM_DURA_TRAN,
        PG_NORM_TRIP,
        PS_NORM_TRIP,
        COMM_AVAI_TRAN,
        GEND_WOME,
        INCO_HIGH,
        EDUC_HIGH,
        AGE_35,
        AGE_55,
        EG,
        ES,
        SG,
        SS,
        DRIV_EXPE_TWOP
    )

def model_initialization_func ():

    """
    Defines the beta-parameters to be estimated .
    Syntax is of form: Name, default value, a lower bound, a upper bound, a flag which is
    0 if the parameter is to be estimated and 1 if it is not estimated.
    """
    """
    The ASCs
    """
    ASC_G = Beta('ASC_G', 0, None, None, 0)
    ASC_S = Beta('ASC_S', 0, None, None, 0)
    ASC_TRA = Beta('ASC_TRA', 0, None, None, 1) # 1 as is the normalized ASC
    """
    The policy variables
    """
    B_P = Beta('B_P', 0, None, None, 0)
    B_E = Beta('B_E', 0, None, None, 0)
    B_S = Beta('B_S', 0, None, None, 0)

    """
    Covariates
    """

    B_COMM_DURA_TRAN = Beta('B_COMM_DURA_TRAN', 0, None, None, 0)
    B_EDUC_HIGH = Beta('B_EDUC_HIGH', 0, None, None, 0)
    B_GEND_WOME = Beta('B_GEND_WOME', 0, None, None, 0)
    B_INCO_HIGH = Beta('B_INCO_HIGH', 0, None, None, 0)
    B_AGE_35 = Beta('B_AGE_35', 0, None, None, 0)
    B_AGE_55 = Beta('B_AGE_55', 0, None, None, 0)
    B_DRIV_EXPE = Beta('B_DRIV_EXPE', 0, None, None, 0)

    """
    Garage utility function. 
    """
    V_G = (
            ASC_G + 
            B_P * PG_NORM_TRIP +
            B_E * EG +
            B_S * SG + 
            B_AGE_35 * AGE_35 +
            B_AGE_55 * AGE_55 +
            B_EDUC_HIGH * EDUC_HIGH +
            B_GEND_WOME * GEND_WOME +
            B_DRIV_EXPE * DRIV_EXPE_TWOP +
            B_INCO_HIGH * INCO_HIGH 
        )
    """
    On-street utility function
    """
    V_S = (
            ASC_S + 
            B_P * PS_NORM_TRIP +
            B_E * ES +
            B_S * SS + 
            B_AGE_35 * AGE_35 +
            B_AGE_55 * AGE_55 +
            B_EDUC_HIGH * EDUC_HIGH +
            B_GEND_WOME * GEND_WOME +
            B_DRIV_EXPE * DRIV_EXPE_TWOP +
            B_INCO_HIGH * INCO_HIGH 
        )
    """
    Public transport utility function
    """
    V_TRAN = (
            ASC_TRA +
            B_COMM_DURA_TRAN * (COMM_DURA_TRAN) 
        )

    V_MNL = {1: V_G , 2: V_S , 3: V_TRAN } # Joins the choice to the utility function

    av = {1: 1, 2: 1, 3:COMM_AVAI_TRAN} # Sets an availability condition

    return V_MNL, av