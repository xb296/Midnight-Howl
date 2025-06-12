# import necessary libraries
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from collections import deque
import random

# define a class for the environment
# which is a dataset of spacial vectors
class Environment:
    def __init__(self):
        self.dataset = []

        # generate a dataset of spacial vectors
        # for example, 2D vectors
        for i in range(2):
            # for example, there are 2 clusters of vectors
            # each cluster has 100 vectors
            # the vectors are generated from a normal distribution
            # the mean of the normal distribution is different for each cluster
            # the variance of the normal distribution is the same for each cluster
            # the variance is 1
            
            for j in range(100):
                if i == 0:
                    # vector is a random 2D vector centered at (20, 0)
                    # the distribution is normal with mean (20, 0) and variance 1
                    vector = np.random.normal(loc=[20, 0], scale=1, size=2)
                    self.dataset.append(vector)
                else:
                    # vector is a random 2D vector centered at (-20, 0)
                    # the distribution is normal with mean (-20, 0) and variance 1
                    vector = np.random.normal(loc=[-20, 0], scale=1, size=2)
                    self.dataset.append(vector)

    def draw_data_label(self):
        # return a random index of the dataset
        return np.random.randint(0, 200)

    def get_data_from_label(self, label):
        # return the data at the index
        return self.dataset[label]

    def compute_distance(self, vector1, vector2):
        # return the distance between the two vectors
        return np.linalg.norm(vector1 - vector2)

class SpeakerDQN(nn.Module):
    def __init__(self, input_size=2, hidden_size=64, output_size=216):  # 216 = 6^3 possible words
        super(SpeakerDQN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)

class ListenerDQN(nn.Module):
    def __init__(self, input_size=18, hidden_size=64, output_size=2, device=None):  # input_size=18 (3x6 one-hot encoding)
        super(ListenerDQN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        # Different scale factors for x and y axes
        self.scale = torch.tensor([22.0, 2.0], device=device)  # [x_scale, y_scale]
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        # Apply tanh to get values in [-1, 1] and scale to [-22, 22] for x and [-2, 2] for y
        return torch.tanh(x) * self.scale

class Speaker:
    def __init__(self, learning_rate=0.001, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SpeakerDQN().to(self.device)
        self.target_model = SpeakerDQN().to(self.device)
        self.target_model.load_state_dict(self.model.state_dict())
        
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.memory = deque(maxlen=10000)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        
    def word_to_index(self, word):
        # Convert word to index (e.g., 'abc' -> 0, 'abd' -> 1, etc.)
        letters = 'abcdef'
        index = 0
        for i, char in enumerate(word):
            index += letters.index(char) * (6 ** (2-i))
        return index
    
    def index_to_word(self, index):
        # Convert index to word
        letters = 'abcdef'
        word = ''
        for i in range(3):
            word = letters[index % 6] + word
            index //= 6
        return word
    
    def generate_word(self, vector):
        if random.random() < self.epsilon:
            # Random word generation
            letters = 'abcdef'
            return ''.join(random.choice(letters) for _ in range(3))
        
        with torch.no_grad():
            state = torch.FloatTensor(vector).unsqueeze(0).to(self.device)
            q_values = self.model(state)
            action_idx = q_values.argmax().item()
            return self.index_to_word(action_idx)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        
        batch = random.sample(self.memory, batch_size)
        states = torch.FloatTensor([x[0] for x in batch]).to(self.device)
        actions = torch.LongTensor([self.word_to_index(x[1]) for x in batch]).to(self.device)
        rewards = torch.FloatTensor([x[2] for x in batch]).to(self.device)
        next_states = torch.FloatTensor([x[3] for x in batch]).to(self.device)
        dones = torch.FloatTensor([x[4] for x in batch]).to(self.device)
        
        current_q_values = self.model(states).gather(1, actions.unsqueeze(1))
        next_q_values = self.target_model(next_states).max(1)[0].detach()
        target_q_values = rewards + (1 - dones) * self.gamma * next_q_values
        
        loss = F.mse_loss(current_q_values.squeeze(), target_q_values)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class Listener:
    def __init__(self, learning_rate=0.001, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = ListenerDQN(device=self.device).to(self.device)
        self.target_model = ListenerDQN(device=self.device).to(self.device)
        self.target_model.load_state_dict(self.model.state_dict())
        
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.memory = deque(maxlen=10000)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
    
    def word_to_tensor(self, word):
        # Convert word to tensor (one-hot encoding of each character)
        letters = 'abcdef'
        tensor = torch.zeros(3, 6)
        for i, char in enumerate(word):
            tensor[i][letters.index(char)] = 1
        return tensor.flatten()  # This will give us a 18-dimensional vector (3x6)
    
    def generate_vector(self, word):
        if random.random() < self.epsilon:
            # Random vector generation with different bounds for x and y
            return np.array([
                np.random.uniform(-22, 22),  # x coordinate
                np.random.uniform(-2, 2)     # y coordinate
            ])
        
        with torch.no_grad():
            state = self.word_to_tensor(word).unsqueeze(0).to(self.device)
            return self.model(state).cpu().numpy()[0]
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        
        batch = random.sample(self.memory, batch_size)
        states = torch.stack([self.word_to_tensor(x[0]) for x in batch]).to(self.device)  # Shape: [batch_size, 18]
        actions = torch.FloatTensor([x[1] for x in batch]).to(self.device)  # Shape: [batch_size, 2]
        rewards = torch.FloatTensor([x[2] for x in batch]).to(self.device)  # Shape: [batch_size]
        next_states = torch.stack([self.word_to_tensor(x[3]) for x in batch]).to(self.device)  # Shape: [batch_size, 18]
        dones = torch.FloatTensor([x[4] for x in batch]).to(self.device)  # Shape: [batch_size]
        
        current_q_values = self.model(states)  # Shape: [batch_size, 2]
        next_q_values = self.target_model(next_states).detach()  # Shape: [batch_size, 2]
        target_q_values = rewards.unsqueeze(1) + (1 - dones.unsqueeze(1)) * self.gamma * next_q_values
        
        loss = F.mse_loss(current_q_values, target_q_values)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class ReferentialGame:
    # the game is a game of referential communication
    # the speaker agent generates a word based on the 2D vector
    # the listener agent generates a 2D vector based on the word
    def __init__(self):
        self.speaker = Speaker()
        self.listener = Listener()
        self.environment = Environment()
        self.target_update_frequency = 10  # Update target networks every 10 epochs

    def train(self):
        num_epochs = 1000
        for epoch in range(num_epochs):
            # run 30 interactions in one epoch
            accumulated_reward = 0
            for _ in range(30):
                label = self.environment.draw_data_label()
                vector = self.environment.get_data_from_label(label)
                word = self.speaker.generate_word(vector)
                guess_vector = self.listener.generate_vector(word)
                distance = self.environment.compute_distance(vector, guess_vector)
                reward = -distance
                accumulated_reward += reward
                
                # Store experiences in replay memory
                self.speaker.remember(vector, word, reward, vector, False)
                self.listener.remember(word, guess_vector, reward, word, False)
            
            # Train both networks
            self.speaker.replay()
            self.listener.replay()
            
            # Update target networks periodically
            if epoch % self.target_update_frequency == 0:
                self.speaker.target_model.load_state_dict(self.speaker.model.state_dict())
                self.listener.target_model.load_state_dict(self.listener.model.state_dict())
            
            # Print progress
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Average Reward: {accumulated_reward/30:.2f}")