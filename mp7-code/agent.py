import utils
import random
import math

class Agent:
    
    def __init__(self, actions,  two_sided = False):
        self._actions = actions
        self._train = True
        self._x_bins = utils.X_BINS
        self._y_bins = utils.Y_BINS
        self._v_x = utils.V_X
        self._v_y = utils.V_Y
        self._paddle_locations = utils.PADDLE_LOCATIONS
        self._num_actions = utils.NUM_ACTIONS
        # Create the Q Table to work with
        self.Q = utils.create_q_table()

        self.epsilon = .1
        self.alpha = .2
        self.gamma = .9

    def act(self, state, bounces, done, won):
         #TODO - fill out this function
        return self._actions[0]

    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    def save_model(self,model_path):
        # At the end of training save the trained model
        utils.save(model_path,self.Q)

    def load_model(self,model_path):
        # Load the trained model for evaluation
        self.Q = utils.load(model_path)
    
# https://studywolf.wordpress.com/2012/11/25/reinforcement-learning-q-learning-and-exploration/
# linked from lecture

    def getQ(self, state, action):
        return self.Q.get((state, action), 0.0)
        # return self.Q.get((state, action), 1.0)
    
    def learnQ(self, state, action, reward, value):
        curr_q = self.Q.get((state, action), None)
        if curr_q is None:
            self.Q[(state, action)] = reward
        else:
            self.Q[(state, action)] = curr_q + self.alpha * (value - curr_q)

    def chooseAction(self, state):
        if random.random() < self.epsilon:
            action = random.choice(self._actions)
        else:
            q = [self.getQ(state, a) for a in self._actions]
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self._actions)) if self.Q[i] == maxQ]
                i = random.choice(best)
            else:
                i = self.Q.index(maxQ)

            action = self._actions[i]
        return action

    def learn(self, prev_state, action, reward, prime_state):
        max_q = max([self.getQ(prime_state, a) for a in self._actions])
        self.learnQ(prev_state, action, reward, reward + self.gamma*max_q)
    
    
    def getDiscreteState(self, state):
        ball_x = state[0]
        ball_y = state[1]
        v_x = state[2]
        v_y = state[3]
        paddle_y = state[4]
        paddle_height = 0.2

        x_vel = -1
        if v_x > 0:
            x_vel = 1

        y_vel = -1
        if abs(v_y) < 0.015:
            y_vel = 0
        elif v_y >= 0.015:
            y_vel = 1
        
        discrete_paddle = math.floor(12 * paddle_y / (1 - paddle_height))
        if paddle_y == 1 - paddle_height:
            discrete_paddle = 11

        rescaled_x = math.ceil(ball_x*self._x_bins)
        rescaled_y = math.ceil(ball_y*self._y_bins)
        discrete_position = (rescaled_y * (self._x_bins-1)) + rescaled_x

        return discrete_position, x_vel, y_vel, discrete_paddle

    def getReward(self, won, bounces, done):
        reward = 0
        if done and won:
            reward = 1
        elif done and not won:
            reward = -1
        #to be continue



