# Generate a random string with maxium length L
import random

def generate_string(L):
    length = random.randint(1, L)
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))

SIZE = 40
semantic_space = range(SIZE)

# compute the encoding energy of a string
def compute_encoding_energy(string):
    return len(string)

# this is a measure of energy by 1-dimensional distance
def compute_decoding_energy(target, recovered_target):
    return abs(target - recovered_target)
    
L = 5

speaker_memory = {}

for i in semantic_space:
    speaker_memory[i] = generate_string(L)

listener_memory = {}

for i in semantic_space:
    listener_memory[generate_string(L)] = i

# print(speaker_memory)

# print(listener_memory)

established_connection = {}

iteration_idx = 0
while iteration_idx < 1:
    # Monte Carlo

    # Compute energy of the system
    energy = 0
    # Since the system is not very large, the energy is accurate
    for i in semantic_space:
        # i is the target
        # generate the string using speaker_memory
        s = speaker_memory[i]

        # genreate the recovered target using listener_memory
        if s in listener_memory:
            recovered_target = listener_memory[s]
            established_connection[s] = recovered_target
        else:
            # a large enough number to simulate infinity
            recovered_target = 100

        # compute the energy
        energy += compute_encoding_energy(s) + compute_decoding_energy(i, recovered_target)

    print(f"iteration {iteration_idx}: {energy}")


    # Update the system

    # randomly select a target
    target = random.choice(semantic_space)

    # if the target is in the established connection, optimise the listener
    if target in established_connection:
        # choose another target
        target = random.choice(semantic_space)
        while target in established_connection:
            target = random.choice(semantic_space)
    else:
        # choose a target
        target = random.choice(semantic_space)

    # if the target is not in the established connection
    # choose another 
    # Check if the system is in equilibrium

    # If the system is in equilibrium, break the loop

    # If the system is not in equilibrium, continue the loop

    iteration_idx += 1