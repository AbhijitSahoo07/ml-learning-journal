# Reinforcement Learning (Classical)

## Overview
Reinforcement Learning (RL) is a paradigm of machine learning where an "agent" learns to make decisions by interacting with an "environment." Unlike supervised learning, which relies on labeled data, or unsupervised learning, which finds patterns in unlabeled data, RL agents learn through trial and error, receiving "rewards" or "penalties" for their actions. The goal of the agent is to discover a "policy"—a strategy that maps states to actions—that maximizes the total cumulative reward over the long run. "Classical" RL typically refers to methods that operate on discrete, often smaller, state and action spaces, frequently using tabular methods (like Q-tables) or dynamic programming, without relying on function approximators like neural networks.

## What Problem It Solves
Classical Reinforcement Learning addresses problems involving sequential decision-making in uncertain environments. It's particularly powerful when:
*   **Explicit programming is difficult or impossible:** When the optimal behavior is too complex to hard-code, or the environment dynamics are unknown.
*   **Learning from interaction is feasible:** The agent can explore and receive feedback from its environment.
*   **Long-term consequences matter:** Actions have delayed effects, and the agent needs to optimize for future rewards, not just immediate ones.
*   **No labeled data is available:** The learning process is driven by rewards, not pre-classified examples.

Examples include teaching an agent to play a game, control a robot, or manage resources where the best sequence of actions is not obvious beforehand.

## How It Works
The core of classical Reinforcement Learning revolves around an agent-environment interaction loop:

1.  **Observation (State $S_t$):** At a given time $t$, the agent observes the current state of the environment.
2.  **Action (Action $A_t$):** Based on its current policy (its learned strategy) and the observed state, the agent chooses an action to perform.
3.  **Interaction:** The agent executes the action in the environment.
4.  **New State (State $S_{t+1}$):** The environment transitions to a new state as a result of the agent's action.
5.  **Reward (Reward $R_{t+1}$):** The environment provides a numerical reward signal, indicating how good or bad the previous action was in the context of the new state.
6.  **Learning:** The agent uses the observed reward and the transition to the new state to update its policy or value function, aiming to improve its future decision-making.

This loop continues until a terminal state is reached or for a predefined number of steps. The agent's ultimate goal is to learn an optimal policy ($\pi^*$) that dictates the best action to take in any given state to maximize the expected sum of future rewards. Key components include:
*   **Policy ($\pi$):** A function that maps states to actions.
*   **Value Function ($V^\pi(s)$ or $Q^\pi(s,a)$):** A prediction of the expected future reward from a given state or state-action pair, following a particular policy.
*   **Model (optional):** An understanding of the environment's dynamics (how states transition and rewards are generated). Model-based RL uses this, while model-free RL learns directly from experience.

## Mathematical Intuition
Classical Reinforcement Learning is formally grounded in the framework of **Markov Decision Processes (MDPs)**. An MDP is defined by a tuple $(\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma)$:

