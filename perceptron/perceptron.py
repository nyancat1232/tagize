from dataclasses import dataclass,field
from typing import Callable,List,Union,Self,Dict,Any

@dataclass
class Node:
    learning_rate : float = 0.01
    is_terminal : bool = False

    ins_forward : List = field(default_factory=list)
    ins_backward : List = field(default_factory=list)
    outs_forward : float = 0.0
    outs_backward : float = 0.0


    def connect_ins(self,node):
        self.ins_forward.append(node)
        self.ins_backward.append(0.0)
    
    def forward(self):
        for in_forward in self.ins_forward:
            try:
                print(in_forward)
                in_forward.forward()
            except:
                continue

        temp=[]
        
        self.outs_forward = self._forw_func(self.ins_forward)
        if self.is_terminal:
            self.outs_backward = self.outs_forward
        return self
    
    def backward(self):
        self.ins_backward = [self._back_func(self.outs_backward,inp) for inp in self.ins_forward]
        return self
    
    def summary(self):
        return f'''\n
        {"forward_line":_>20.20} {"backward_line":_>20.20}\n
        {str(self.ins_forward):_>20.20} {str(self.ins_backward):_>20.20}\n
        {str(self.outs_forward):_>20.20} {str(self.outs_backward):_>20.20}\n
        '''


class Add(Node):
    def __init__(self,learning_rate:float=0.01,is_terminal=False):
        self.learning_rate=learning_rate
        self.ins_forward=[]
        self.ins_backward=[]
        self.outs_forward=0.0
        self.outs_backward=0.0
        self.is_terminal=is_terminal

        def _forw_func(ins_f):
            return sum(ins_f)
        self._forw_func = _forw_func

        def _back_func(out_back,in_forw):
            return out_back
        self._back_func = _back_func

class Mult(Node):
    def __init__(self,learning_rate:float=0.01,is_terminal=False):
        self.learning_rate=learning_rate
        self.ins_forward=[]
        self.ins_backward=[]
        self.outs_forward=0.0
        self.outs_backward=0.0
        self.is_terminal=is_terminal

        def _forw_func(ins_f):
            prod=1
            for inn in  ins_f:
                prod*=inn
            return prod
        self._forw_func = _forw_func

        def _back_func(out_back,in_forw):
            raise "ooo"
        self._back_func = _back_func


# y=ax+b, x=1,y=3
# a<-random
# b<-random
# layer1=Mult([a,x])
# layer2=Add([layer1,b])
# layer_error=Add([layer2,-y],terminal=True)