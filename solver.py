import json
from service import SolvePost, Service
from typing import List, Dict
from game_7_players import Player


class Solver:
    def __init__(self):
        with open("preflop_suggestions.json", 'r') as f:
            self.preflop_data: dict = json.load(f)
        self.service: Service = Service()
        self.hero_bet_sizes: Dict[List[float]] = {
            'flop': [20,40,80],
            'turn': [20,40,80],
            'river': [20,40,80],
        }
        self.opponent_bet_sizes: Dict[List[float]] = {
            'flop': [20,40,80],
            'turn': [20,40,80],
            'river': [20,40,80],
        }

    def get_preflop_ev(self, hole_cards: str, position: str):
        hole_cards_combo = hole_cards[0] + hole_cards[2]
        hole_cards_combo += "s" if hole_cards[1] == hole_cards[3] else ""

        combo_data = self.preflop_data.get(hole_cards_combo, None)
        if combo_data == None:
            combo_data = self.preflop_data.get(hole_cards_combo[:1])

        # print(hole_cards_combo)
        cards_ev = combo_data[position]
        return (cards_ev)

    def get_suggestion_tree(self, hero: Player, opponent:Player):
        IP, OOP = hero, opponent if hero.is_IP(opponent) else opponent, hero
        game_stage = self.service.define_game_stage(hero.game.board_cards)

        response = self.service.send_data_to_solver(
            SolvePost(
                hero_role = "IP" if hero.is_IP else "OOP",
                hole_cards=hero.hole_cards,
                pot=hero.game.total_pot,
                effective_stack=hero.game.min_effective_stack(),
                board=",".join(hero.game.board_cards),
                range_ip=",".join(IP.get_range()),
                range_oop=",".join(OOP.get_range()),
                game_stage=game_stage,
                bet_size_IP_bet=IP.bet_sizes[game_stage]["bet"],
                bet_size_IP_raise=IP.bet_sizes[game_stage]["raise"],
                bet_size_OOP_bet=OOP.bet_sizes[game_stage]["bet"],
                bet_size_OOP_raise=OOP.bet_sizes[game_stage]["raise"],
                accuracy=0.05,
                max_iteration=500,
                use_isomorphism=1,
                allin_threshold=0.67,
                et_thread_num=8
            )
        )



if __name__ == "__main__":
    solver = Solver()
    solver.get_preflop_ev("Ks3d", position="UTG")
