import utils
import random

class Agent:
    
    def __init__(self, actions):
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

# https://github.com/studywolf/blog/blob/master/RL/Cat%20vs%20Mouse%20exploration/qlearn.py

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




    def getQ(self, state, action):
        return self.Q.get((state, action), 0.0)
        # return self.Q.get((state, action), 1.0)
    
    def learnQ(self, state, action, reward, value):
        oldv = self.Q.get((state, action), None)
        if oldv is None:
            self.Q[(state, action)] = reward
        else:
            self.Q[(state, action)] = oldv + self.alpha * (value - oldv)

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

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.getQ(state2, a) for a in self._actions])
        self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)
