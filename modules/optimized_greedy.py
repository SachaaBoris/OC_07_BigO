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

    shared.display_title("Optimized (greedy)", "en cours")
    start_time = shared.horodatage()

    best_combination, best_combinations = greedy_list(actions)

    if config.LOGS:
        shared.start_logging(config.LOGFILE)

    end_time = shared.horodatage()
    shared.display_title("Optimized (greedy)", "terminé")

    shared.print_results(csv_file,best_combination,
        formatted_combinations,anomalies,start_time,end_time)
    if config.LOGS:
        shared.stop_logging()
        print_stuff(f'Fichier {config.LOGFILE} exporté.')

    shared.print_other_best(best_combinations)

    if config.GUI:
        input("Appuyez sur 'entrer' pour retourner au menu précédent.")

def greedy_list(actions):
    # Trier la liste pour comparer plusieurs résultats
    # Returns best_combination, best_combinations
    actions_percent_desc = actions
    actions_percent_asc = actions[::-1]
    actions_real_desc = sorted(actions,
        key=lambda action: action['profit'], reverse=True)
    actions_real_asc = actions_real_desc[::-1]
    actions_price_desc = sorted(actions,
        key=lambda action: action['cost'], reverse=True)
    actions_price_asc = actions_price_desc[::-1]

    best_percent_desc = knapsack_greedy(actions_percent_desc)
    best_percent_asc = knapsack_greedy(actions_percent_asc)
    best_real_desc = knapsack_greedy(actions_real_desc)
    best_real_asc = knapsack_greedy(actions_real_asc)
    best_price_desc = knapsack_greedy(actions_price_desc)
    best_price_asc = knapsack_greedy(actions_price_asc)

    combinations = [best_percent_desc, best_percent_asc, best_real_desc,
        best_real_asc, best_price_desc, best_price_asc]

    combinations = sorted(combinations, key=lambda x: x[2], reverse=True)

    return combinations[0], combinations

def knapsack_greedy(actions):
    # Algorithme glouton
    # Returns best_combination
    total_cost = 0
    total_profit = 0
    chosen_actions = []

    # Parcourir les actions et les ajouter jusqu'à MAX_BUDGET
    for action in actions:
        if total_cost + action['cost'] <= config.MAX_BUDGET:
            chosen_actions.append(action)
            total_cost += action['cost']
            total_profit += action['profit']

    best_combination = [chosen_actions, total_cost, total_profit]
    best_combinations = [best_combination]
    # Retourne la combinaison choisie, le coût total et le profit total
    return best_combination
