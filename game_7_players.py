from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import re

class Game:
    def __init__(self, total_pot: float, effective_stack: float, bb: float):
        self.total_pot: float = total_pot
        self.effective_stack: float = effective_stack
        self.round: str = "pre-flop"
        self.board_cards: List[str | None] = []
        self.active_positions: List[str] = ["SB", "BB", "UTG", "LJ", "HJ", "CO", "BTN" ]
        self.history: Dict[str, Dict[str, str | None]] = {
            # [FOLD, CHECK, CALL, BET SMALL/MEDIUM/BIG, RAISE SMALL/MEDIUM/BIG, ALL-IN, POST, -(UNACTIVE) ]
            "pre-flop": {"UTG": None, "LJ": None, "HJ": None, "CO": None, "BTN": None, "SB": None, "BB": None},
            "flop": {"UTG": None, "LJ": None, "HJ": None, "CO": None, "BTN": None, "SB": None, "BB": None},
            "turn": {"UTG": None, "LJ": None, "HJ": None, "CO": None, "BTN": None, "SB": None, "BB": None},
            "river": {"UTG": None, "LJ": None, "HJ": None, "CO": None, "BTN": None, "SB": None, "BB": None}
        }
        self.bb: float = bb
        self.players: List[Player] = []
        print("Game started.")

    def set_round(self, round:str):
        self.round = round
        print(f"Game round set to \"{round}\".")

    def change_bet_size(self, round: str, type: str, amount: float):
        self.bet_sizes[round][type] == amount
        
    def set_board_cards(self, cards:List[str]):
        self.board_cards = cards
    
    def add_board_card(self, card: str):
        self.board_cards.append(card)
        print(f"Board cards updated. New board: {self.board_cards}.")

    def next_round(self):
        if self.round == "pre-flop":
            self.round = "flop"
        elif self.round == "flop":
            self.round = "turn"
        elif self.round == "turn":
            self.round = "river"

        for player in self.players:
            if player.position not in self.active_positions:
                self.update_history(self.round, player.position, "-")

        print(f"Round changes to {self.round}.")

    def update_history(self, round: str, position: str, action: str):
        self.history[round][position] = action

    def add_to_pot(self, quantity: float):
        self.total_pot += quantity

    def evaluate_raise(self, quantity:float) -> str:
        bb_quantity = quantity / self.bb
        if bb_quantity <= 2.5:
            return f"SMALL"
        elif bb_quantity <= 11:
            return f"MEDIUM"
        elif bb_quantity <= 24:
            return f"BIG"
    
    def evaluate_bet(self, quantity:float) -> str:
        bb_quantity = quantity / self.bb
        if bb_quantity <= 2.5:
            return f"SMALL"
        elif bb_quantity <= 11:
            return f"MEDIUM"
        elif bb_quantity <= 24:
            return f"BIG"
    
    
    def add_players(self, players: List["Player"]):
        self.players = players
        print(f"Players added.")
    
    def show_results_in_terminal(self):
        for round, result in self.history.items():
            print("\n-------------------------")
            print(f"Round:{round}")
            print("-----")
            for position, action in result.items():
                print(f"{position}: {action}")
    
    def min_effective_stack(self):
        return min([i.effective_stack for i in self.players])

            
class Player(ABC):
    def __init__(self, position: str, game: Game, effective_stack:float, hole_cards: Optional[str] = None):
        self.position: str = position  # UTG, LJ, HJ, CO, BTN, SB, BB
        self.bet_sizes: Dict[Dict[float]] = {
            "flop": {"bet": 50, "raise": 60},
            "turn": {"bet": 50, "raise": 60},
            "river": {"bet": 50, "raise": 60}
        }
        self.hole_cards: str | None = hole_cards
        self.game: Game = game
        self.puted_money: Dict[float] = {
            "pre-flop": 0,
            "flop": 0,
            "turn": 0,
            "river": 0
        }

        self.effective_stack: float = effective_stack

    def is_IP(self, opponent: "Player") -> bool:
        hero_index = self.game.active_positions.index(self.position)
        opponent_index = opponent.game.active_positions.index(opponent.position)
        return True if hero_index > opponent_index else False

    @abstractmethod
    def get_ranges(self, opponent_position:str):
        pass
    
    def fold(self):
        self.game.update_history(
            self.game.round,
            self.position,
            action="FOLD"
            )
        self.game.active_positions.remove(self.position)
        print(f"{self.position}: FOLD")

    def raise_(self, quantity: float):
        quantity = float(quantity)
        raise_type = self.game.evaluate_raise(quantity)
        self.game.update_history(self.game.round, self.position, f"RAISE {raise_type} ({quantity})")
        self.puted_money[self.game.round] += quantity
        self.game.add_to_pot(quantity)
        self.effective_stack -= quantity
        print(f"{self.position}: RAISE ({quantity})")
        
    def call(self):
        biggest_puted_money_for_round = max([i.puted_money[self.game.round] for i in self.game.players])
        money_to_complete = biggest_puted_money_for_round - self.puted_money[self.game.round]

        self.game.add_to_pot(money_to_complete)
        self.effective_stack -= money_to_complete
        self.game.update_history(self.game.round, self.position, f"CALL ({biggest_puted_money_for_round})")

        if money_to_complete == biggest_puted_money_for_round:
            print(f"{self.position}: CALL ({money_to_complete})")
        else:
            print(f"{self.position}: CALL ({money_to_complete})(to complete)") 
    
    def check(self):
        self.game.update_history(self.game.round, self.position, "CHECK")
        print(f'{self.position}: CHECK')
    
    def bet(self, quantity:float):
        bet_type = self.game.evaluate_bet(quantity)
        self.game.update_history(self.game.round, self.position, f"BET {bet_type} ({quantity})")
        self.puted_money[self.game.round] += quantity
        self.game.add_to_pot(quantity)
        self.effective_stack -= quantity
        print(f"{self.position}: BET ({quantity})")
    
    
