import os
import config
from modules import shared


def get_best_combinations(csv_file):
    # Vérification de la structure du CSV
    if not shared.csv_structure_check(csv_file):
        return  # Arrête l'exécution si la structure est incorrecte
    
    from main import print_stuff
    actions, anomalies = shared.read_csv(csv_file)
    
    n_actions = len(actions)
    total_combinations = (2 ** n_actions) - 1
    formatted_combinations = shared.format_combinations(total_combinations)
    
    shared.display_title("Optimized (dynamic)","en cours")
    start_time = shared.horodatage()
    
    best_combination, best_combinations = knapsack_dyna(actions)
    
    if config.LOGS:
        shared.start_logging(config.LOGFILE)
    
    end_time = shared.horodatage()
    shared.display_title("Optimized (dynamic)","terminé")
    
    shared.print_results(csv_file, best_combination, formatted_combinations, anomalies, start_time, end_time)
    if config.LOGS:
        shared.stop_logging()
        print_stuff(f'Fichier {config.LOGFILE} exporté.')
    
    shared.print_other_best(best_combinations)
    
    if config.GUI:
        input("Appuyez sur 'entrer' pour retourner au menu précédent.")

# Fonction de programmation sac à dos dynamique
def knapsack_dyna(actions):
    average_profit = shared.calculate_average_profit(actions)
    n = len(actions)
    #multiplier = 100
    multiplier = 10
    max_budget = int(config.MAX_BUDGET * multiplier) # Garder la précision du float
    min_budget = shared.calculate_min_budget(average_profit)

    dp = [0] * (max_budget + 1) # Liste de profit possibles
    chosen_actions = [[[] for _ in range(max_budget + 1)] for _ in range(n + 1)] # Liste d'actions choisies

    dyna_combinations = []
    seen_combinations = set()
    tested_combinations = 0

    for i in range(1, n + 1):
        action_cost_int = int(actions[i-1]['cost'] * multiplier) # Methode range() ne fonctionne pas avec un type float
        action_cost = actions[i-1]['cost']
        action_profit = actions[i-1]['profit']
        action_id = actions[i-1]['id']
        
        for budget in range(max_budget, action_cost_int - 1, -1):
            tested_combinations += 1
            new_profit = dp[budget - action_cost_int] + action_profit
            if new_profit > dp[budget]:
                dp[budget] = new_profit
                chosen_actions[i][budget] = chosen_actions[i-1][budget - action_cost_int] + [(action_id, action_cost)]
                
                combination_tuple = tuple(sorted(action_id for action_id, _ in chosen_actions[i][budget]))
                if combination_tuple not in seen_combinations:
                    seen_combinations.add(combination_tuple)
                    total_cost = sum(action_cost for _, action_cost in chosen_actions[i][budget])
                    
                    if total_cost <= config.MAX_BUDGET:
                        # Ajout de la combinaison à la liste
                        #dyna_combinations.append((dp[budget], total_cost, [action_id for action_id, _ in chosen_actions[i][budget]]))
                        dyna_combinations.append((dp[budget], total_cost, [action for action in actions if action['id'] in [action_id for action_id, _ in chosen_actions[i][budget]]]))
            else:
                chosen_actions[i][budget] = chosen_actions[i-1][budget]
    
    best_combinations = []
    for (profit, cost, combination) in dyna_combinations:
        if min_budget <= cost:
            best_combinations.append([combination, cost, profit])
    
    best_combinations = sorted(best_combinations, key=lambda x: x[2], reverse=True)
    best_combination = best_combinations[0]
    return best_combination, best_combinations
    
    print(f'{best_combination}')
    input("POUET POUET")