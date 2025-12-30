"""
This script computes the policy scenarios.
Version 21.10.2025
Ville Isoranta
"""
import biogeme.biogeme as bio # import the Biogeme itself
from biogeme import models # import models from Biogeme
from biogeme.expressions import Beta # Required to estimate the beta-coefficients
from biogeme.nests import OneNestForNestedLogit, NestsForNestedLogit # Import NL model
from scipy.stats import chi2 # import chi-square distribution for model comparison
from biogeme.expressions import Derive
import biogeme.results as res
from IPython.core.display_functions import display
from biogeme.expressions import Beta, bioDraws, PanelLikelihoodTrajectory,MonteCarlo, log # Required to estimate the beta-coefficients

"""
Imports the database used for market share analysis
"""
from data_preparation import(
    database_MASA
)
"""
Imports the utility functions for the price
based policy scenario
"""

from EC_init_final_policy_price import (
    model_ini
)
"""
Imports the utility functions for the egress time
based policy scenario
"""
from EC_init_final_policy_egress import (
    model_ini_egress
)
"""
Imports the utility functions for the search time
based policy scenario
"""
from EC_init_final_policy_search import (
    model_ini_search
)
"""
Imports the utility functions for the joint price-egress time
policy scenario
"""
from EC_init_final_policy_p_and_e import (
    model_ini_p_e
)
"""
Imports the utility functions for the sole price change 
given egress time of 0 minutes and search time of
1 minutes to determine synergy of the joint policy
scenario
"""
from EC_init_final_policy_price_synergy import (
    model_ini_price_synergy
)

"""
Imports the utility functions for the sole egress time change 
given price  of 0 euros and search time of
1 minutes to determine synergy of the joint policy
scenario
"""
from EC_init_final_policy_egress_synergy import (
    model_ini_egress_synergy
)

"""
Loads the beta-coefficient values from the result file. 
"""
results = res.bioResults(pickle_file='removed')
print("MONTHLY PRICE RANGE 0-100")

"""
The first loop defines the price-based scenario (Figure 9
in Section 4.2.5).
Egress time and search time are the current egress and
search time for each decision-maker. 
"""

