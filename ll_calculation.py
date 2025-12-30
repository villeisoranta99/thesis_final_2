"""
This scrip calculates log likelihood and 
pseudo R^2 for the observed market share
base model.
"""
from scipy.stats import chi2 # imports chi-square distribution for model comparison

"""
Likelihood ratio test.
"""
# The next values were manually varied
ll_observed_shares = -2623.126
ll_final_model = -1476.168
ll_equal_shares = -2699.29 # This is the LL for the equal market share model

print("LL final model")
print(ll_final_model) #prints the log likelihoods

print("LL observed market shares")
print(ll_observed_shares)

"""
The test statistic.
"""

lldiff_observed = 2*(ll_final_model-ll_observed_shares)
print("Test statistic for the observed market share model")
print (lldiff_observed)

"""
Number of parameters in the models.
"""
# The next values were manually varied
parameters_final_model = 13
parameters_obs_ms = 2

"""
Degress of freedom.
"""
dofs_observed = parameters_final_model - parameters_obs_ms # calculated dofs
print("dofs for chisq test")
print(dofs_observed)

"""
p-value
cutoff at p=0.05; reject (i.e. keep the null hypothesis of equality) is p>0.05.
"""
p_observed = 1 - chi2.cdf(lldiff_observed, dofs_observed) # defines the p-value (the right hand side of the distribution)
print("p value")
print (p_observed)

"""
Alternatively the critical value
Reject if lower than the critical value
"""
print ("critical value")
print(chi2.ppf(0.95, dofs_observed))

"""
The pseudo R^2
"""
rho = 1-(ll_final_model/ll_observed_shares)
print("rho")
print(rho)

"""
The adjusted psudo R^2
"""

diff = ll_final_model-parameters_final_model
rho_adj = 1-(diff/ll_observed_shares)
print("adj rho")
print(rho_adj)

"""
The rest of the script does the
exactly same procedures for the equal market share model.
These statistics were not reported in the study
due to risk of fit overestimation. These
stats were also automatically reported 
by Biogeme
"""

"""
The test statistic.
"""
lldiff_equal = 2*(ll_final_model-ll_equal_shares)
print("Test statistic for the equal market share model")
print (lldiff_equal)

parameters_equal_ms = 0

"""
Degress of freedom.
"""
dofs_equal = parameters_final_model - parameters_equal_ms 
print("dofs for chisq test")
print(dofs_equal)

"""
p-value
cutoff at p=0.05; reject (i.e. keep the null hypothesis of equality) is p>0.05.
"""
p_equal = 1 - chi2.cdf(lldiff_equal, dofs_equal) 
print("p value")
print (p_equal)



"""
The pseudo R^2
"""
rho = 1-(ll_final_model/ll_equal_shares)
print("rho")
print(rho)

"""
The adjusted psudo R^2
"""
diff = ll_final_model-parameters_final_model
rho_adj = 1-(diff/ll_equal_shares)
print("adj rho")
print(rho_adj)