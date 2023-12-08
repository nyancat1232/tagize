from dataclasses import dataclass,field
from typing import Callable,List,Union,Self,Dict,Any

@dataclass
class Node:
    learning_rate : float = 0.01

    ins_forward : List[Union[float,Self]] = field(default_factory=list)
    ins_is_parameter : List[bool] = field(default_factory=list)
    ins_backward : List[float] = field(default_factory=list)
    out_forward : float = 0.0
    out_backward : Self = None
    out_backward_address : int = -1


    _single_input=False


    def connect_previous_node(self:Self,previous_node:Self,is_a_parameter=False):
        if self._single_input and len(self.ins_forward):
            raise "Cannot add more than one input."
        try:
            previous_node.out_backward_address = len(self.ins_backward)
        except:
            pass

        self.ins_forward.append(previous_node)
        self.ins_is_parameter.append(is_a_parameter)
        self.ins_backward.append(0.0)
        try:
            previous_node.out_forward = 0.0
            previous_node.out_backward = self
        except:
            pass

    def get_shallow_ins(self):
        temp=[]
        for in_forward in self.ins_forward:
            try:
                elem=in_forward.out_forward
            except:
                elem=in_forward
            temp.append(elem)
        return temp
    
    def _refresh_out_previous(self):
        temp=[]
        for in_forward in self.ins_forward:
            try:
                elem=in_forward.forward()
            except:
                elem=in_forward
            temp.append(elem)
        return temp

    def forward(self) -> float:
        '''
        calculate from input to output
        ## See Also:
        backward
        ## Examples:
        ...

model_1 = Mult()
model_1.connect_previous_node(3)
model_1.connect_previous_node(2)
model_1.forward()
> 6
...
        '''
        temp=self._refresh_out_previous()

        self.out_forward=self._forw_func(temp)
        return self.out_forward
    
        
    def refresh_gradient(self) -> List[float]:
        '''
        reflect partial derivation from output to each input
        ## See Also:
        backward
        ## Examples:
            >3\n
            >_x_6\n
            >2\n
            >____+_2\n
            >__-4\n
\n
            model_1 = Mult()\n
            model_1.connect_previous_node(3.)\n
            model_1.connect_previous_node(2.)\n
            model_2 = Add()\n
            model_2.connect_previous_node(model_1)\n
            model_2.connect_previous_node(-4.)\n
            model_2.forward()\n
            model_2.backward()\n
            backpropagation_result_of_model_1=model_1.backward()\n
            backpropagation_result_of_model_1
            > [4,6]
        '''
        if self.is_terminal():
            self.ins_backward= self._back_func(self.out_forward,self.get_shallow_ins())
        else:
            self.ins_backward= self._back_func(self.out_backward.backward()[self.out_backward_address],self.get_shallow_ins())
        return self.ins_backward

    
    def is_terminal(self):
        return self.out_backward is None

    def summary(self):
        fill_padding_lines=4

        lines = ['' for l in range(len(self.ins_forward)*fill_padding_lines)]
        for line_ind,v in enumerate(zip(self.get_shallow_ins(),self.ins_backward)):
            lines[line_ind*fill_padding_lines] += str(v[0]) + '-'*10
            lines[line_ind*fill_padding_lines+1] += ' '*5+str(v[1])+ ' '*4+'|'*1
            lines[line_ind*fill_padding_lines+2] += ' '*3+ ' '*9
            if line_ind < fill_padding_lines*(len(self.ins_forward)-1)-1:
                lines[line_ind*fill_padding_lines+2] += '|'*1
        lines[0]+='-'*4+"("+self._symbol+')'+'-'*5
        lines[0]+=str(self.out_forward)
        ret = "\n".join(lines)
        return ret
        #return f'''\n
        #{"forward_line":_>20.20} {"backward_line":_>20.20}\n
        #{str(self.get_shallow_ins()):_>20.20} {str(self.ins_backward):_>20.20}\n
        #{str(self.out_forward):_>20.40} {str(self.out_backward):_>20.40} {str(self.out_backward_address):_>20.20}\n
        #'''
    
    def summary_python_code(self,count=0):
        line=[]
        for index,in_forward in enumerate(self.ins_forward):
            try:
                line.append(f"temp{index}{count+1} = "+in_forward.summary_python_code(count+1)+f"\ntemp{index}{count} = temp{index}{count+1}")
            except:
                line.append(str(in_forward))
        return f'{self._symbol.join(line)}'
    
@dataclass
class Add(Node):
    _symbol = '+'

    def _forw_func(self,arr):
        return sum(arr)

    def _back_func(self,out_back,ins_shallow_forw):
        return [out_back for current_in in ins_shallow_forw]
        #return out_back

@dataclass
class Mult(Node):
    _symbol = '*'

    def _forw_func(self,arr):
        prod=1
        for a in arr:
            prod*=a
        return prod

    def _back_func(self,out_back,ins_shallow_forw):
        rr=[]
        for ind,_ in enumerate(ins_shallow_forw):
            ins_shallow_forw_but_me = ins_shallow_forw.copy()
            del ins_shallow_forw_but_me[ind]
            prod=1
            for in_shallow_forw_but_me in ins_shallow_forw_but_me:
                prod*=in_shallow_forw_but_me
            rr.append(prod*out_back)
        return rr

@dataclass
class Inv(Node):
    _symbol = '_/'
    _single_input = True

    def _forw_func(self,arr):
        return 1./arr[0]
    def _back_func(self,out_back,ins_shallow_forw):
        return out_back*-1./(ins_shallow_forw[0]**2)
    

# y=ax+b, x=1,y=3
# a<-random
# b<-random
# layer1=Mult([a,x])
# layer2=Add([layer1,b])
# layer_error=Add([layer2,-y],terminal=True)