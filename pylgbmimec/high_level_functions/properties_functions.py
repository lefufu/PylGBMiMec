from basic_functions import Mission


# This file contain high level functions associated to mission level

# ---------------------------------------------
def setObjectKvs(mission:Mission, objID, **parameters ):
    """modify objects key/values of a mission by using multiple keys/values in parameters
            :param objID: int
            Id of object to modify
            :param parameters: dict
            all criterion to search objects, separated by ,
            eg groupList = findObject(newMission, Type='Vehicle', Index=range(11,16), XPos=range(29000,29700), ZPos=range(25000,27000))
            filter criterions
            key=value
                eg: Name='Blue', Xpos=3.23, Type="Plane"
                if string is used fpr any key except Type, it will be used as regex. Eg 'Plane' = ok for every string containing 'Plane',
                    '^Plane$' ok only for string containing strictly Plane
                Type field must be the exact string with exact case
     """
    print()