class UTG(Player):
    def __init__(self, game: Game, effective_stack: float):
        super().__init__(position="UTG", game=game, effective_stack=effective_stack)
    
    @staticmethod
    def get_ranges(opponent_position:str):
        hero_range = ""
        opponent_range = ""

        if opponent_position == "SB":
            hero_f_path = r"ranges\6max_range\UTG\2.5bb\SB\11.0bb\UTG\Call\UTG_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\SB\11.0bb\UTG\Call\SB_range.txt"
        elif opponent_position == "BB":
            hero_f_path = r"ranges\6max_range\UTG\2.5bb\BB\Call\UTG_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\BB\Call\BB_range.txt"
        elif opponent_position in ("LJ", "HJ"):
            hero_f_path = r"ranges\6max_range\UTG\2.5bb\MP\8.5bb\UTG\Call\UTG_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\MP\8.5bb\UTG\Call\MP_range.txt"
        elif opponent_position == "CO":
            hero_f_path = r"ranges\6max_range\UTG\2.5bb\CO\8.5bb\UTG\Call\UTG_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\CO\8.5bb\UTG\Call\CO_range.txt"
        elif opponent_position == "BTN":
            hero_f_path = r"ranges\6max_range\UTG\2.5bb\BTN\Call\UTG_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\BTN\Call\BTN_range.txt"
        
        with open(hero_f_path, 'r') as f:
            hero_range = f.read()
        with open(opponent_f_path, 'r') as f:
            opponent_range = f.read()
        
        
        return hero_range, opponent_range


class LJ(Player):
    def __init__(self, game: Game, effective_stack: float):
        super().__init__(position="LJ", game=game, effective_stack=effective_stack)

    @staticmethod
    def get_ranges(opponent_position:str) -> List[str]:
        hero_range = ""
        opponent_range = ""
        if opponent_position == "SB":
            hero_f_path = r"ranges\6max_range\MP\2.5bb\SB\11.0bb\MP\Call\MP_range.txt"
            opponent_f_path = r"ranges\6max_range\MP\2.5bb\SB\11.0bb\MP\Call\SB_range.txt"
        elif opponent_position == "BB":
            hero_f_path = r"ranges\6max_range\MP\2.5bb\BB\Call\MP_range.txt"
            opponent_f_path = r"ranges\6max_range\MP\2.5bb\BB\Call\BB_range.txt"
        elif opponent_position == "UTG":
            hero_f_path = r"ranges\6max_range\UTG\2.5bb\MP\8.5bb\UTG\Call\MP_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\MP\8.5bb\UTG\Call\UTG_range.txt"
        elif opponent_position in ("CO", "HJ"):
            hero_f_path = r"ranges\6max_range\MP\2.5bb\CO\8.5bb\MP\Call\MP_range.txt"
            opponent_f_path = r"ranges\6max_range\MP\2.5bb\CO\8.5bb\MP\Call\CO_range.txt"
        elif opponent_position == "BTN":
            hero_f_path = r"ranges\6max_range\MP\2.5bb\BTN\Call\BTN_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\BTN\Call\BTN_range.txt"

        with open(hero_f_path, 'r') as f:
            hero_range = f.read()
        with open(opponent_f_path, 'r') as f:
            opponent_range = f.read()
        
        
        return hero_range, opponent_range


