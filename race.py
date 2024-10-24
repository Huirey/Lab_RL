import numpy as np

class MDP:
    def __init__(self, states, actions, transition_prob, rewards, gamma=0.9):
        self.states = states # 状态空间
        self.actions = actions # 动作空间
        self.transition_prob = transition_prob # 转移模型
        self.rewards = rewards # 回报
        self.gamma = gamma # 回报折扣
        self.value_function = np.zeros(len(states))
        self.policy = np.zeros(len(states), dtype=int)

# 定义状态和动作
states = ['Cool','Warm','Overheated']
actions = ['Slow', 'Fast']

transition_prob = {}
rewards = {}

for state in states:
    transition_prob[state] = {}
    rewards[state] = {}

    for action in actions:
        transition_prob[state][action] = {}
        
        # 初始化所有转移概率和奖励
        for next_state in states:
            transition_prob[state][action][next_state] = 0
            rewards[state][action] = -0.04  # 默认奖励

        x, y = state
        # 这里的可能有问题,终止状态直接终止
        if state == (4, 3):  # 设定+1终止状态
            rewards[state]['up'] = 1
            rewards[state]['right'] = 1
            continue
        elif state == (4, 2):  # 设定-1终止状态
            rewards[state]['down'] = -1
            rewards[state]['left'] = -1
            continue

        # 计算各个动作的实际效果
        if action == 'up':
            intended_state = (x, min(y + 1, 3))
            alt1_state = (max(x - 1, 1), y)
            alt2_state = (min(x + 1, 4), y)
        elif action == 'right':
            intended_state = (min(x + 1, 4), y)
            alt1_state = (x, min(y + 1,3))
            alt2_state = (x, max(y - 1,1))
        elif action == 'down':
            intended_state = (x, max(y - 1,1))
            alt1_state = (max(x - 1, 1), y)
            alt2_state = (min(x + 1, 4), y)
        elif action == 'left':
            intended_state = (max(x - 1, 1), y)
            alt1_state = (x, min(y + 1,3))
            alt2_state = (x, max(y - 1,1))

        # 设置概率
        transition_prob[state][action][intended_state] = 0.8
        transition_prob[state][action][alt1_state] = 0.1
        transition_prob[state][action][alt2_state] = 0.1

gamma = 0.9

mdp = MDP(states, actions, transition_prob, rewards, gamma)
# 根据需要调用策略迭代和值迭代方法
pass