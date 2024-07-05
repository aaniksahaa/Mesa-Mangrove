import scipy.stats as ss

# outputs Poisson distributed data with given mean
# suitable for non-negative integer data
def get_poisson_distributed_data(mean,len):
    data = ss.poisson.rvs(mean,size=len)
    return data