import torch
from dataclasses import dataclass,field

from typing import Any,Dict,Callable
#https://pytorch.org/tutorials/beginner/pytorch_with_examples.html
@dataclass
class TorchPlus:
    meta_optimizer : torch.optim.Optimizer = torch.optim.SGD
    meta_optimizer_learning_rate : float = 0.015
    meta_optimizer_epoch : int = 2000
    meta_error_measurement : Any = torch.nn.MSELoss
    meta_activator : Any = None
    
    all_leaf_tensors : Dict[str,torch.Tensor] = field(default_factory=dict)

    assign_leaf_tensors : Callable = None
    assign_process_process : Callable = None

    def get_all_params(self):
        return [self.all_leaf_tensors[key] for key in self.all_leaf_tensors if self.all_leaf_tensors[key].requires_grad]
    def train_one_step_by_equation(self,label,prediction_quation):
        loss = self.meta_error_measurement()(label,  prediction_quation)
        optim = self.meta_optimizer(self.get_all_params(),lr=self.meta_optimizer_learning_rate)
        optim.zero_grad()
        loss.backward()
        optim.step()
    def train(self):
        #all terminals
        self.assign_leaf_tensors(self)
        
        for _ in range(self.meta_optimizer_epoch):
            #process
            self.assign_process_process(self)

            #train
            self.train_one_step_by_equation(self._label,self._pred)
        return self.get_all_params()