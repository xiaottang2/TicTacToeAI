import random
import operator
import os
import pickle
import time

class Game(object):
  def __init__(self):
    self.board = ['_']*9
    # self._who_plays_first = random.choice([1, 2])
    self._who_plays_first = 1
    theQ = None
    if os.path.isfile('Q1.pickle'):
      with open('Q1.pickle', 'rb') as f:
        theQ = pickle.load(f)
    
    self._playerA = ComputerPlayer("A", Q=theQ if theQ else None)
    # self._playerB = ComputerPlayer("B")
    # self._playerB = HumanPlayer("B")
    self._playerB = DummyPlayer("B")
    self._max_iter = 100
    self._winner = None
    self._count = []

  def _draw(self):
    row = "| {} | {} | {} |"
    hr = "\n--------------\n"
    print (hr+row+hr+row+hr+row+hr).format(*self.board)

  def start(self, quiet=False):
    self.quiet = quiet
    start_t = time.time()
    next_player = self._playerA if self._who_plays_first == 1 else self._playerB
    next_next_player = self._playerB if self._who_plays_first == 1 else self._playerA
    assert next_player != next_next_player
    next_player.char = 'X'
    next_next_player.char = 'O'

    for _ in range(self._max_iter):
      if _%10 ==0:
        print _
      if _%(10000*30) == 0 and _ != 0:
        with open('Q1.pickle', 'wb') as f:
          pickle.dump(self._playerA.Q, f)
      if not self.quiet:
        print '====== New Game ======'

      while not self._end():
        """The one who plays first play first
          Actions:
            Draw()
            Player_first.place_checker()
            Draw()
            Player_second.place_checker()
        """
        if not self.quiet:
          self._draw()
        next_player.place_checker(game)
        tmp = next_player
        next_player = next_next_player
        next_next_player = tmp

      if not self.quiet:
        self._draw()
      self._count.append(self._winner.name)
      self._reset()

    # Print summary
    print "In {} matches, player A wins {} times \n \
          B wins {} times \n \
          A's winning ratio: {}".format(self._max_iter,
                                        self._count.count('A'),
                                        self._count.count('B'),
                                        self._count.count('A')/float(len(self._count)))

    with open('Q1.pickle', 'wb') as f:
      pickle.dump(self._playerA.Q, f)

    end_t = time.time()
    print "Duration: {}".format(end_t-start_t)

  def _reset(self):
    self.board = ['_'] * 9

  def _end(self, msg=True):
    for a, b, c in [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                    [0, 3, 6], [1, 4, 7], [2, 5, 8],
                    [0, 4, 8], [2, 4, 6]]:
      if self.board[a] == self.board[b] == self.board[c] != '_':
        winner_char = self.board[a]
        self._winner = self._playerA if self._playerA.char == winner_char else self._playerB        
        if msg and not self.quiet:
          print "{} wins!".format(str(self._winner))
        return True

    if '_' not in self.board:
      dummy = Player()
      self._winner = dummy
      if msg and not self.quiet:
        print "Draw!"
      return True

    return False

  def act(self, action, char):
    assert self.board[action] == '_', "Error: position already taken"
    self.board[action] = char
    if self._end(msg=False):
      if self._winner.char == char:
        return 1.0 
      else:
        return -1.
    else:
      return 0.


class Player(object):

  def __init__(self):
    self.char = "Draw"
    self.name = "Draw"
    pass

  def __str__(self):
    return self._identity

  def place_checker(self):
    pass


class HumanPlayer(Player):

  def __init__(self, name):
    self._identity = "Human"
    self.char = "U"
    self.name = name

  def place_checker(self, game):
    assert self.char != "U" , "{}'s char hasn't been assigned".format(self._identity)
    
    try:
      position = raw_input("Choose a position to place checker(0-8):")
      position = int(position)
      while game.board[position] != "_":
        position = raw_input("Choose a position to place checker(0-8):")    
        position = int(position)
    except ValueError as e:
      raise ValueError("Position must be integer")
    
    

    game.act(position, self.char)
    game.board[position] = self.char



