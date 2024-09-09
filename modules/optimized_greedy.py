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

    best_combination, best_combinations = knapsack_greedy(actions)

    if config.LOGS:
        shared.start_logging(config.LOGFILE)

    end_time = shared.horodatage()
    shared.display_title("Optimized (greedy)", "terminé")

    shared.print_results(
        csv_file,
        best_combination,
        formatted_combinations,
        anomalies,
        start_time,
        end_time)
    if config.LOGS:
        shared.stop_logging()
        print_stuff(f'Fichier {config.LOGFILE} exporté.')

    shared.print_other_best(best_combinations)

    if config.GUI:
        input("Appuyez sur 'entrer' pour retourner au menu précédent.")


def knapsack_greedy(actions):
    # Algorithme sac à dos glouton
    # Returns best_combination, best_combinations
    average_profit = shared.calculate_average_profit(actions)
    min_budget = shared.calculate_min_budget(average_profit)
    total_cost = 0
    total_profit = 0
    chosen_actions = []
    best_combinations = []

    # Parcourir les actions et les ajouter jusqu'à MAX_BUDGET
    for action in actions:
        if total_cost + action['cost'] <= config.MAX_BUDGET:
            chosen_actions.append(action)
            total_cost += action['cost']
            total_profit += action['profit']
            if min_budget <= total_cost:
                best_combinations.append(
                    [chosen_actions[:], total_cost, total_profit])

    best_combinations = sorted(
        best_combinations,
        key=lambda x: x[2],
        reverse=True)
    best_combination = [chosen_actions, total_cost, total_profit]
    # Retourne la combinaison choisie, le coût total et le profit total
    return best_combination, best_combinations
