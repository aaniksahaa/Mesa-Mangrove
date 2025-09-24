import scipy.stats as ss
import math
# outputs data distributed between 0 and 2*min with min as average and given cov as covariance
# cov must be between 0 and 1/sqrt(3)
def get_beta_distributed_data(mean,cov,len):
    max_cov = 1/(math.sqrt(3))
    if(cov > max_cov):
        cov = max_cov
    alpha = beta = 0.5*(1/(cov**2)-1)  # derived
    data = ss.beta.rvs(alpha,beta,size=len)
    data = list(map(lambda x: x*2*mean , data))
    return data