class ComputerPlayer(Player):

  def __init__(self, name, Q=None):
    self._identity = "Computer" + name if name else "Computer"
    self.char = "U"
    self.name = name
    # Init Q    
    self.Q = Q if Q else {}
    self._states = []
    self._actions = []
    self.gamma = 0.5 # discounting rate
    self.alpha = 0.2 # learning rate
    self.epsilon = 0.2 # exploration ratio

    self._last_action = None

    # Get all states
    for i in range(9):
      


  def place_checker(self, game):
    assert self.char != "U" , "{}'s char hasn't been assigned".format(self._identity)
    board = self._interpret_board(game.board)
    state = State(board)    
    if state not in self.Q:
      # print "state not presented"
      # self.Q[state] = self._make_action_table(state)   # Value table, all 0
      self.Q[state] = 0.
    
    r = random.random()

    nextActions = []
    nextStates = []
    for i in range(9):
      if game.board[i] == '_':
        nextActions.append(i)
        nextStates.append(state.nextState(i))

    actions = sorted(self.Q[state].items(), key=operator.itemgetter(1), reverse=True)
    assert not game._end(), "Error: Game should not end"
    assert len(actions) > 0
    action = actions[0][0] if r > self.epsilon else random.choice([a for a in range(9) if game.board[a] == '_'])

    reward = game.act(action, self.char)

    new_board = self._interpret_board(game.board)
    new_state = State(new_board)
    if new_state not in self.Q:
      # print "state not presented"
      self.Q[new_state] = 0.

    # # Update Q table for the new state
    # try:
    #   max_q_in_new_state = max(self.Q[new_state][a] for a in range(9) if game.board[a] == '_')
    # except ValueError as e:
    #   # Game actually finishes
    #   # Find out if win or lose by checking the reward
    #   max_q_in_new_state = 1.0 if reward > 0 else -1.0

    new_state_q = self.Q[new_state]
    self.Q[state] = (1-self.alpha)*self.Q[state] + self.alpha*(reward + self.gamma*new_state_q)


    
    # Update Q for all previous states
    self._states.append(state)
    self._actions.append(action)
    for i in range(len(self._states) - 1, -1, -1):
      if i < 1:
        break
      aState = self._states[i]
      preState = self._states[i - 1]
      aAction = self._actions[i]
      preAction = self._actions[i - 1]
      # max_q_in_state = max(self.Q[aState][a] for a in range(9) if aState.get()[a] == '_')
      new_state_q = self.Q[aState]
      self.Q[preState] = (1 - self.alpha) * self.Q[preState] + self.alpha * (reward + self.gamma * new_state_q)

    self._last_action = action

  def _interpret_board(self, board):
    """Intepret checkers in the board.

    No matter what the game choose to represent this player,
    alway use X to represent its checkers

      Args:
        board: A list of character indicate the board

      Returns:
        a board, 'X' denotes this player's checker, 'O' denotes the other player's checker
    """
    assert len(board) == 9 and isinstance(board, list)
    result = []
    for i in range(9):
      x = ''
      if board[i] == self.char:
        x = 'X'
      elif board[i] == '_':
        x = '_'
      else:
        x = 'O'
      result.append(x)
    return result


  def _make_action_table(self, state):
    """Make an action table as a dict

    Key represents last action, or current position
    Value represents Q-value

    Args:
      state: current state of (board, action) tuple

    Returns:
      a dictionary with key representing available actions,
      value reprsenting initial Q-value of 0.0
    """
    # board, action = state.get()
    board = state.get()
    result = {}
    for pos, checker in enumerate(board):
      if checker == '_':
        result[pos] = 0.0
    return result

class DummyPlayer(Player):
  def __init__(self, name):
    self._identity = "Dummy"
    self.char = "U"
    self.name = name

  def place_checker(self, game):
    action = random.choice([pos for pos in range(9) if game.board[pos] == '_' ])
    game.board[action] = self.char


class State(object):
  """A simple state object containing just a list(board) and an int(action)"""
  def __init__(self, board):
    self.board = board
    # self.action = action

  def get(self):
    """Return board and action as a tuple"""
    # return (self.board, self.action)
    return self.board

  def __str__(self):
        # return str(self.board) + str(self.action)
        return str(self.board)

  def __hash__(self):      
      return hash(str(self))

  def __eq__(self, other):
    # return self.board == other.board and self.action == other.action
    return self.board == other.board

  def nextState(self, position)
    board = np.copy(self.board)
    board[position] = 'X'
    return State(board)
  
    

if __name__ == '__main__':
  game = Game()
  game.start(quiet=True)

    