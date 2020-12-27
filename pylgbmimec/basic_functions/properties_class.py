from .error_handling import *


class Properties:
    """ contains object properties
    supported type for propertie :  unitary (int, float, str), array (set ={v1,v2..}, Dictionnary (dictionnary {name1:val1, name2:val2,...}), list [obj1, obj2,..], W=windLayer, C = Country
    Value : object
    depend of type
    """

# ---------------------------------------------
    def __init__(self, value: object) -> object:
        """ create basic propertie
        """
        self.Value = value

    # ---------------------------------------------
    def copy(self) -> object:
        """ copy property into a new one
        """
        newProp=Properties()
        if type(self) == int or type(self) == float or type(self) == str:
            newProp=self.Value
        if type(self) == list:
            newProp=self.Value.copy()
        if type(self) == set:
            newProp=self.Value.copy()
        if type(self) == dict:
            newProp=self.Value.copy()
        return newProp

# ---------------------------------------------
    def __str__(self):
            typeProp=type(self.Value)
            if typeProp == float or typeProp == int or typeProp == str:
                convert2str = "Unitary properties:{0}".format(typeProp)
                convert2str +="\n  Value:{0}".format(self.Value)
            elif typeProp == dict:
                convert2str = "Dictionnary properties:{0}".format(typeProp)
                for lvalue in self.Value:
                    convert2str += "\n  {0} : {1}".format(lvalue,self.Value[lvalue])
            elif typeProp == list:
                convert2str = "List properties:".format(typeProp)
                for lvalue in self.Value:
                    convert2str += "\n  {0}".format(lvalue)
            elif typeProp == set:
                convert2str = "Array properties:{0}".format(typeProp)
                for lvalue in self.Value:
                    convert2str += "\n  {0}".format(lvalue)
            return convert2str
