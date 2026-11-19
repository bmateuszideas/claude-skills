# Ch 20 — Reinforcement Learning: MDPs, value & policy iteration, Q-learning

Source: `chapter_reinforcement-learning` of d2l-ai/d2l-en (CC BY-SA 4.0). The tabular RL foundation.

## The MDP loop
Agent–environment interaction: at step t, observe **state** $s_t$, take **action** $a_t$, receive **reward** $r_t$, environment transitions to $s_{t+1}$. Formalized as a **Markov decision process**: states $\mathcal{S}$, actions $\mathcal{A}$, transition dynamics $P(s'|s,a)$, reward function $R(s,a)$, discount factor $\gamma \in [0,1]$. **Markov property**: future depends only on the current state, not history. Return $G_t = \sum_{k\ge0} \gamma^k r_{t+k+1}$; goal: maximize expected return $E[G_t]$.

## Policies & value functions
- **Policy** $\pi(a|s)$: the agent's behavior. Deterministic vs stochastic.
- **State-value** $V^\pi(s) = E[G_t | s_t=s]$; **action-value** $Q^\pi(s,a) = E[G_t | s_t=s, a_t=a]$.
- **Bellman equations**: $V^\pi(s) = \sum_a \pi(a|s)\sum_{s',r} P(s',r|s,a)[r + \gamma V^\pi(s')]$ — value = immediate reward + discounted future value. The basis of everything below.

## Dynamic programming (known model)
- **Value iteration**: repeatedly apply Bellman optimality backup $V(s) \leftarrow \max_a \sum_{s',r} P(s',r|s,a)[r+\gamma V(s')]$ until convergence → optimal $V^*$, then greedy policy. Converges in finite steps for finite MDPs (contraction mapping, factor γ).
- **Policy iteration**: evaluate a policy (solve linear Bellman equations) → improve policy greedily → repeat. Converges to $\pi^*$.

## Q-learning (model-free, off-policy)
Update: $Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$. Learns $Q^*$ directly without knowing $P$. Exploration: **ε-greedy** (act greedily w.p. 1−ε, random w.p. ε). **Deep Q-Networks (DQN, 2015)**: replace the Q-table with a neural net + experience replay + target network — the Atari breakthrough.

## 2026 delta
- Tabular methods are for small state spaces; real RL uses function approximation (DQN, policy gradients like PPO/A3C, actor-critic) — PPO is the current default for continuous control (robotics, games).
- RLHF (ch. 14 context) is the big modern application: a reward model + PPO fine-tunes LLMs to human preferences.
- Simulators (MuJoCo, Isaac Gym) + domain randomization are how most RL training happens before real-world deployment.

## Gotchas
- Discount γ close to 1 → long horizons but slow convergence; γ=0 → myopic.
- ε-greedy decay schedule matters; too little exploration = stuck in suboptimal policy.
- Reward shaping can cause reward hacking — design rewards carefully (the alignment problem).
