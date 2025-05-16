# import torch
# import torch.nn as nn

# policy of the teacher
# read in a vector, then generate a string
class TeacherPolicy:
    def __init__(self):
        # create a policy model?
        self.policy = [[None] * 32] * 32

    def get_action(self, vector):
        # ? what should this be?
        # according to the observed vector (coordinate, in current settings)
        # generate a string
        


# policy of the student
# read a string, then predict its coordination
class StudentPolicy:
    def __init__(self):
        pass
