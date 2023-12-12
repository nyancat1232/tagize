import numpy as np
from typing import Self,List,Any,Callable,Union,Iterator
from dataclasses import dataclass,field

def _mult_forw(ins_shallow: List[float])->float:
    prod = 1.
    for l in ins_shallow:
        prod = prod* l
    return prod

def _mult_back(out:float,ins_shallow: List[float],in_index:int)->float:
    but_me=[v for i,v in enumerate(ins_shallow) if i != in_index]
    prod=1
    for val in but_me:
        prod*=val
    return prod*out


def _add_each_nodes(self,other, func_forward: Callable[[List],float], func_backward : Callable[[float,List,int],float]):
    nb = NodeBridge(forward_value=0.0,func_forward=func_forward,func_backward=func_backward)
    nb.ins.append(self)
    nb.ins.append(other)

    return nb

def default_optimizer(learning_rate=0.01):
    def func(forward_value,backward_value):
        return forward_value-learning_rate*backward_value
    return func


@dataclass
class Node:
    forward_value : Any
    is_parameter: bool = False

    backward_value : float = field(init=False)

    def __post_init__(self):
        self.backward_value = 0.0

    def __add__(self:Self,other:Self):
        return _add_each_nodes(self,other,lambda ins_shallow:sum(ins_shallow),lambda output,ins_shallow,current_in:output)
    
    def __mul__(self:Self,other:Self):
        return _add_each_nodes(self,other,_mult_forw,_mult_back)

    def __str__(self:Self):
        return f'value={self.forward_value}, back value={self.backward_value}'
    
    def _apply_gradient(self:Self,func_optimizer_set):
        if self.is_parameter:
            self.forward_value = func_optimizer_set(self.forward_value,self.backward_value)

    def __iter__(self):
        return iter(self.forward_value)
    
    
@dataclass
class NodeBridge(Node):
    func_forward : Callable[[List],float] = lambda ins:None
    func_backward : Callable[[float,List,int],float] = lambda output,ins_shallow,current_in:None

    ins : List[Union[Node,Self]] = field(default_factory=list,init=False)

    def __post_init__(self):
        super().__post_init__()
        self.ins = []

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
    
    def backward(self:Self,is_terminal=True):
        #terminal node
        if is_terminal:
            self.backward_value=self.forward_value


        #ret=[]
        for ind,node_in in enumerate(self.ins):
            node_in.backward_value = self.func_backward(self.backward_value,self._get_shallow_ins(),ind)
            #node_in._apply_gradient()
            try:
                node_in.backward(False)
            except:
                pass

        #return ret

    def apply_all_gradient_recursive(self:Self,func_optimizer_set):
        for node_in in self.ins:
            try:
                node_in.apply_all_gradient_recursive(func_optimizer_set)
            except:
                pass
            finally:
                node_in._apply_gradient(func_optimizer_set)

    def __str__(self):
        fill_padding_lines=4

        lines = ['' for l in range(len(self.ins)*fill_padding_lines)]
        for line_ind,v in enumerate(self.ins):
            if v.is_parameter:
                lines[line_ind*fill_padding_lines] += '*'
            lines[line_ind*fill_padding_lines] += str(v.forward_value) + '-'*10
            lines[line_ind*fill_padding_lines+1] += ' '*5+str(v.backward_value)+ ' '*4+'|'*1
            lines[line_ind*fill_padding_lines+2] += ' '*3+ ' '*9

        #lines[0]+='-'*4+"("+self._symbol+')'+'-'*5
        lines[0]+=str(self.forward_value)
        ret = "\n".join(lines)
        return ret