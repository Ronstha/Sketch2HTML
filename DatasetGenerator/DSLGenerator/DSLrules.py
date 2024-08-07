graph={
    'root':['header','container','footer'],
    'header':['flex'],
    'nav':['navlink'],
    'logodiv':['image','text'],
    'container':['row'],
    'row':['div-3','div-6','div-9','div-12'],
    'div-3':['text','paragraph','image','card','input','button',],
    'div-6':['text','paragraph','image','card','carousel','input','button','flex'],
    'div-9':['text','paragraph','image','card','carousel','input','table','button','flex'],
    'div-12':['text','paragraph','image','card','carousel','input','table','button','flex'],
    'flex':['text','button'],
    'card':['text','paragraph','image','input','button','flex'],
    'footer':['text']
}

divCombinations = [
    [12],
    [3, 9],
    [6, 6],
    [3, 3, 6],
    [3, 6, 3],
    [9,3]
]
divCombinations2=[
    [6],
    [9],
    [6,3],
    [3,6]
]

rules = {
    'root': {'inOrder': True},
    'logodiv': {'inOrder': True},
    'header':{'min':1,'max':1},
    'container': {'min': 1, 'max':3},
    'row': {'combinations':True,'0': divCombinations,'1':divCombinations2,'proba':0.9},
    'div-3': {'min': 2, 'max': 4},
    'div-6': {'min': 2, 'max': 4},
    'div-9': {'min': 2, 'max': 4},
    'div-12': {'min': 2, 'max':4},
    'card': {'min': 2, 'max': 3},
    'footer': {'min': 1, 'max': 1},
    'nav':{'min': 1, 'max': 5},
    'flex':{'min':2,'max':4},
}