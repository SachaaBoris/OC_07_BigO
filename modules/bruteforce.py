import os
import itertools
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

    choice = "y"
    if n_actions > 25:
        print_stuff(
            f'{n_actions} actions, soit {formatted_combinations} combinaisons à traiter...')
        choice = input(
            "Cela risque d'être très long.\nÊtes vous sûr de vouloir continuer ? ")

    if choice in ["y", "o", "yes", "oui"]:
        shared.display_title("Bruteforce", "en cours")
        start_time = shared.horodatage()

        best_combination, best_combinations = bruteforce(actions, n_actions)

        if config.LOGS:
            shared.start_logging(config.LOGFILE)

        end_time = shared.horodatage()
        shared.display_title("Bruteforce", "terminé")

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

        best_combinations = sorted(
            best_combinations,
            key=lambda x: x[2],
            reverse=True)
        shared.print_other_best(best_combinations)

    else:
        print_stuff(f'Process annulé.')

    if config.GUI:
        input("Appuyez sur 'entrer' pour retourner au menu précédent.")


def bruteforce(actions, n_actions):
    # Algorithme bruteforce
    # Returns best_combination, best_combinations
    average_profit = shared.calculate_average_profit(actions)
    min_budget = shared.calculate_min_budget(average_profit)
    best_combination = [[], 0, 0]
    best_combinations = []

    for r in range(1, n_actions + 1):
        for combination in itertools.combinations(actions, r):
            total_cost, total_profit = calculate_profit(combination)
            if min_budget <= total_cost <= config.MAX_BUDGET:
                if total_profit > best_combination[2]:
                    best_combination = [combination, total_cost, total_profit]
                    best_combinations.append(best_combination)

    best_combinations = sorted(
        best_combinations,
        key=lambda x: x[2],
        reverse=True)
    return best_combination, best_combinations


def calculate_profit(combination):
    total_cost = sum(action['cost'] for action in combination)
    total_profit = sum((action['profit']) for action in combination)
    return total_cost, total_profit
