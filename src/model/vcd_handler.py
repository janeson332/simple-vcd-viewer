#from lib.vcdvcd.vcdvcd.vcdvcd import VCDVCD
from lib import VCDVCD
#from model.vcd_datatypes import timescale, vcd_signal_type,vcd_real_type,vcd_pwl_type
from model.vcd_datatypes import vcd_tv_to_continous_time
from model.vcd_datatypes import vcd_timescale,vcd_pwl,vcd_pwl_tv_to_cont
import collections
import matplotlib.pyplot as plt
import numpy as np

class VCDHandler:
    def __init__(self,filename=None):
        self._filename = filename
        
        self._vcd = None
        self._begin_time = 0
        self._end_time = 0
        self._timescale = vcd_timescale()
        self._tv_signals = {}

    @property
    def filename(self):
        return self._filename
    
    @filename.setter
    def filename(self,value):
        if(value is not None):
            self._filename = value

    @property
    def signal_names(self):
        return self._tv_signals.keys()

    @property
    def timescale(self):
        return self._timescale

    def read_vcd_file(self)->bool:
        try:
            # read vcd file
            self._vcd = VCDVCD(self._filename)
            
            # parse vcd file into internal representation
            self._begin_time = self._vcd.begintime
            self._end_time = self._vcd.endtime
            self._timescale = vcd_timescale(self._vcd.timescale["magnitude"],self._vcd.timescale["unit"])
            self._tv_signals = {}
            id_to_references = {y:x for x,y in self._vcd.references_to_ids.items()}

            for vcd_data_ref,vcd_data_val in self._vcd.data.items():
                if vcd_data_ref in id_to_references:
                    name = id_to_references[vcd_data_ref]
                else:
                    name = vcd_data_ref
                
                tv = vcd_data_val.tv
                t = np.zeros(len(tv),dtype=float)
                v = list(np.zeros(len(tv),dtype=str))
                for i in range(len(tv)):
                    t[i]=tv[i][0]
                    v[i]=str(tv[i][1])
                # asume here float values ..
                # can cause a failure ...
                v = np.array(v)
                v = v.astype(float)
                self._tv_signals[name] = (t,v)
                
            return True
            
        except Exception:
            pass

        return False

    def build_pwl_vcd(self,a:str,b:str):
        #check if signals exist
        if(a not in self._tv_signals.keys() or b not in self._tv_signals.keys()):
            raise ValueError("given signal names do not exist")

        tv_a = self._tv_signals[a]
        tv_b = self._tv_signals[b]

        a_idx = 0
        b_idx = 0
        cur_t = 0

        pwls_v = [vcd_pwl(0,0,0,self._timescale)]*(len(tv_a[0])+len(tv_b[0]))
        pwls_v = np.array(pwls_v)
        pwls_t = np.zeros(len(tv_a[0])+len(tv_b[0]))
        pwls_idx = 0

        next_a_t = 0
        next_b_t = 0
        while(next_a_t != float("inf") or next_b_t != float("inf")):
            a = tv_a[1][a_idx]
            b = tv_b[1][b_idx]

            pwl = vcd_pwl(a,b,cur_t,self._timescale)
            pwls_v[pwls_idx] = pwl
            pwls_t[pwls_idx] = cur_t
            pwls_idx+=1

            next_a_t = float("inf")
            next_b_t = float("inf")
            if(a_idx < (len(tv_a[0])-1)):
                next_a_t = tv_a[0][a_idx+1]

            if(b_idx < (len(tv_b[0])-1)):
                next_b_t = tv_b[0][b_idx+1]

            if(next_a_t==next_b_t):
                a_idx+=1
                b_idx+=1
                cur_t = next_a_t
            elif(next_a_t<next_b_t):
                a_idx+=1
                cur_t = next_a_t
            else:
                b_idx+=1
                cur_t = next_b_t

            if a_idx >= len(tv_a[0]):
                a_idx = len(tv_a[0])-1

            if b_idx >= len(tv_b[0]):
                b_idx = len(tv_b[0])-1
            

        pwls_t = pwls_t[0:pwls_idx]
        pwls_v = pwls_v[0:pwls_idx]

        pwls_tv = (pwls_t,pwls_v)
  
        return pwls_tv

    
    
            


if __name__ == "__main__":
    vcd_handler = VCDHandler()
    vcd_handler.filename = "./src/model/pwl_t_vcd.vcd"
    vcd_handler.read_vcd_file()
    x = vcd_handler.build_pwl_vcd("SystemC.Out_pwl_t.ac","SystemC.Out_pwl_t.b")
    #for i in x[1]:
      #  print(i)
    
    ab = vcd_pwl_tv_to_cont(x)
    plt.figure()
    plt.plot(*ab)
    plt.show()


    
    #ret = vcd_handler.read_signal_names_from_vcd()
    #vcd_handler.get_signal(vcd_handler.signal_names[1])
    #print(ret)
