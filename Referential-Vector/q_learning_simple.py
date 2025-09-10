import numpy as np
import random
from collections import defaultdict
import itertools

# --- Simulation Parameters ---
# Vocabulary and target space
VOCABULARY = ['a', 'b', 'c', 'd']
TARGETS = [0, 1, 2, 3]

# Q-Learning parameters
ALPHA = 0.05  # Learning rate
# Epsilon-greedy strategy for exploration
# Start with a high chance of exploration, then decay it.
INITIAL_EPSILON = 1.0
EPSILON_DECAY = 0.99995
MIN_EPSILON = 0.05

# Simulation length
EPISODES = 50000

# --- Agent Q-Tables ---
# We use defaultdicts to handle new states gracefully.
# Speaker's Q-table: Q_S(t, m) -> maps a (target, message) pair to a value.
q_speaker = defaultdict(float)

# Listener's Q-table: Q_L({m, t, t'}, w) -> maps a (state, action) pair to a value.
# The state is a tuple (message, choice1, choice2).
# The action is the chosen item (choice1 or choice2).
q_listener = defaultdict(lambda: defaultdict(float))


def choose_action(q_table_slice, possible_actions, epsilon):
    """
    Selects an action using an epsilon-greedy policy.

    Args:
        q_table_slice (dict): A dictionary of {action: q_value} for the current state.
        possible_actions (list): A list of actions available in the current state.
        epsilon (float): The current exploration rate.

    Returns:
        The chosen action.
    """
    if random.random() < epsilon:
        # Explore: choose a random action
        return random.choice(possible_actions)
    else:
        # Exploit: choose the best known action
        # Find the maximum Q-value in the slice
        max_q = -np.inf
        for action in possible_actions:
            if q_table_slice[action] > max_q:
                max_q = q_table_slice[action]

        # Get all actions that have the maximum Q-value
        best_actions = [
            action for action in possible_actions if q_table_slice[action] == max_q
        ]
        # Break ties randomly
        return random.choice(best_actions)

def run_simulation():
    """
    Runs the main simulation loop for the specified number of episodes.
    """
    print("--- Starting Simulation ---")
    epsilon = INITIAL_EPSILON
    success_count = 0
    success_history = []

    for episode in range(EPISODES):
        # 1. SETUP THE EPISODE
        # The environment provides a target and a distractor
        target = random.choice(TARGETS)
        distractor = random.choice([t for t in TARGETS if t != target])

        # The listener is presented with two choices. The order is randomized
        # to prevent the listener from learning a positional bias.
        choices = [target, distractor]
        random.shuffle(choices)
        choice1, choice2 = choices[0], choices[1]

        # 2. SPEAKER'S TURN
        speaker_state = target
        speaker_action = choose_action(
            {msg: q_speaker[(speaker_state, msg)] for msg in VOCABULARY},
            VOCABULARY,
            epsilon
        )
        message = speaker_action

        # 3. LISTENER'S TURN
        listener_state = (message, choice1, choice2)
        listener_possible_actions = [choice1, choice2]
        listener_action = choose_action(
            q_listener[listener_state],
            listener_possible_actions,
            epsilon
        )
        listener_choice = listener_action

        # 4. REWARD AND LEARNING
        # Reward is 1 for success, 0 for failure.
        reward = 1 if listener_choice == target else 0
        if reward == 1:
            success_count += 1

        # Update Speaker's Q-table
        # The update rule is simplified because there is no "next state" (gamma=0).
        old_q_s = q_speaker[(speaker_state, message)]
        q_speaker[(speaker_state, message)] = old_q_s + ALPHA * (reward - old_q_s)

        # Update Listener's Q-table
        old_q_l = q_listener[listener_state][listener_choice]
        q_listener[listener_state][listener_choice] = old_q_l + ALPHA * (reward - old_q_l)

        # 5. DECAY EPSILON
        epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)

        # Log progress
        if (episode + 1) % 5000 == 0:
            success_rate = (success_count / 5000) * 100
            success_history.append(success_rate)
            print(f"Episode {episode + 1}/{EPISODES} | "
                  f"Success Rate (last 5k): {success_rate:.2f}% | "
                  f"Epsilon: {epsilon:.4f}")
            success_count = 0

    return success_history


