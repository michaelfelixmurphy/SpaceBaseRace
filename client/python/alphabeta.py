import random

def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    player = game.to_move(state)
    
    def max_value(state, alpha, beta, depth):
        if game.cutoff_test(state, depth):
            return eval_fn(state)
        v = -float("inf")
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state,depth):
            return eval_fn(state)
        v = float("inf")
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min (beta, v)
        return v

    # Body
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state,player))
    return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a),
                                      -float("inf"), float("inf"), 0))

class Game:
    def actions(self, state):
        abstract
    
    def result(self, state, move):
        abstract

    def utility(self, state, player):
        abstract

    def terminal_test(self, state):
        return not self.actions(state)

    def to_move(self, state):
        return state.to_move

    def display(self, state):
        print state

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

               
