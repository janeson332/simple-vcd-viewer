import numpy as np

class vcd_timescale:
    _units = {"s":1,
                  "ms":1e-3,
                  "us":1e-6,
                  "ns":1e-9,
                  "ps":1e-12,
                  "fs":1e-15}
    def __init__(self,factor=1.0,unit:str="s"):
        if(unit not in self._units):
            raise ValueError("invalid unit")

        self.factor = float(factor)
        self.unit = unit

    def n_to_time(self):
        return self.factor * self._units[self.unit]

    def time_to_n(self):
        return 1.0/(self.factor*self._units[self.unit])
        
    def __str__(self):
        return "{0} {1}".format(self.factor,self.unit)


class vcd_pwl:
    def __init__(self,a,b,t0,time_scale:vcd_timescale):
        self.a = a
        self.b = b 
        self.t0 = t0 
        self.timescale = time_scale

    def eval(self,t=None,time_scale:vcd_timescale=None):
        if t is None:
            t = self.t0
        if time_scale is None:
            time_scale = self.timescale

        return self.a + self.b*(t*time_scale.n_to_time() - self.t0*self.timescale.n_to_time())

    def __str__(self):
        return "{0} + {1} * (t-{2} {3})".format(self.a,self.b,self.t0,self.timescale.unit)

def vcd_pwl_tv_to_cont(tv,endtime=None):
    repeated = vcd_tv_to_continous_time(tv)

    v = np.zeros(len(repeated[0]))
    t = repeated[0]

    for i,time in enumerate(t):
        v[i] = repeated[1][i].eval(time)

    return (t,v)




def vcd_tv_to_continous_time(tv):


    t = np.array(tv[0])
    v = np.array(tv[1])

    t = t.repeat(2)[1:]
    v = v.repeat(2)[:-1]

    return(t,v)

