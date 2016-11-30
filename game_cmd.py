import numpy as np
import pickle

NUM_ROWS = 3
NUM_COLS = 3

CHECKER_EMPTY = '_'
CHECKER_P1 = 'X'                # X represents the player who plays first
CHECKER_P2 = 'O'

class State(object):
    def __init__(self):
        self.board = [[CHECKER_EMPTY for i in range(NUM_ROWS)] for j in range(NUM_COLS)]
        self.winner = None
        self.end = None
        self.hash = None
    def getHash(self):
        # Calculate a unique hash of self.board
        if not self.hash:
            hashSource = ''
            for i in range(NUM_ROWS):
                for j in range(NUM_COLS):
                    hashSource += self.board[i][j]
            self.hash = hash(hashSource)

            # Verify
            if hashSource == CHECKER_EMPTY*9:
                assert self.hash == -3319119174650460690


        return self.hash

    def ifEnd(self):
        if self.end is not None:
            return self.end

        self.end = False

        for a, b, c in [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                    [0, 3, 6], [1, 4, 7], [2, 5, 8],
                    [0, 4, 8], [2, 4, 6]]:
            ai = a / 3; aj = a % 3
            bi = b / 3; bj = b % 3
            ci = c / 3; cj = c % 3

            if self.board[ai][aj] == self.board[bi][bj] == self.board[ci][cj] != CHECKER_EMPTY:
                self.end = True
                self.winner = CHECKER_P1 if self.board[ai][aj] == CHECKER_P1 else CHECKER_P2
        
        # Draw
        if CHECKER_EMPTY not in self.board:
            self.end = True
            self.winner = None

        return self.end

    def nextState(self, i, j, checker):
        # Set checker in row i column j
        newState = State()
        newState.board = np.copy(self.board)
        newState.board[i][j] = checker
        return newState

    def draw(self):
        row = "| {} | {} | {} |"
        hr = "\n--------------\n"
        print (hr+row+hr+row+hr+row+hr).format(*np.reshape(self.board, -1))

def toggleChecker(checker):
    if checker == CHECKER_P1:
        return CHECKER_P2
    return CHECKER_P1

def getAllStatesRecursive(currentState, currentChecker, allStates):
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            if currentState.board[i][j] == CHECKER_EMPTY:
                newState = currentState.nextState(i, j, currentChecker)
                newHash = newState.getHash()
                if newHash not in allStates.keys():
                    allStates[newHash] = (newState, newState.ifEnd())
                    if not newState.ifEnd():
                        getAllStatesRecursive(newState, toggleChecker(currentChecker), allStates)

def getAllStates():
    initState = State()
    allStates = {}
    currentChecker = CHECKER_P1
    allStates[initState.getHash()] = (initState, initState.ifEnd())
    getAllStatesRecursive(initState, currentChecker, allStates)
    return allStates

allStates = getAllStates()

class Game(object):
    def __init__(self, player1, player2, feedback=True):
        self.p1 = player1
        self.p2 = player2
        self.p1.setChecker(CHECKER_P1)
        self.p2.setChecker(CHECKER_P2)
        self.currentState = State()
        self.currentPlayer = None
        self.allStates = allStates
        self.feedback = feedback

    def reset(self):
        self.currentState = State()
        self.currentPlayer = None

    def start(self, show=False):
        while True:
            if show:
                self.currentState.draw()
            if self.currentPlayer == self.p1:
                self.currentPlayer = self.p2
            else:
                self.currentPlayer = self.p1
            self.currentPlayer.feedState(self.currentState)
            (i, j, checker) = self.currentPlayer.takeAction()
            newState = self.currentState.nextState(i, j, checker)           
            hashVal = newState.getHash()            
            self.currentState, ifEnd = self.allStates[hashVal]
            self.currentPlayer.feedState(newState)
            if newState.ifEnd():
                if show:
                    self.currentState.draw()
                if self.feedback:
                    if newState.winner == CHECKER_P1:
                        self.p1.feedReward(1.)
                        self.p2.feedReward(-1.)
                    elif newState.winner == CHECKER_P2:
                        self.p1.feedReward(-1.)
                        self.p2.feedReward(1.)
                    else:               # Draw
                        self.p1.feedReward(-1.)
                        self.p2.feedReward(-1.)
                return self.currentState.winner

