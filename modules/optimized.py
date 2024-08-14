import csv
import os
from modules import shared
import config


def get_best_combinations(csv_file):
    from main import print_stuff
    shared.display_title("Optimized","en cours")
    start_time = shared.horodatage()
    actions = []
    anomalies = []
    
    # Lecture du CSV et remplissage de l'array actions
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            price = float(row['price'])
            profit_value = float(row['profit'])
            
            if config.LOGS:
                if price <= 0 or profit_value <= 0:
                    anomalies.append({
                        'id': name,
                        'cost': price,
                        'profit': profit_value
                    })
            
            # Ajouter à la liste seulement les données normales
            if price > 0 and profit_value > 0:
                profit_multiplier = profit_value / 100
                if profit_multiplier > config.THRESHOLD:
                    actions.append({
                        'id': name,
                        'cost': price,
                        'profit': profit_multiplier
                    })
    
    sorted_all_actions = sorted(actions, key=lambda action: action['profit'], reverse=True)
    if len(sorted_all_actions) > config.MAX_ACTIONS:
        sorted_actions = sorted_all_actions[:config.MAX_ACTIONS]
    else:
        sorted_actions = sorted_all_actions
    
    n_actions = len(sorted_actions)
    total_combinations, estimated_time, formatted_time = shared.work_estimation(n_actions)
    
    if estimated_time > 1:
        print_stuff(f'{n_actions} actions, soit {total_combinations} combinaisons à traiter...')
        print_stuff(f'Temps necessaire estimé : ~{formatted_time}')
    
    choice = "y"
    if estimated_time > 30:
        choice = input("Êtes vous sûr de vouloir continuer ? ")
    
    if choice in ["y", "o", "yes", "oui"]:
        combinations = shared.combinations_library(sorted_actions)
        if config.LOGS:
            shared.start_logging(config.LOGFILE)
        
        end_time = shared.horodatage()
        shared.display_title("Optimized","terminé")
        print_stuff(f'Sur {total_combinations} combinaisons, {total_combinations - len(combinations)} ont été ignorées avec le filtre "BUDGET MAX : {config.MAX_BUDGET}"')
        
        shared.print_stuff_results(combinations, anomalies, formatted_time, start_time, end_time)
        if config.LOGS:
            shared.stop_logging()
            print_stuff(f'Fichier {config.LOGFILE} exporté.')
    
    else:
        print_stuff(f'Process annulé.')
    
    input("Appuyez sur 'entrer' pour retourner au menu précédent.")