*   $\mathcal{S}$: A finite set of states.
*   $\mathcal{A}$: A finite set of actions.
*   $\mathcal{P}(s' | s, a)$: The state transition probability function, which gives the probability of transitioning to state $s'$ from state $s$ after taking action $a$.
*   $\mathcal{R}(s, a, s')$: The reward function, which gives the expected immediate reward received after transitioning from state $s$ to state $s'$ via action $a$.
*   $\gamma \in [0, 1]$: The discount factor, which determines the present value of future rewards. A higher $\gamma$ makes the agent care more about long-term rewards.

The core idea is to find a policy $\pi(a|s)$ (probability of taking action $a$ in state $s$) that maximizes the expected discounted cumulative reward, also known as the **return**.

The **Value Function** $V^\pi(s)$ for a policy $\pi$ represents the expected return starting from state $s$ and following policy $\pi$:
$$V^\pi(s) = E_\pi \left[ \sum_{k=0}^\infty \gamma^k R_{t+k+1} \mid S_t = s \right]$$

The **Action-Value Function** (or Q-function) $Q^\pi(s,a)$ represents the expected return starting from state $s$, taking action $a$, and then following policy $\pi$:
$$Q^\pi(s,a) = E_\pi \left[ \sum_{k=0}^\infty \gamma^k R_{t+k+1} \mid S_t = s, A_t = a \right]$$

The **Bellman Equations** are fundamental to solving MDPs. They express a relationship between the value of a state and the values of its successor states. For the optimal value function $V^*(s)$ and optimal action-value function $Q^*(s,a)$:

**Bellman Optimality Equation for $V^*(s)$:**
$$V^*(s) = \max_a \sum_{s',r} P(s',r|s,a) [r + \gamma V^*(s')]$$
This states that the optimal value of a state is the maximum over all possible actions of the expected immediate reward plus the discounted optimal value of the next state.

**Bellman Optimality Equation for $Q^*(s,a)$:**
$$Q^*(s,a) = \sum_{s',r} P(s',r|s,a) [r + \gamma \max_{a'} Q^*(s',a')]$$
This states that the optimal Q-value for a state-action pair is the expected immediate reward plus the discounted maximum optimal Q-value of the next state.

Algorithms like Value Iteration and Policy Iteration (model-based) or Q-learning and SARSA (model-free) iteratively solve these equations to find the optimal policy.

## Advantages
*   **Learns optimal policies:** Can discover the best possible sequence of actions to maximize long-term rewards.
*   **No prior knowledge of environment needed (model-free):** Can learn directly from interaction without an explicit model of the environment's dynamics.
*   **Handles sequential decision-making:** Naturally suited for problems where current actions affect future outcomes.
*   **Adapts to change:** Can continuously learn and adapt its policy if the environment dynamics change over time.
*   **No labeled data required:** Learns solely from reward signals, making it suitable for problems where data labeling is impractical.

## Disadvantages
*   **Sample inefficiency:** Often requires a very large number of interactions with the environment to learn an effective policy, which can be time-consuming or costly in real-world scenarios.
*   **Curse of dimensionality:** Classical tabular methods struggle significantly with large state and action spaces, as the Q-table or value function table grows exponentially.
*   **Exploration-exploitation dilemma:** The agent must balance exploring new actions (to find potentially better strategies) with exploiting known good actions (to maximize current rewards). Finding the right balance is crucial and often difficult.
*   **Reward shaping challenge:** Designing an effective reward function that guides the agent towards the desired behavior without unintended side effects can be very difficult and requires domain expertise.
*   **Convergence guarantees:** While many classical algorithms have theoretical convergence guarantees, practical implementation can be sensitive to hyperparameters and lead to slow convergence or instability.

## Real World Applications
1.  **Game Playing (e.g., Chess, Checkers, Backgammon):** Early successes of classical RL involved agents learning to play board games against human opponents. For instance, TD-Gammon, an early neural network-based RL program, learned to play backgammon at a world-class level by playing against itself.
2.  **Elevator Scheduling:** Optimizing elevator movement in a building to minimize waiting times and energy consumption. An RL agent can learn policies for dispatching elevators based on passenger requests and current elevator locations.
3.  **Traffic Light Control:** Managing traffic flow at intersections to reduce congestion and travel times. RL agents can learn to adjust traffic light timings dynamically based on real-time traffic conditions, treating each intersection as an environment.

## Python Example
This example demonstrates Q-learning in a simple 4x4 grid world. The agent needs to navigate from a start 'S' to a goal 'G', avoiding a 'Hole' 'H'.

```python
import numpy as np

# Define the grid world
# S: Start, F: Frozen (safe), H: Hole (bad), G: Goal (good)
# The environment is a 4x4 grid
# 0 1 2 3
# 4 5 6 7
# 8 9 10 11
# 12 13 14 15
grid = [
    "SFFF",
    "FHFH",
    "FFFH",
    "HFFG"
]

# Map grid characters to states
state_map = {
    'S': 0, 'F': 1, 'H': 2, 'G': 3
}
# Convert grid to a list of characters for easier indexing
flat_grid = [char for row in grid for char in row]

# Number of states (16 for 4x4 grid)
num_states = len(flat_grid)
# Number of actions (Up, Down, Left, Right)
num_actions = 4 # 0: Up, 1: Down, 2: Left, 3: Right

# Initialize Q-table with zeros
q_table = np.zeros((num_states, num_actions))

# Hyperparameters
learning_rate = 0.1  # Alpha
discount_factor = 0.99 # Gamma
epsilon = 0.1        # Epsilon for epsilon-greedy policy
num_episodes = 2000

# Define rewards for each state
rewards = np.full(num_states, -0.1) # Small penalty for each step
for i, char in enumerate(flat_grid):
    if char == 'H':
        rewards[i] = -10 # Big penalty for falling in a hole
    elif char == 'G':
        rewards[i] = 10 # Big reward for reaching the goal

# Define terminal states
terminal_states = [i for i, char in enumerate(flat_grid) if char in ['H', 'G']]

# Function to get next state and reward
def get_next_state(current_state, action):
    row, col = divmod(current_state, 4) # Convert 1D state to 2D (row, col)
    
    if action == 0: # Up
        row = max(0, row - 1)
    elif action == 1: # Down
        row = min(3, row + 1)
    elif action == 2: # Left
        col = max(0, col - 1)
    elif action == 3: # Right
        col = min(3, col + 1)
        
    next_state = row * 4 + col
    return next_state, rewards[next_state]

# Q-learning algorithm
for episode in range(num_episodes):
    current_state = 0 # Start state (S)
    
    while current_state not in terminal_states:
        # Epsilon-greedy action selection
        if np.random.uniform(0, 1) < epsilon:
            action = np.random.randint(num_actions) # Explore
        else:
            action = np.argmax(q_table[current_state, :]) # Exploit
            
        next_state, reward = get_next_state(current_state, action)
        
        # Q-learning update rule
        # Q(s,a) = Q(s,a) + alpha * [R + gamma * max_a' Q(s',a') - Q(s,a)]
        old_q_value = q_table[current_state, action]
        
        if next_state in terminal_states:
            # If next_state is terminal, there are no future actions, so max_a' Q(s',a') is 0
            max_future_q = 0
        else:
            max_future_q = np.max(q_table[next_state, :])
            
        new_q_value = old_q_value + learning_rate * (reward + discount_factor * max_future_q - old_q_value)
        q_table[current_state, action] = new_q_value
        
        current_state = next_state

print("Q-table after training:")
print(q_table)

# Test the learned policy
print("\nTesting the learned policy:")
current_state = 0
path = [current_state]
while current_state not in terminal_states:
    action = np.argmax(q_table[current_state, :])
    current_state, _ = get_next_state(current_state, action)
    path.append(current_state)
    if len(path) > 20: # Prevent infinite loops in case of bad policy
        print("Path too long, likely stuck or bad policy.")
        break

print("Path taken:", path)
print("Goal reached!" if path[-1] == 15 else "Failed to reach goal.")
```

## Interview Questions
1.  **What is the agent-environment loop in Reinforcement Learning?**
    *   **Answer:** The agent-environment loop describes the continuous interaction between an RL agent and its environment. At each time step, the agent observes the current state of the environment, selects an action based on its policy, and executes it. The environment then transitions to a new state and provides a reward signal to the agent. This new state and reward are used by the agent to update its policy, and the loop repeats. This iterative process allows the agent to learn and refine its behavior over time.

2.  **Explain the exploration-exploitation dilemma. How is it typically addressed in classical RL?**
    *   **Answer:** The exploration-exploitation dilemma is a fundamental challenge in RL. **Exploration** refers to trying new actions or visiting new states to discover potentially better strategies or more rewarding paths. **Exploitation** refers to choosing actions that are known to yield the highest rewards based on current knowledge. The dilemma arises because an agent cannot do both simultaneously; too much exploration might lead to suboptimal performance, while too much exploitation might prevent the agent from discovering truly optimal strategies. In classical RL, this is often addressed using **epsilon-greedy policies**. With probability $\epsilon$ (a small value), the agent chooses a random action (exploration), and with probability $1-\epsilon$, it chooses the action with the highest estimated Q-value (exploitation). $\epsilon$ is often decayed over time, starting with more exploration and gradually shifting towards more exploitation as the agent learns.

3.  **What is a Markov Decision Process (MDP) and why is it fundamental to classical RL?**
    *   **Answer:** A Markov Decision Process (MDP) is a mathematical framework used to model sequential decision-making problems where outcomes are partly random and partly under the control of a decision-maker. It's defined by states, actions, transition probabilities, and rewards. It's fundamental to classical RL because it provides the formal mathematical foundation for almost all RL problems. The "Markov" property implies that the future state depends only on the current state and action, not on the entire history of states and actions. This simplification allows for the development of algorithms (like Value Iteration, Policy Iteration, Q-learning) that can efficiently compute optimal policies by focusing only on the immediate state transitions and rewards.

## Quiz
1.  What is the primary goal of a Reinforcement Learning agent?
    a) To maximize immediate reward.
    b) To minimize the number of actions taken.
    c) To maximize the total cumulative reward over the long term.
    d) To find the shortest path to a goal.

    **Answer:** c) To maximize the total cumulative reward over the long term.

2.  Which of the following is NOT a core component of a Markov Decision Process (MDP)?
    a) States ($\mathcal{S}$)
    b) Actions ($\mathcal{A}$)
    c) Policy ($\pi$)
    d) Transition Probabilities ($\mathcal{P}$)
    e) Reward Function ($\mathcal{R}$)

    **Answer:** c) Policy ($\pi$) - While a policy is what an RL agent learns *within* an MDP, it is not a defining component of the MDP itself. The MDP defines the environment; the policy defines the agent's behavior in that environment.

## Further Reading
1.  **"Reinforcement Learning: An Introduction" by Richard S. Sutton and Andrew G. Barto (2nd Edition):** Often referred to as the "bible" of RL, this book provides a comprehensive and accessible introduction to the field, covering classical methods in detail. [Link to online version](http://incompleteideas.net/book/the-book-2nd.html)
2.  **OpenAI Spinning Up in Deep RL:** While it focuses on Deep RL, its introductory sections provide excellent foundational knowledge on core RL concepts, including MDPs and classical algorithms. [Link](https://spinningup.openai.com/en/latest/index.html)
3.  **David Silver's Reinforcement Learning Course (UCL):** A highly regarded lecture series that covers the mathematical foundations and algorithms of RL, starting with classical methods. [Link to YouTube playlist](https://www.youtube.com/playlist?list=PLqM7alScZfJ_Weyb_N-L4J_13e1t_1-z-)