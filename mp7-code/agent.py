import utils
import random
import math
import collections
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
        self.last_x_dir = self._v_x

        self.games_played = 0
        self.epsilon = .5
        self.alpha = .2
        self.gamma = .9

        self.prev_state = None
        self.prev_action = None
        self.prev_reward = None
        self.N = self.Q.copy()


    def act(self, state, bounces, done, won):
         #TODO - fill out this function
        #  print(state)
        # reward = getReward(state)
        # action = self.learn(self.prev_state, self.prev_action, reward, state)
        # return action
        # print(self.Q.shape)
        if self.prev_state == None:
            self.prev_state = state
            self.prev_action = 1
            self.prev_reward = 0
            return 0
        #print(state)
        if self._train == False:
                self.epsilon = 0
                self.alpha = 0
                self.gamma = 0
        self.qLearningAgent(state, won, done)

        if done:
            self.games_played += 1
            if(self.epsilon > .08):
                self.epsilon *= .9999
            if(self.alpha > .025):
                self.alpha *= .99993
            if self.games_played%1000 == 0:
                print('alpha',self.alpha)
                print('epsilon', self.epsilon)
        #if self._train == False:
        #    self.epsilon = 0

        d_state, x_vel, y_vel, discrete_paddle  = self.getDiscreteState(self.prev_state)

        ball_x = d_state % 12
        ball_y = int(d_state/12)
        #print(ball_x, ball_y, discrete_paddle)
        #print(self.Q[ball_x, ball_y, x_vel, y_vel, discrete_paddle])
        a_list = list(self.Q[ball_x, ball_y, x_vel, y_vel, discrete_paddle])
        #print(a_list.index(max(a_list)))
        return a_list.index(max(a_list)) - 1


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

    def f(self, count, max_q, a_list):
        if random.random() < self.epsilon:
            action = random.choice(self._actions)
            return action
        else:
            if count > 1:
                best = [i for i in range(len(self._actions)) if a_list[i] == max_q]
                i = random.choice(best)
            else:
                i = list(a_list).index(max_q)
        return i


    def qLearningAgent(self, prime_state, won, done):
        prime_reward = self.getReward(prime_state, won, done)
        self.prev_reward = prime_reward
        d_state, x_vel, y_vel, discrete_paddle  = self.getDiscreteState(self.prev_state)
        p_d_state, p_x_vel, p_y_vel, p_discrete_paddle  = self.getDiscreteState(prime_state)

        ball_x = d_state % 12
        ball_y = int(d_state/12)

        p_ball_x = p_d_state % 12
        p_ball_y = int(p_d_state/12)
        if self.prev_state is None:
            action_prime_index = random.choice([0,1,2])
                    #(X_BINS,Y_BINS,V_X,V_Y,PADDLE_LOCATIONS,NUM_ACTIONS)
        # if ball_x == 11:
        #     self.Q[ball_x, ball_y, x_vel, y_vel, discrete_paddle, 0] = prime_reward
        #     self.Q[ball_x, ball_y, x_vel, y_vel, discrete_paddle, 1] = prime_reward
        #     self.Q[ball_x, ball_y, x_vel, y_vel, discrete_paddle, 2] = prime_reward
        #     action_prime_index = 0
        if self.prev_state is not None:
            self.N[ball_x, ball_y, x_vel, y_vel, discrete_paddle, self.prev_action] += 1
            nsa = self.N[ball_x, ball_y, x_vel, y_vel, discrete_paddle, self.prev_action]
            qsa = self.Q[ball_x, ball_y, x_vel, y_vel, discrete_paddle, self.prev_action]

            a_list = self.Q[p_ball_x, p_ball_y, p_x_vel, p_y_vel, p_discrete_paddle]
            max_q = max(a_list)
            count = collections.Counter(a_list)[max_q]
            action_prime_index = self.f(count, max_q, a_list)

            max_qsa_prime = self.Q[p_ball_x, p_ball_y, p_x_vel, p_y_vel, p_discrete_paddle, action_prime_index]
            nsa_prime = self.Q[ball_x, ball_y, x_vel, y_vel, discrete_paddle, action_prime_index]

            qsa += (self.alpha) * ( self.prev_reward + self.gamma * max_qsa_prime - qsa )
            self.Q[ball_x, ball_y, x_vel, y_vel, discrete_paddle, self.prev_action] = qsa
        self.prev_state = prime_state
        self.prev_action = action_prime_index
        self.prev_reward = prime_reward
        #print(self.Q[ball_x, ball_y, x_vel, y_vel, discrete_paddle, self.prev_action])
        return self._actions[self.prev_action]



    def getDiscreteState(self, state):
        #print(state)
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

        discrete_paddle = min(11,math.floor(12 * paddle_y / (1 - paddle_height)))
        if paddle_y == 1 - paddle_height:
            discrete_paddle = 11

        rescaled_x = min(11,math.floor(ball_x*self._x_bins))
        rescaled_y = min(11,math.floor(ball_y*self._y_bins))
        discrete_position = (rescaled_y * self._x_bins) + rescaled_x

        return discrete_position, x_vel, y_vel, discrete_paddle

    def getReward(self, state, won, done):
        discrete_position, t1, t2, discrete_paddle = self.getDiscreteState(state)

        ball_x = discrete_position % 12
        ball_y = int(discrete_position/12)
        if won:
            return 10
        if done and not won:
            return -10
        if ball_x == 11 and (state[1] > state[4] and state[1] < state[4] + .2):
            return 1
        if ball_x == 11:
            return -1

        #to be continue
        return 0
