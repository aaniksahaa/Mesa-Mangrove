import random

def get_normally_distributed_data(mean,cov,size):
    std_dev = cov*mean
    data = [random.normalvariate(mean, std_dev) for i in range(size)]
    for i in range(size):
        data[i] = round(data[i])
    return data