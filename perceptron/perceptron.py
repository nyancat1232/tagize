from dataclasses import dataclass,field
from typing import Callable,List,Union,Self,Dict,Any

@dataclass
class Node:
    learning_rate : float = 0.01

    ins_forward : List = field(default_factory=list)
    ins_backward : List = field(default_factory=list)
    out_forward : float = 0.0
    out_backward : Any = None


    def connect_previous_node(self:Self,previous_node:Self):
        self.ins_forward.append(previous_node)
        self.ins_backward.append(0.0)
        try:
            previous_node.out_forward = 0.0
            previous_node.out_backward = self
        except:
            pass

    def forward(self):
        temp=[]
        for in_forward in self.ins_forward:
            try:
                elem=in_forward.forward()
            except:
                elem=in_forward
            temp.append(elem)

        self.out_forward=self._forw_func(temp)
        return self.out_forward

        
    def backward(self):
        temp=[]
        for in_forward in self.ins_forward:
            try:
                elem=in_forward.forward()
            except:
                elem=in_forward
            temp.append(elem)

        self.out_forward=self._forw_func(temp)
        return self.out_forward
    
    def is_terminal(self):
        return self.out_backward is None

    def summary(self):
        return f'''\n
        {"forward_line":_>20.20} {"backward_line":_>20.20}\n
        {str(self.ins_forward):_>20.20} {str(self.ins_backward):_>20.20}\n
        {str(self.out_forward):_>20.20} {str(self.out_backward):_>20.20}\n
        '''

@dataclass
class Add(Node):
    def _forw_func(self,arr):
        return sum(arr)

    def _back_func(self,out_back,in_forw):
        return [out_back for current_in in in_forw]
        #return out_back

@dataclass
class Mult(Node):
    def _forw_func(self,arr):
        prod=1
        for a in arr:
            prod*=a
        return prod

    def _back_func(self,out_back,in_forw):
        except_me = [out_back for current_in in in_forw]
        return [out_back for current_in in in_forw]
        #return out_back


# y=ax+b, x=1,y=3
# a<-random
# b<-random
# layer1=Mult([a,x])
# layer2=Add([layer1,b])
# layer_error=Add([layer2,-y],terminal=True)