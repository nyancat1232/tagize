
def numerical_derivative(func,current_x,epoch=10):
    def deriv(func,current_x:float):
        def numerical_diff(func,current_x,delta=1):
            return (func(current_x+delta)-func(current_x-delta))/(2*delta)
        def mean_weight(nums,weights):
            return sum([a*b for a,b in zip(nums,weights)])/sum(weights)
        
        dic_res={'slope':[],'weight':[]}
        delt=4
        while True:
            delt = delt/2
            slope=numerical_diff(func,current_x,delt)

            dic_res['slope'].append(slope)
            dic_res['weight'].append(1./delt)
            
            try:
                diff_slope_pre = abs(dic_res['slope'][-2]-dic_res['slope'][-1])
                if diff_slope_pre<1e-12 and diff_slope_pre<abs(slope-dic_res['slope'][-1]-slope):
                    print(f'warning {diff_slope_pre} {abs(slope-dic_res["slope"][-1]-slope)}')
            except:
                pass

            yield mean_weight(dic_res['slope'],dic_res['weight'])
    
    ret=None
    for _,val in zip(range(epoch),deriv(func,current_x)):
        ret = val
    return ret