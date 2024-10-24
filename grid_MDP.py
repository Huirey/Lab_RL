import numpy as np
import random
class MDP:
    def __init__(self, states, actions, transition_prob, rewards, gamma=0.9):
        self.states = states # 状态空间
        self.actions = actions # 动作空间
        self.transition_prob = transition_prob # 转移模型
        self.rewards = rewards # 回报
        self.gamma = gamma # 回报折扣
        self.value_function = np.zeros(len(states))
        self.policy = np.zeros(len(states), dtype=int)

    def value_iteration(self, epsilon=0.01):
        # Placeholder for value iteration implementation
        pass

    def policy_iteration(self):
        # Placeholder for policy iteration implementation
        pass

    def evaluate_policy(self):
        # Placeholder for policy evaluation implementation
        pass

    def improve_policy(self):
        # Placeholder for policy improvement implementation
        pass

# 定义状态和动作
states = [(i, j) for i in range(1,5) for j in range(1,4)]
actions = ['up', 'right', 'down', 'left']

transition_prob = {}
rewards = {}

for state in states:

    transition_prob[state] = {}
    rewards[state] = -0.04  # 默认奖励
    if state == (4, 3):  # 设定+1终止状态
        rewards[state] = 1
    elif state == (4, 2):  # 设定-1终止状态
        rewards[state] = -1

    for action in actions:
        transition_prob[state][action] = {}
        
        # 初始化所有转移概率
        for next_state in states:
            transition_prob[state][action][next_state] = 0

        x, y = state
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

# 价值迭代
def Value_Iteration(S,A,P,R,gamma,epsilon):
    # 局部变量初始化
    U = {s:0 for s in S} # 上一次迭代效应值
    U_ = {s:0 for s in S} # 本次迭代效应值
    U_[(4,2)] = -1 # ==不迭代终止状态==
    U_[(4,3)] = 1
    delta = np.inf # 每两次迭代之间效应值最大的变化幅度
    # 循环
    while(delta >= epsilon*(1 - gamma) / gamma):
        U = U_.copy();delta = 0
        for s in S:
            if s==(4,2) or s==(4,3): # ==不迭代终止状态==
                continue
            U_[s] = R[s] + gamma * (max([  sum([  P[s][a][s_] * U[s_] for s_ in S]) for a in A]))
            if np.abs(U_[s] - U[s]) > delta:
                delta = np.abs(U_[s] - U[s])

    return U


# 策略提取
def Policy_Extraction(S,A,P,U):
    PI = {s:None for s in S}
    for s in S :
        if s==(4,2) or s==(4,3): # ==不迭代终止状态==
            continue
        PI[s] = A[np.argmax([  sum([ P[s][a][s_]*U[s_] for s_ in S])  for a in A])]
    return PI


# 策略评估
def Policy_Evaluation(PI,U,S,P,R,gamma,k=10):
    # 目的是估计出在固定策略的状况下，每个状态的效应值
    # 拥有了固定的策略，那么我们就可以精确的计算出每一个状态的效应值，如果是这样，那么就不需要初始的U
    # 也可以执行简化的价值迭代来估计每个状态的效应值（被选择），那么就需要初始的U,
    U_ = U.copy()
    for _ in range(k):
        U = U_.copy()
        for s in S:
            if s==(4,2) or s==(4,3): # ==不迭代终止状态==
                continue
            U_[s] = R[s] + gamma * sum([  P[s][PI[s]][s_] * U[s_] for s_ in S])
    return U_


# 策略迭代
def Policy_Iteration(S,A,P,R,gamma):
    # 局部变量初始化
    U = {s:0 for s in S} # 本次迭代效应值
    U[(4,2)] = -1
    U[(4,3)] = 1
    PI = {s:A[random.randint(0, 3)] for s in S}
    PI[(4,2)] = None
    PI[(4,3)] = None
    unchanged = False
    while(unchanged!=True):
        U = Policy_Evaluation(PI,U,S,P,R,gamma)
        unchanged = True
        for s in S:
            if s==(4,2) or s==(4,3): # ==不迭代终止状态==
                continue
            if R[s] + gamma * (max([  sum([  P[s][a][s_] * U[s_] for s_ in S]) for a in A])) > R[s] + gamma * sum([  P[s][PI[s]][s_] * U[s_] for s_ in S]):
                PI[s] = A[np.argmax([  sum([  P[s][a][s_] * U[s_] for s_ in S]) for a in A])]
                unchanged = False
    # print(U)
    return PI

U = Value_Iteration(states,actions,transition_prob,rewards,0.99,0.000001)
PI = Policy_Extraction(states,actions,transition_prob,U)
# print(U)
print(PI)

PI = Policy_Iteration(states,actions,transition_prob,rewards,0.99)
print(PI)