class HJ(Player):
    def __init__(self, game: Game, effective_stack: float):
        super().__init__(position="HJ", game=game, effective_stack=effective_stack)

    @staticmethod
    def get_ranges(opponent_position:str) -> List[str]:
        hero_range = ""
        opponent_range = ""
        if opponent_position == "SB":
            hero_f_path = r"ranges\6max_range\MP\2.5bb\SB\11.0bb\MP\Call\MP_range.txt"
            opponent_f_path = r"ranges\6max_range\MP\2.5bb\SB\11.0bb\MP\Call\SB_range.txt"
        elif opponent_position == "BB":
            hero_f_path = r"ranges\6max_range\MP\2.5bb\BB\Call\MP_range.txt"
            opponent_f_path = r"ranges\6max_range\MP\2.5bb\BB\Call\BB_range.txt"
        elif opponent_position in ("UTG", "LJ"):
            hero_f_path = r"ranges\6max_range\UTG\2.5bb\MP\8.5bb\UTG\Call\MP_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\MP\8.5bb\UTG\Call\UTG_range.txt"
        elif opponent_position == "CO":
            hero_f_path = r"ranges\6max_range\MP\2.5bb\CO\8.5bb\MP\Call\MP_range.txt"
            opponent_f_path = r"ranges\6max_range\MP\2.5bb\CO\8.5bb\MP\Call\CO_range.txt"
        elif opponent_position == "BTN":
            hero_f_path = r"ranges\6max_range\MP\2.5bb\BTN\Call\MP_range.txt"
            opponent_f_path = r"ranges\6max_range\MP\2.5bb\BTN\Call\BTN_range.txt"

        with open(hero_f_path, 'r') as f:
            hero_range = f.read()
        with open(opponent_f_path, 'r') as f:
            opponent_range = f.read()
        
        
        return hero_range, opponent_range

class CO(Player):
    def __init__(self, game: Game, effective_stack: float):
        super().__init__(position="CO", game=game, effective_stack=effective_stack)

    @staticmethod
    def get_ranges(opponent_position:str) -> List[str]:
        hero_range = ""
        opponent_range = ""

        if opponent_position == "SB":
            hero_f_path = r"ranges\6max_range\CO\2.5bb\SB\11.0bb\CO\Call\CO_range.txt"
            opponent_f_path = r"ranges\6max_range\CO\2.5bb\SB\11.0bb\CO\Call\SB_range.txt"
        elif opponent_position == "BB":
            hero_f_path = r"ranges\6max_range\CO\2.5bb\BB\Call\CO_range.txt"
            opponent_f_path = r"ranges\6max_range\CO\2.5bb\BB\Call\BB_range.txt"
        elif opponent_position in ("LJ", "HJ"):
            hero_f_path = r"ranges\6max_range\MP\2.5bb\CO\8.5bb\MP\Call\CO_range.txt"
            opponent_f_path = r"ranges\6max_range\MP\2.5bb\CO\8.5bb\MP\Call\MP_range.txt"
        elif opponent_position == "UTG":
            hero_f_path = r"ranges\6max_range\UTG\2.5bb\CO\8.5bb\UTG\Call\CO_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\CO\8.5bb\UTG\Call\UTG_range.txt"
        elif opponent_position == "BTN":
            hero_f_path = r"ranges\6max_range\CO\2.5bb\BTN\Call\CO_range.txt"
            opponent_f_path = r"ranges\6max_range\CO\2.5bb\BTN\Call\BTN_range.txt"

        with open(hero_f_path, 'r') as f:
            hero_range = f.read()
        with open(opponent_f_path, 'r') as f:
            opponent_range = f.read()
        
        
        return hero_range, opponent_range


class BTN(Player):
    def __init__(self, game: Game, effective_stack: float):
        super().__init__(position="BTN", game=game, effective_stack=effective_stack)

    @staticmethod
    def get_ranges(opponent_position:str) -> List[str]:
        hero_range = ""
        opponent_range = ""

        if opponent_position == "SB":
            hero_f_path = r"ranges\6max_range\BTN\2.5bb\SB\11.0bb\BTN\Call\BTN_range.txt"
            opponent_f_path = r"ranges\6max_range\BTN\2.5bb\SB\11.0bb\BTN\Call\SB_range.txt"
        elif opponent_position == "BB":
            hero_f_path = r"ranges\6max_range\BTN\2.5bb\BB\Call\BTN_range.txt"
            opponent_f_path = r"ranges\6max_range\BTN\2.5bb\BB\Call\BB_range.txt"
        elif opponent_position in ("LJ", "HJ"):
            hero_f_path = r"ranges\6max_range\MP\2.5bb\BTN\Call\BTN_range.txt"
            opponent_f_path = r"ranges\6max_range\MP\2.5bb\BTN\Call\MP_range.txt"
        elif opponent_position == "UTG":
            hero_f_path = r"ranges\6max_range\UTG\2.5bb\BTN\Call\BTN_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\BTN\Call\UTG_range.txt"
        elif opponent_position == "CO":
            hero_f_path = r"ranges\6max_range\CO\2.5bb\BTN\Call\BTN_range.txt"
            opponent_f_path = r"ranges\6max_range\CO\2.5bb\BTN\Call\CO_range.txt"

        with open(hero_f_path, 'r') as f:
            hero_range = f.read()
        with open(opponent_f_path, 'r') as f:
            opponent_range = f.read()
        
        
        return hero_range, opponent_range