def print_listener_q_table():
    """
    Prints the entire Q-table for the Listener agent in a readable format.
    """
    print("\n--- Listener's Full Q-Table ---")
    print(f"{'State (Msg, C1, C2)':<25} | {'Q(Action=C1)':<15} | {'Q(Action=C2)':<15}")
    print("-" * 60)

    # Generate all possible states for the listener
    # This includes all messages and all ordered pairs of distinct targets.
    all_target_pairs = list(itertools.permutations(TARGETS, 2))

    # Sort everything for a consistent, readable output
    sorted_vocab = sorted(VOCABULARY)
    sorted_pairs = sorted(all_target_pairs)

    for m in sorted_vocab:
        for t1, t2 in sorted_pairs:
            state = (m, t1, t2)
            # Get the Q-values for the two possible actions in this state
            q_val1 = q_listener[state][t1]
            q_val2 = q_listener[state][t2]
            
            state_str = f"('{state[0]}', {state[1]}, {state[2]})"
            
            # Highlight the better choice to make the policy easier to see
            if q_val1 > q_val2:
                q_str1 = f"*{q_val1:.4f}*"
                q_str2 = f" {q_val2:.4f} "
            elif q_val2 > q_val1:
                q_str1 = f" {q_val1:.4f} "
                q_str2 = f"*{q_val2:.4f}*"
            else: # Equal values
                q_str1 = f" {q_val1:.4f} "
                q_str2 = f" {q_val2:.4f} "

            print(f"{state_str:<25} | {q_str1:<15} | {q_str2:<15}")


def analyze_results():
    """
    Analyzes and prints the learned policies and the emergent language.
    """
    print("\n--- Simulation Finished: Analyzing Results ---")

    # 1. Determine the Speaker's learned policy
    speaker_policy = {}
    for t in TARGETS:
        # For each target, find the message with the highest Q-value
        # for the given target t, which message m in VOCABULARY has the highest Q-value?
        best_msg = max(VOCABULARY, key=lambda m: q_speaker[(t, m)])
        speaker_policy[t] = best_msg

    print("\n[Speaker's Learned Policy]")
    print("Target -> Chosen Message")
    for target, msg in sorted(speaker_policy.items()):
        print(f"  {target}    ->    '{msg}'")

    # 2. Determine the Listener's learned policy
    listener_policy = {}

    for t in TARGETS:
        # for each target t, let Speaker generate a message
        # this prevents the listener take a wrong message with a given target, which makes the listener confused
        msg = speaker_policy[t]
        distractor = random.choice([d for d in TARGETS if d != t])
        state = (msg, t, distractor)
        best_choice = max([t, distractor], key=lambda choice: q_listener[state][choice])
        listener_policy[msg] = best_choice

    # for m in VOCABULARY:
    #     # To test the listener, we see what it does for each message
    #     # when presented with all possible targets.
    #     predictions = []
    #     for t in TARGETS:
    #         # Create a dummy state with a random distractor
    #         distractor = random.choice([d for d in TARGETS if d != t])
    #         state = (m, t, distractor)
    #         # Choose the best action (no exploration)
    #         best_choice = max([t, distractor], key=lambda choice: q_listener[state][choice])
    #         # print(f"message: {m}, target: {t}, best choice: {best_choice}")
    #         predictions.append(best_choice)
    #     # The listener's "meaning" for a message is the target it most often chooses.
    #     listener_policy[m] = max(set(predictions), key=predictions.count)

    print("\n[Listener's Learned Policy]")
    print("Message -> Interpreted Target")
    for msg, target in sorted(listener_policy.items()):
        print(f"  '{msg}'    ->    {target}")

    # 3. Display the emergent protocol
    print("\n[Emergent Language Protocol]")
    print("Target <--> Message")
    successful_mappings = 0
    for target, msg in sorted(speaker_policy.items()):
        if listener_policy.get(msg) == target:
            status = "✅ (Success)"
            successful_mappings += 1
        else:
            status = "❌ (Failure)"
        print(f"   {target}   <-->   '{msg}'   {status}")

    final_success_rate = (successful_mappings / len(TARGETS)) * 100
    print(f"\nFinal Communication Success Rate: {final_success_rate:.2f}%")


# --- Run the script ---
if __name__ == "__main__":
    run_simulation()
    analyze_results()
    # print_listener_q_table()