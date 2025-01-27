# TEST
from service import Service, SolvePost
import json
from typing import List, Dict, Any
import time

service = Service()

def load_test_cases_from_json(json_path: str) -> List[Dict[str, Any]]:
    """
    Reads a JSON file at `json_path` and transforms its contents into
    a list of test case dictionaries with the following structure:

    test_cases:list = [
        {  
            "total_pot": float,
            "effective_stack": float,
            "board": List[str],
            "hole": List[str],
            "role": str,
            "bet_sizes": {
                "IP": {"bet": float, "raise": float},
                "OOP": {"bet": float, "raise": float}
            },
            "accuracy": float,
            "max_iteration": int,
            "isomorphism": int,
            "allin_threshold": float,
            "et_thread_num": int
        },
        ...
    ]
    """
    with open(json_path, "r") as f:
        raw_data = json.load(f)

    test_cases = []
    for item in raw_data:
        # Here we explicitly cast to ensure the correct types, 
        # though you can omit casting if you trust the JSON structure.
        test_case = {
            "total_pot": float(item["total_pot"]),
            "effective_stack": float(item["effective_stack"]),
            "board": item["board"],  # already a list of strings
            "hole": item["hole"],    # already a list of strings
            "role": item["role"],
            "bet_sizes": {
                "IP": {
                    "bet": float(item["bet_sizes"]["IP"]["bet"]),
                    "raise": float(item["bet_sizes"]["IP"]["raise"])
                },
                "OOP": {
                    "bet": float(item["bet_sizes"]["OOP"]["bet"]),
                    "raise": float(item["bet_sizes"]["OOP"]["raise"])
                }
            },
            "accuracy": float(item["accuracy"]),
            "max_iteration": int(item["max_iteration"]),
            "isomorphism": int(item["isomorphism"]),
            "allin_threshold": float(item["allin_threshold"]),
            "et_thread_num": int(item["et_thread_num"])
        }
        test_cases.append(test_case)

    return test_cases

def test(
    test_cases:list,
):
    with open("testing_results.txt", "w") as f:
        for i, scenario in enumerate(test_cases):
            game_stage = service.define_game_stage(scenario["board"])
            ranges = service.generate_auto_ranges(scenario["board"], scenario["hole"], scenario["role"])
            
            start_time = time.time()
            response = service.send_data_to_solver(
                SolvePost(
                    hole_cards="".join(scenario["hole"]),
                    pot=scenario["total_pot"],
                    effective_stack=scenario["effective_stack"],
                    board=scenario["board"],
                    range_ip=ranges["IP"],
                    range_oop=ranges["OOP"],
                    game_stage=game_stage,
                    bet_size_IP_bet=scenario["bet_sizes"]["IP"]["bet"],
                    bet_size_IP_raise=scenario["bet_sizes"]["IP"]["raise"],
                    bet_size_OOP_bet=scenario["bet_sizes"]["OOP"]["bet"],
                    bet_size_OOP_raise=scenario["bet_sizes"]["OOP"]["raise"],
                    accuracy=scenario["accuracy"],
                    max_iteration=scenario["max_iteration"],
                    use_isomorphism=scenario["isomorphism"],
                    allin_threshold=scenario["allin_threshold"],
                    et_thread_num=scenario["et_thread_num"]
                )
            )
            end_time = time.time()
            response_time = end_time - start_time

            text_to_write = f"""
                TESTING SCENARIO #{i+1}:
                !Solver Input:
                - total pot: {scenario["total_pot"]}
                - effective stack: {scenario["effective_stack"]}
                - hole cards: {scenario["hole"]}
                - board cards: {scenario["board"]}
                - game_stage: {game_stage}
                - role: {scenario["role"]}
                - range_ip: {ranges["IP"]}
                - range_oop: {ranges["OOP"]}
                - bet_size_IP_bet: {scenario["bet_sizes"]["IP"]["bet"]}
                - bet_size_IP_raise: {scenario["bet_sizes"]["IP"]["raise"]}
                - bet_size_OOP_bet: {scenario["bet_sizes"]["OOP"]["bet"]}
                - bet_size_OOP_raise: {scenario["bet_sizes"]["OOP"]["raise"]}
                - accuracy: {scenario["accuracy"]}
                - max_iteration: {scenario["max_iteration"]}
                - use_isomorphism: {scenario["isomorphism"]}
                - allin_threshold: {scenario["allin_threshold"]}
                - et_thread_num: {scenario["et_thread_num"]}
                !Solver Result:
                {response}
                !Response Time:
                {response_time}
                ---------------------------------------------
            """
            f.write(text_to_write)


def main():
    board = ["9c", "8c", "3h"]
    game_stage = service.define_game_stage(board)
    hero_hole = ["Jh", "Kh"]  
    role = "OOP"
    ranges = service.generate_auto_ranges(board, hero_hole, role)
    print(ranges)
    range_ip=ranges["IP"]
    range_oop=ranges["OOP"]
    bet_size_ip_bet = 50
    bet_size_ip_raise = 60
    bet_size_oop_bet = 50
    bet_size_oop_raise = 60

    response = service.send_data_to_solver(
        SolvePost(
            hole_cards="".join(hero_hole),
            pot=4,
            effective_stack=10,
            board=board,
            range_ip=range_ip,
            range_oop=range_oop,
            game_stage=game_stage,
            bet_size_IP_bet=bet_size_ip_bet,
            bet_size_IP_raise=bet_size_ip_raise,
            bet_size_OOP_bet=bet_size_oop_bet,
            bet_size_OOP_raise=bet_size_oop_raise,
            accuracy=0.05,
            max_iteration=200,
            use_isomorphism=1,
            allin_threshold=0.67,
            et_thread_num=8

        )
    )
    print(response)

if __name__ == "__main__":
    test_cases = load_test_cases_from_json("test_cases.json")
    test(test_cases)
