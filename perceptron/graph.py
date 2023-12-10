import numpy as np
from typing import Self,List,Any,Callable
from dataclasses import dataclass,field


def _add_each_nodes(self,other, func_forward: Callable[[List],float]):
    nb = NodeBridge(forward_value=0.0,func_forward=func_forward)
    nb.ins.append(self)
    nb.ins.append(other)
    return nb


@dataclass
class Node:
    forward_value : Any
    is_parameter: bool = False
    backward_value : float = field(init=False)

    def __post_init__(self):
        self.backward_value = 0.0

    def __add__(self:Self,other:Self):
        return _add_each_nodes(self,other,lambda nodes:sum(nodes))
    
    def __mul__(self:Self,other:Self):
        def _ret_func(ll):
            prod = 1.
            for l in ll:
                prod *= l
            return prod
        return _add_each_nodes(self,other,_ret_func)
    
    def __str__(self:Self):
        return f'value={self.forward_value}, back value={self.backward_value}'
    
@dataclass
class NodeBridge(Node):
    func_forward : Callable[[List],float] = lambda ins:None
    learning_rate : float = 0.01

    ins : List[Node] = field(default_factory=list,init=False)

    def __post_init__(self):
        self.ins = []


    def __add__(self:Self,other:Self):
        return _add_each_nodes(self,other,lambda nodes:sum(nodes))
    
    
    def _get_shallow_ins(self):
        return [ii.forward_value for ii in self.ins]

    

    def forward(self):
        pass
        #self.forward_value.forward_value = self.func_forward(self._get_shallow_ins())
        #return self.forward_value
    
    def backward(self:Self):
        rr=[]
        for i in self.ins:
            rr.append()
    
    def __repr__(self):
        return self.out
    
    def __str__(self):
        return f'In :\n{self.ins}\nOut :\n{self.out}'
        