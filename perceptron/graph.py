import numpy as np
from typing import Self,List,Any,Callable,Union
from dataclasses import dataclass,field

def _mult_forw(ll):
    prod = 1.
    for l in ll:
        prod = prod* l
    return prod

def _mult_back(out:Any,ins_shallow: List[float],in_index:int):
    but_me=[v for i,v in enumerate(ins_shallow) if i != in_index]
    prod=1
    for val in but_me:
        prod*=val
    return prod*out


def _add_each_nodes(self,other, func_forward: Callable[[List],float], func_backward : Callable[[Any,List,int],float]):
    nb = NodeBridge(forward_value=0.0,func_forward=func_forward,func_backward=func_backward)
    nb.ins.append(self)
    nb.ins.append(other)

    return nb


@dataclass
class Node:
    forward_value : Any
    is_parameter: bool = False
    learning_rate: float = 0.0001
    backward_value : Union[float,Self] = field(init=False)

    def __post_init__(self):
        self.backward_value = 0.0

    def __add__(self:Self,other:Self):
        return _add_each_nodes(self,other,lambda nodes:sum(nodes),lambda output,ins,current_in:output)
    
    def __mul__(self:Self,other:Self):
        return _add_each_nodes(self,other,_mult_forw,_mult_back)
    

    def __str__(self:Self):
        return f'value={self.forward_value}, back value={self.backward_value}'
    
    def _apply_gradient(self:Self):
        if self.is_parameter:
            self.forward_value -= self.learning_rate*self.backward_value
    
    
@dataclass
class NodeBridge(Node):
    func_forward : Callable[[List],float] = lambda ins:None
    func_backward : Callable[[Any,List,int],float] = lambda output,ins_shallow,current_in:None

    ins : List[Union[Node,Self]] = field(default_factory=list,init=False)

    def __post_init__(self):
        self.ins = []


    def __add__(self:Self,other:Self):
        return _add_each_nodes(self,other,lambda nodes:sum(nodes),lambda output,ins,current_in:output)

    def __mul__(self:Self,other:Self):
        return _add_each_nodes(self,other,_mult_forw,_mult_back)
    
    def _get_shallow_ins(self) -> List[Any]:
        return [ii.forward_value for ii in self.ins]

    def forward(self:Self):
        for node_in in self.ins:
            try:
                node_in.forward()
            except:
                pass

        self.forward_value = self.func_forward(self._get_shallow_ins())
        return self.forward_value
    
    def backward(self:Self,back_val:Any=None):
        #terminal node
        if back_val==None:
            self.backward_value=self.forward_value


        #ret=[]
        for ind,node_in in enumerate(self.ins):
            node_in.backward_value = self.func_backward(self.backward_value,self._get_shallow_ins(),ind)
            node_in._apply_gradient()
            try:
                node_in.backward(node_in.backward_value)
            except:
                pass

        #return ret


        
    
    def __repr__(self):
        return self.out
    
    def __str__(self):
        return f'In :\n{self.ins}\nOut :\n{self.out}'
        