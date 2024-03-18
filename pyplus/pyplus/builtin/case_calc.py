import itertools

class CaseCalc:
    '''
    Calculation for all cases. 

    If you have difficulty in deciding something, this will be helpful.
    
    Examples
    --------
    >>> cc2 = bp.CaseCalc()
    >>> cc2['fruit']={'apple','banana','orange'}
    >>> cc2['eat']={True,False}
    >>> cc2-={'eat':False,'fruit':'apple'}
    >>> cc2.get_all_case()
    {('apple', True),
    ('banana', False),
    ('banana', True),
    ('orange', False),
    ('orange', True)}
    '''
    samples : dict[str,set]
    exclusion : list[dict[str,set]]
    def __init__(self):
        self.samples = dict()
        self.exclusion = list()
    def __setitem__(self,key:str,value:set):
        self.samples[key]=value
        return self
    def __isub__(self,other:dict[str,set]):
        self.exclusion.append(other)
        return self
    def __repr__(self):
        return f'Case:{repr(self.samples)}\nCase exclusion: {self.exclusion}'
    def get_all_case(self):
        order = self.samples.keys()
        exclusion_sorted = [{key:exclusion[key] for key in order} 
                                for exclusion in self.exclusion]
        exclusion_vals = [tuple(exc.values()) for exc in exclusion_sorted]
        return {case for case 
        in itertools.product(*self.samples.values()) if case not in exclusion_vals}
    def input_something(self,display:str)->str:
        raise NotImplementedError('You must implement input_something(self,display:str)->str.')
    def ask_all_case(self)->dict[tuple,str]:
        all_case = self.get_all_case()
        ret_dict = dict()
        for case in all_case:
            ret_dict[case] = self.input_something(f'When {case}?')
        return ret_dict