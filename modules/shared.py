import os
import sys
import csv
import time
import psutil
import config
from prettytable import PrettyTable
from contextlib import redirect_stdout
from datetime import datetime
from main import clear_screen
from main import print_stuff


class Logger:
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log = open(log_file, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()


def start_logging(log_file):
    open(log_file, 'w').close()
    sys.stdout = Logger(log_file)
    sys.stderr = Logger(log_file)


def stop_logging():
    sys.stdout.log.close()
    sys.stdout = sys.stdout.terminal
    sys.stderr.log.close()
    sys.stderr = sys.stderr.terminal


def display_title(type, status):
    clear_screen()
    print_stuff("\nAlgoInvest&Trade")
    print_stuff("Optimisation d'achat d'actions")
    print_stuff(f'\nMethode {type} {status}.')
    CONSOLE_CONTENT = ''


def horodatage():
    return datetime.now()


def format_combinations(combinations):
    if combinations > 999999999999:
        combinations = format(combinations, ".2e")
    elif combinations > 999999 and combinations <= 999999999999:
        combinations = f"{combinations:,}".replace(',', ' ')
    return combinations


def window_width(table):
    table_str = table.get_string()
    first_line = table_str.split('\n')[0]
    table_width = len(first_line)
    if table_width > 130:
        cmd = f"mode {table_width + 2},35"
        os.system(cmd)
        print_stuff(config.CONSOLE_CONTENT)


def chunk_ids(ids_list, chunk_size):
    """Divise la liste d'IDs en sous-listes de taille maximale `chunk_size`."""
    for i in range(0, len(ids_list), chunk_size):
        yield ids_list[i:i + chunk_size]


def print_results(csv_file, combination, total_combinations,
                  anomalies, start_time, end_time):
    # Affiche le meilleur résultat
    action_set = os.path.basename(csv_file)
    print_stuff(f"\nMeilleur achat pour {action_set} :")
    my_table = PrettyTable(["Combinaison", "Coût", "Profit"])
    combination_cost = f"{combination[1]:.2f}€"
    combination_profit = f"{combination[2]:.2f}€"
    ids_list = [action['id'][-4:] for action in combination[0]]

    for index, chunk in enumerate(chunk_ids(ids_list, 13)):
        ids = ", ".join(chunk)
        if index == 0:
            my_table.add_row([ids, combination_cost, combination_profit])
        else:
            my_table.add_row([ids, "", ""])

    window_width(my_table)
    print_stuff(my_table)

    # Horodatage de fin + process memoire
    if len(anomalies) > 0:
        print_stuff(f"\nAnomalies détectées       : {len(anomalies)}")
    else:
        print_stuff("\nAucune anomalie détectée.")
    process = psutil.Process()
    print_stuff(f"Combinaisons possibles    : {total_combinations}")
    print_stuff(
        f"Utilisation de la mémoire : {process.memory_info().rss / (1024 * 1024):.2f} Mo")
    print_stuff("Début du script           : " +
                start_time.strftime("%Y-%m-%d %H:%M:%S"))
    print_stuff("Fin du script             : " +
                end_time.strftime("%Y-%m-%d %H:%M:%S"))
    print_stuff(f"Temps d'exécution         : {end_time - start_time}\n")


def csv_structure_check(filepath):
    expected_header = ['name', 'price', 'profit']

    try:
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)

            if header != expected_header:
                print(
                    "Le dataset n'est pas conforme, en-tête name, price, profit attendu.")
                choice = input("Appuyez sur entrée pour revenir au menu. ")
                return False
        return True

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{filepath}' est introuvable.")
        return False

    except Exception as e:
        print(f"Erreur lors de la vérification du fichier CSV : {e}")
        return False


def calculate_average_profit(actions):
    total_profit = sum(action['profit'] for action in actions)
    average_profit = total_profit / len(actions) if actions else 0
    return average_profit


def calculate_min_budget(average_profit):
    min_budget = config.MAX_BUDGET - (config.MAX_BUDGET * average_profit / 100)
    return min_budget


def print_other_best(best_combinations):
    print("Autres combinaisons trouvées :")
    for i, (combination, cost, profit) in enumerate(
            best_combinations[:10], start=1):
        print(f"Coût : {cost:.2f}€ | Profit : {profit:.2f}€")

    print("\n")


def read_csv(filepath):
    # Lecture du CSV et remplissage de l'array actions
    actions = []
    anomalies = []

    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            price = float(row['price'])
            profit = float(row['profit'])

            # Ajouter à la liste seulement les données normales
            if price > 0 and profit > 0:
                actions.append({
                    'id': name,
                    'cost': price,
                    'profit': (profit / 100) * price
                })
            else:
                anomalies.append({
                    'id': name,
                    'cost': price,
                    'profit': profit
                })

    actions = sorted(
        actions,
        key=lambda action: action['profit'],
        reverse=True)
    return actions, anomalies
