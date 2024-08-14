import os
import sys
import time
import psutil
import itertools
from prettytable import PrettyTable
from contextlib import redirect_stdout
from datetime import datetime
from main import clear_screen
from main import print_stuff
import config


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

def format_time(seconds):
    intervals = [
        ('years', 31536000),
        ('months', 2592000),
        ('weeks', 604800),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1),
        ('milliseconds', 0.001),
    ]
    
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append(f"{int(value)} {name.rstrip('s') if value == 1 else name}")
            
    return ', '.join(result)

def work_estimation(n_actions):
    total_combinations = (2 ** n_actions) - 1
    estimated_time = total_combinations * 0.00000568
    formatted_time = format_time(estimated_time)
    return total_combinations, estimated_time, formatted_time

def window_width(table):
    table_str = table.get_string()
    first_line = table_str.split('\n')[0]
    table_width = len(first_line)
    if table_width > 130:
        cmd = f"mode {table_width + 2},35"
        os.system(cmd)
        print_stuff(config.CONSOLE_CONTENT)

def print_stuff_results(combinations, anomalies, estimated_time, start_time, end_time):
    # Affiche les 3 meilleurs résultats
    print_stuff("\n3 meilleus achats :")
    my_table = PrettyTable(["ID", "Profit"])
    
    for i, (combination, profit) in enumerate(combinations[:3], start=1):
        ids = ", ".join(f"id#{action['id'][-4:]}" for action in combination)
        formatted_profit = f"{profit:.2f}€"
        my_table.add_row([ids, formatted_profit])
    
    window_width(my_table)
    print_stuff(my_table)
    
    my_table = PrettyTable(["ID", "Profit"])
    # Affiche les 3 pires résultats
    print_stuff("\n3 pires achats :")
    for i, (combination, profit) in enumerate(reversed(combinations[-3:]), start=1):
        ids = ", ".join(f"id#{action['id'][-4:]}" for action in combination)
        formatted_profit = f"{profit:.2f}€"
        my_table.add_row([ids, formatted_profit])
    
    window_width(my_table)
    print_stuff(my_table)
    if len(anomalies) > 0:
        print_stuff('\n' + 'Anomalies :\n' + str(anomalies))
    else:
        print_stuff('\n' + 'Aucune anomalie trouvée.')
    print_stuff(f'Parmis {len(combinations)} combinaisons valides.')
    
    # Horodatage de fin + process memoire
    process = psutil.Process()
    print_stuff(f"Utilisation de la mémoire : {process.memory_info().rss / (1024 * 1024):.2f} Mo")
    print_stuff("Début du script : " + start_time.strftime("%Y-%m-%d %H:%M:%S"))
    print_stuff("Fin du script   : " + end_time.strftime("%Y-%m-%d %H:%M:%S"))
    print_stuff(f"Temps d'exécution estimé : {estimated_time}")
    print_stuff(f"Temps d'exécution réel   : {end_time - start_time}")
    
def calculate_profit(combination):
    total_cost = sum(action['cost'] for action in combination)
    total_profit = sum(action['cost'] * action['profit'] for action in combination)
    return total_cost, total_profit

def combinations_library(actions):
    # Liste pour stocker les combinaisons valides avec leur bénéfice
    combinations = []

    # Parcourir toutes les combinaisons possibles
    for r in range(1, len(actions) + 1):
        for combination in itertools.combinations(actions, r):
            total_cost, total_profit = calculate_profit(combination)
            if total_cost <= config.MAX_BUDGET:
                combinations.append((combination, total_profit))

    # Trier les combinaisons par profit décroissant
    return sorted(combinations, key=lambda x: x[1], reverse=True)