class AIPlayer(object):
    def __init__(self, learningRate = 0.1, exploreRatio = 0.1, discountRatio = 0.9):
        self.learningRate = learningRate
        self.exploreRatio = exploreRatio
        self.discountRatio = discountRatio
        self.Q = {}
        self.myStates = []
        self.currentState = None
        self.checker = None

    def setChecker(self, checker):
        self.checker = checker
        # Build Q table
        for stateHash in allStates:
            state, ifEnd = allStates[stateHash]
            if ifEnd:
                if state.winner == self.checker:
                    self.Q[stateHash] = 1.0
                else:
                    self.Q[stateHash] = -1.0
            else:
                self.Q[stateHash] = 0

    def reset(self):
        self.myStates = []
        self.currentState = None

    def feedState(self, state):
        self.myStates.append(state.getHash())
        self.currentState = state

    def takeAction(self):
        pendingStates = []
        pendingActions = []
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                if self.currentState.board[i][j] == CHECKER_EMPTY:
                    pendingStates.append(self.currentState.nextState(i, j, self.checker).getHash())
                    pendingActions.append((i, j, self.checker))

        if np.random.rand() < self.exploreRatio:
            np.random.shuffle(pendingActions)
            action = pendingActions[0]
            return action

        Qs = []
        for stateHash, action in zip(pendingStates, pendingActions):
            Qs.append((self.Q[stateHash], action))
        Qs.sort(key=lambda x: x[0], reverse=True)
        action = Qs[0][1]
        return action

    def feedReward(self, reward):
        currentStateHash = self.myStates[-1]
        self.Q[currentStateHash] += self.learningRate * (reward - self.Q[currentStateHash])
        for i in range(len(self.myStates)-2, -1, -1):
            currentStateHash = self.myStates[i]
            previousStateHash = self.myStates[i+1]
            self.Q[currentStateHash] += self.learningRate * (self.discountRatio * self.Q[previousStateHash] - self.Q[currentStateHash])
        self.myStates = []

    def savePolicy(self):
        with open('optimal_Q_{}'.format(self.checker), 'wb') as f:
            pickle.dump(self.Q, f)

    def loadPolicy(self):
        with open('optimal_Q_{}'.format(self.checker), 'rb') as f:
            self.Q = pickle.load(f)

class HumanPlayer(object):
    def __init__(self):
        self.state = None
        self.checker = None

    def setChecker(self, checker):
        self.checker = checker

    def feedState(self, state):
        self.state = state

    def takeAction(self):
        try:
            position = raw_input("Choose a position to place checker(1-9):")
            position = int(position) - 1
            i = position / 3 
            j = position % 3 
        except ValueError as e:
            raise ValueError("Position must be integer")

        if self.state.board[i][j] != CHECKER_EMPTY:
            return self.takeAction()
        return (i, j, self.checker)

    def feedReward(self, reward):
        pass

def Train(epoch=20000):
    player1 = AIPlayer()
    player2 = AIPlayer()
    game = Game(player1, player2)
    p1Win = 0.
    p2Win = 0.
    for i in range(epoch):
        print "Epoch {}".format(i)
        winner = game.start()
        if winner == CHECKER_P1:
            p1Win += 1
        elif winner == CHECKER_P2:
            p2Win += 1
        game.reset()
        player1.reset()
        player2.reset()
    print "P1: {} ".format(p1Win/epoch)
    print "P2: {} ".format(p2Win/epoch)
    player1.savePolicy()
    player2.savePolicy()

def Compete(turns=500):
    player1 = AIPlayer()
    player2 = AIPlayer()
    game = Game(player1, player2, False)
    p1Win = 0.
    p2Win = 0.
    player1.loadPolicy()
    # player2.loadPolicy()
    for i in range(turns):
        print "Turns {}".format(i)
        winner = game.start()
        if winner == CHECKER_P1:
            p1Win += 1
        elif winner == CHECKER_P2:
            p2Win += 1
        game.reset()
        player1.reset()
        player2.reset()
    print "P1: {} ".format(p1Win/turns)
    print "P2: {} ".format(p2Win/turns)

def Play():
    player1 = AIPlayer()
    player2 = HumanPlayer()
    game = Game(player1, player2, False)
    player1.loadPolicy()
    winner = game.start(show=True)
    winnerName = ''
    if winner == None:
        print "Draw!"; return
    elif winner == CHECKER_P1:
        winnerName = 'AI'
    else:
        winnername = 'Human'
    print "{} wins!".format(winnerName)

# Train(epoch=100000)
Compete()
# Play()