for i in range(0,101):
    
    V_ML, av,_ = model_ini(i)
    
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
    Creates the biogeme object and conducts the simulation.
    """
    the_biogeme_mark = bio.BIOGEME(database_MASA, simulate)
    simulated_values = the_biogeme_mark.simulate(results.get_beta_values())

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

"""
The second loop defines the egress time-based scenario (Figure 10
in Section 4.2.5).
Price and search time are the current price and
search time for each decision-maker. 
For clarity, the following codes are not commented as they
are identical to the above code. Only the argument 
used to call the utility function script chnages from
price to egress time (and later to search time)
"""
print("EGRESS TIMES RANGE 0-10")

for i in range(0,11):
    
    V_ML, av,_ = model_ini_egress(i)
        
    prob_G= MonteCarlo((models.logit(V_ML, av, 1)))
    prob_S= MonteCarlo((models.logit(V_ML, av, 2)))
    prob_TRAN= MonteCarlo((models.logit(V_ML, av, 3)))

    simulate = {
        'prob_G' : prob_G,
        'prob_S' : prob_S,
        'prob_TRAN' : prob_TRAN
    }

    the_biogeme_mark = bio.BIOGEME(database_MASA, simulate)
    simulated_values = the_biogeme_mark.simulate(results.get_beta_values())

    marketShare_G = simulated_values['prob_G'].mean()

    print(
        f'Market share for Garage: {100*marketShare_G:.2f}% '
    )

    marketShare_S = simulated_values['prob_S'].mean()

    print(
        f'Market share for on-street parking: {100*marketShare_S:.2f}% '
    )

    marketShare_TRAN = simulated_values['prob_TRAN'].mean()

    print(
        f'Market share for public transport: {100*marketShare_TRAN:.2f}% '

    )
"""
The third loop defines the search time-based scenario (Figure 11
in Section 4.2.5).
Price and egress time are the current price and
egress time for each decision-maker. 
"""
print("SEARCH TIMES RANGE 0-10")
for i in range(0,11):
    
    V_ML, av,_ = model_ini_search(i)

    prob_G= MonteCarlo((models.logit(V_ML, av, 1)))
    prob_S= MonteCarlo((models.logit(V_ML, av, 2)))
    prob_TRAN= MonteCarlo((models.logit(V_ML, av, 3)))

    simulate = {
        'prob_G' : prob_G,
        'prob_S' : prob_S,
        'prob_TRAN' : prob_TRAN
    }

    the_biogeme_mark = bio.BIOGEME(database_MASA, simulate)
    simulated_values = the_biogeme_mark.simulate(results.get_beta_values())

    marketShare_G = simulated_values['prob_G'].mean()

    print(
        f'Market share for Garage: {100*marketShare_G:.2f}% '
    )

    marketShare_S = simulated_values['prob_S'].mean()

    print(
        f'Market share for on-street parking: {100*marketShare_S:.2f}% '
    )

    marketShare_TRAN = simulated_values['prob_TRAN'].mean()

    print(
        f'Market share for public transport: {100*marketShare_TRAN:.2f}% '
    )

"""
The fourth loop defines the search joint policy scenario (Figures 12
and 13 in Section 4.2.5).
Price and egress time are varied
and seach time is set as 1 minute. 
"""
print("PRICE RANGE 0-100, EGRESS TIMES, 1, 3, 5, 7, 9, SEARCH TIME = 1")

for e in range(1, 11, 2):
    
    print(f'Egress time is: {e:.2f}')
    
    for p in range(0,101):
        
        V_ML, av,_ = model_ini_p_e(p, e)
            
        prob_G= MonteCarlo((models.logit(V_ML, av, 1)))
        prob_S= MonteCarlo((models.logit(V_ML, av, 2)))
        prob_TRAN= MonteCarlo((models.logit(V_ML, av, 3)))

        simulate = {
            'prob_G' : prob_G,
            'prob_S' : prob_S,
            'prob_TRAN' : prob_TRAN
        }

        the_biogeme_mark = bio.BIOGEME(database_MASA, simulate)
        simulated_values = the_biogeme_mark.simulate(results.get_beta_values())

        marketShare_G = simulated_values['prob_G'].mean()

        print(
            f'Market share for Garage: {100*marketShare_G:.2f}% '
        )

        marketShare_S = simulated_values['prob_S'].mean()

        print(
            f'Market share for on-street parking: {100*marketShare_S:.2f}% '
        )

        marketShare_TRAN = simulated_values['prob_TRAN'].mean()

        print(
            f'Market share for public transport: {100*marketShare_TRAN:.2f}% '

        )

"""
The fifth loop defines the effect of sole price change on modal share
given egress time of 0 minutes and search time of 1 minute.
This information is used to detrmine the synergetic effect
shown in Figure 13
"""
print("PRICE RANGE 0-100, EGRESS TIMES = 0, SEARCH TIME = 1")


for i in range(0,101):
    
    V_ML, av,_ = model_ini_price_synergy(i)
    
    
    prob_G= MonteCarlo((models.logit(V_ML, av, 1)))
    prob_S= MonteCarlo((models.logit(V_ML, av, 2)))
    prob_TRAN= MonteCarlo((models.logit(V_ML, av, 3)))

    simulate = {
        'prob_G' : prob_G,
        'prob_S' : prob_S,
        'prob_TRAN' : prob_TRAN
    }

    the_biogeme_mark = bio.BIOGEME(database_MASA, simulate)
    simulated_values = the_biogeme_mark.simulate(results.get_beta_values())

    marketShare_G = simulated_values['prob_G'].mean()

    print(
        f'Market share for Garage: {100*marketShare_G:.2f}% '
    )

    marketShare_S = simulated_values['prob_S'].mean()

    print(
        f'Market share for on-street parking: {100*marketShare_S:.2f}% '
    )

    marketShare_TRAN = simulated_values['prob_TRAN'].mean()

    print(
        f'Market share for public transport: {100*marketShare_TRAN:.2f}% '
    )

"""
The sixth loop defines the effect of sole egress time change on modal share
given price of 0 euros and search time of 1 minute.
This information is used to detrmine the synergetic effect
shown in Figure 13
"""
print("PRICE = 0, EGRESS TIMES = 0-10, SEARCH TIME = 1")

for i in range(0,11):
    
    V_ML, av,_ = model_ini_egress_synergy(i)
        
    prob_G= MonteCarlo((models.logit(V_ML, av, 1)))
    prob_S= MonteCarlo((models.logit(V_ML, av, 2)))
    prob_TRAN= MonteCarlo((models.logit(V_ML, av, 3)))

    simulate = {
        'prob_G' : prob_G,
        'prob_S' : prob_S,
        'prob_TRAN' : prob_TRAN
    }

    the_biogeme_mark = bio.BIOGEME(database_MASA, simulate)
    simulated_values = the_biogeme_mark.simulate(results.get_beta_values())

    marketShare_G = simulated_values['prob_G'].mean()

    print(
        f'Market share for Garage: {100*marketShare_G:.2f}% '
    )

    marketShare_S = simulated_values['prob_S'].mean()

    print(
        f'Market share for on-street parking: {100*marketShare_S:.2f}% '
    )

    marketShare_TRAN = simulated_values['prob_TRAN'].mean()

    print(
        f'Market share for public transport: {100*marketShare_TRAN:.2f}% '

    )

"""
All the results were saved from the terminal toa txt file
Threafter, final computations and figures were mady with
Excel.
"""
