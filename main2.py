from game_7_players import Game, UTG, LJ, HJ, CO, BTN, SB, BB
from solver import Solver

if __name__ == "__main__":
  # testing scenario for flop
  game = Game(
    total_pot=0,
    effective_stack=200,
    bb=2
  )
  solver = Solver()
  player1 = SB(game=game, effective_stack=200)
  player2 = BB(game=game, effective_stack=200)
  player3 = UTG(game=game, effective_stack=200)
  player4 = LJ(game=game, effective_stack=200)
  player5 = HJ(game=game, effective_stack=200)
  player6 = CO(game=game, effective_stack=200)
  player7 = BTN(game=game, effective_stack=200)

  game.add_players([player1, player2, player3, player4, player5, player6, player7])

  # define us and our cards
  we_are = player5
  we_are.hole_cards = "Ks3h"

  # !PRE-FLOP
  game.set_round("pre-flop")
  # player1 (SB) posts 1$
  player1.post()
  # player2 (BB) posts 2$
  player2.post()
  # player3 (UTG) folds
  player3.fold()
  # LJ raises 6$
  player4.raise_(6)
  # HJ(we are) calls 6$
  combo_ev = solver.get_preflop_ev(we_are.hole_cards, we_are.position)
  print(f"We have cards with this pre-flop EV: {combo_ev}")
  we_are.call()
  # CO folds
  player6.fold()
  # BTN calls
  player7.call()
  # SB folds
  player1.fold()
  # BB calls 4 (to complete)
  player2.call()

  print(game.active_positions)

  # !FLOP
  game.next_round()
  game.set_board_cards(['Kc', '9d', '3s'])
  print(f'total pot: {game.total_pot}\nboard cards: {game.board_cards}')

  # BB (player 2) checks
  player2.check()
  # LJ (player4) bets 10$
  player4.bet(10)
  # HJ (we are)
  # !solver's help
  # response = solver.get_suggestion_tree()
  we_are.raise_(25)
  # BTN folds
  player7.fold()
  # BB folds
  player2.fold()
  # UTG calls 15 to complete
  player3.call()

  # !TURN
  game.next_round()
  game.add_board_card("7d")
  print(f'total pot: {game.total_pot}\nboard cards: {game.board_cards}')

  print(game.history)






  



  
  
  
  