class Blinds(Player):
    def __init__(self, position: str, game: Game, effective_stack: float):
        super().__init__(position=position, game=game, effective_stack=effective_stack)
        self._game = game
        self._position = position

    def post(self):
        quantity = float(self._game.bb if self.position == "BB" else self._game.bb / 2)
        self.puted_money[self.game.round] += quantity
        self._game.add_to_pot(quantity)
        self.effective_stack -= quantity
        self._game.update_history("pre-flop", self._position, f"POST ({quantity})")
        print(f"{self.position}: POST ({quantity})")
    
    @staticmethod
    def get_ranges(opponent_position:str):
        pass

class SB(Blinds):
    def __init__(self, game: Game, effective_stack: float):
        super().__init__(position="SB", game=game, effective_stack=effective_stack)

    @staticmethod
    def get_ranges(opponent_position:str) -> List[str]:
        hero_range = ""
        opponent_range = ""

        if opponent_position == "BTN":
            hero_f_path = r"ranges\6max_range\BTN\2.5bb\SB\11.0bb\BTN\Call\SB_range.txt"
            opponent_f_path = r"ranges\6max_range\BTN\2.5bb\SB\11.0bb\BTN\Call\BTN_range.txt"
        elif opponent_position == "BB":
            hero_f_path = r"ranges\6max_range\SB\3.0bb\BB\Call\SB_range.txt"
            opponent_f_path = r"ranges\6max_range\SB\3.0bb\BB\Call\BB_range.txt"
        elif opponent_position in ("LJ", "HJ"):
            hero_f_path = r"ranges\6max_range\MP\2.5bb\SB\11.0bb\MP\Call\SB_range.txt"
            opponent_f_path = r"ranges\6max_range\MP\2.5bb\SB\11.0bb\MP\Call\MP_range.txt"
        elif opponent_position == "UTG":
            hero_f_path = r"ranges\6max_range\UTG\2.5bb\SB\11.0bb\UTG\Call\SB_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\SB\11.0bb\UTG\Call\UTG_range.txt"
        elif opponent_position == "CO":
            hero_f_path = r"ranges\6max_range\CO\2.5bb\SB\11.0bb\CO\Call\SB_range.txt"
            opponent_f_path = r"ranges\6max_range\CO\2.5bb\SB\11.0bb\CO\Call\CO_range.txt"

        with open(hero_f_path, 'r') as f:
            hero_range = f.read()
        with open(opponent_f_path, 'r') as f:
            opponent_range = f.read()
        
        
        return hero_range, opponent_range


class BB(Blinds):
    def __init__(self, game: Game, effective_stack: float):
        super().__init__(position="BB", game=game, effective_stack=effective_stack)

    @staticmethod
    def get_ranges(opponent_position:str) -> List[str]:
        hero_range = ""
        opponent_range = ""

        if opponent_position == "BTN":
            hero_f_path = r"ranges\6max_range\BTN\2.5bb\BB\Call\BB_range.txt"
            opponent_f_path = r"ranges\6max_range\BTN\2.5bb\BB\Call\BTN_range.txt"
        elif opponent_position == "SB":
            hero_f_path = r"ranges\6max_range\SB\3.0bb\BB\Call\BB_range.txt"
            opponent_f_path = r"ranges\6max_range\SB\3.0bb\BB\Call\SB_range.txt"
        elif opponent_position in ("LJ", "HJ"):
            hero_f_path = r"ranges\6max_range\MP\2.5bb\BB\Call\BB_range.txt"
            opponent_f_path = r"ranges\6max_range\MP\2.5bb\BB\Call\MP_range.txt"
        elif opponent_position == "UTG":
            hero_f_path = r"ranges\6max_range\UTG\2.5bb\BB\Call\BB_range.txt"
            opponent_f_path = r"ranges\6max_range\UTG\2.5bb\BB\Call\UTG_range.txt"
        elif opponent_position == "CO":
            hero_f_path = r"ranges\6max_range\CO\2.5bb\BB\Call\BB_range.txt"
            opponent_f_path = r"ranges\6max_range\CO\2.5bb\BB\Call\CO_range.txt"

        with open(hero_f_path, 'r') as f:
            hero_range = f.read()
        with open(opponent_f_path, 'r') as f:
            opponent_range = f.read()
        
        
        return hero_range, opponent_range
