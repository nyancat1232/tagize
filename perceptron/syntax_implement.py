from pyplus.perceptron.graph import Node
def _reflect_before(optimizer,epoch,_locals):
    def func(answer,predict,_locals=_locals):
        ret = {l:_locals[l] for l in _locals}
        e = predict + Node(-answer)
        for _ in range(epoch):    #will be reflec(100) 1600 c
            e.forward()
            e.backward()
            e.apply_all_gradient_recursive()
        return ret
    return func

def reflect(_locals):
    def func(optimizer,epoch):
        return _reflect_before(optimizer,epoch,_locals)
    return func

#!Relu
#model Xor:
#    def MakeFunc(arr):
#        return arr[0]*?randint() + arr[1]*?randint()
#    reflect(Adam(100)) [0,1,1,0],MakeFunc([[0,0],[1,0],[0,1],[1,1]])
#
#Xor.to_regular_python()
#> def xor():
#>     def MakeFunc(arr):
#>         return arr[0]*0.5 + arr[1]*0.2
#>     return 0.5, 0.2

#!Relu
#model Xor:
#    def MakeFunc(arr):
#        return arr[0]*?randint() + arr[1]*?randint()
#    reflect(Adam(100)) [0,1,1,0],MakeFunc([[0,0],[1,0],[0,1],[1,1]]) MakeFunc
#
#Xor.to_regular_python()
#> def xor():
#>     def MakeFunc(arr):
#>         return arr[0]*0.5 + arr[1]*0.2
#>     return MakeFunc