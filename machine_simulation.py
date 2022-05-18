import numpy as np

class Machine():
    '''
    prod x ~ N(norm_cap, cap_uncertainty)
    norm_cap: normal capacity of the machine in units/time unit
    cap_uncertainty: variance of the machine output.
    outage_prob: probability of the machine stopping at any given point in time
    exp_outage_length: the expected length of the outage if one occures in time units
    '''

    def __init__(self, normal_capacity: int, cap_uncertainty, outage_prob: float, exp_outage_length: float):
        self.norm_cap = normal_capacity
        self.outage_prob = outage_prob
        self.cap_uncertainty = cap_uncertainty
        self.exp_outage_length = exp_outage_length

    def simulate(self, duration, plot=False):
        
        production = np.zeros(20)
        time = 0
        while time < duration:
            if np.random.random() > self.outage_prob:
                production[time] = np.round(np.random.normal(self.norm_cap, self.cap_uncertainty))
                time += 1
            else:
                outage_length = np.random.poisson(self.exp_outage_length)
                production[time:time+outage_length] = 0
                time += outage_length

        return production
        if plot:
            fig, ax = plt.subplots()
            fig = px.line(production)
            return fig