from modules import bruteforce
from modules import optimized
import traceback
import os
import random
import config


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    config.CONSOLE_CONTENT = ''

def print_stuff(stuff):
    print(f'{stuff}')
    config.CONSOLE_CONTENT += str(stuff) + '\n'

def option_input(type):
    while True:
        new_value = input(f'Nouveau {type} : ')
        if type in ["Budget", "Actions"]:
            try:
                new_value = int(new_value)
                if new_value > 0:
                    break
                else:
                    print_stuff("Veuillez entrer un nombre entier positif.")
            
            except ValueError:
                print_stuff("Veuillez entrer un nombre entier positif.")
        else:
            try:
                new_value = float(new_value)
                if new_value > 0:
                    break
                else:
                    print_stuff("Veuillez entrer un nombre positif.")
            
            except ValueError:
                print_stuff("Veuillez entrer un nombre positif.")
    
    return new_value

def print_stuff_shared_menu(type):
    clear_screen()
    print_stuff("\nAlgoInvest&Trade")
    print_stuff("Optimisation d'achat d'actions")
    print_stuff(f'\n{type} Menu :')
    print_stuff("1. Dataset 0")
    print_stuff("2. Dataset 1")
    print_stuff("3. Dataset 2")
    print_stuff(f'4. Edit Max Actions ({config.MAX_ACTIONS})')
    print_stuff(f'5. Edit Max Budget ({config.MAX_BUDGET}€)')

def bruteforce_menu():
    wrong_choice = False
    while True:
        print_stuff_shared_menu("Bruteforce")
        print_stuff("6. Return to previous menu")
        
        if wrong_choice:
            wrong_choice = False
            choice = input("Choix invalide. Choisissez une option valide [1-X] : ")
        else:
            choice = input("Votre choix : ")

        if choice == "1":
            file_path = "data/dataset0_Python+P7.csv"
            bruteforce.get_best_combinations(file_path)
        elif choice == "2":
            file_path = "data/dataset1_Python+P7.csv"
            bruteforce.get_best_combinations(file_path)
        elif choice == "3":
            file_path = "data/dataset2_Python+P7.csv"
            bruteforce.get_best_combinations(file_path)
        elif choice == "4":
            new_value = option_input("Actions")
            config.MAX_ACTIONS = new_value
        elif choice == "5":
            new_value = option_input("Budget")
            config.MAX_BUDGET = new_value
        elif choice == "6":
            break
        else:
            wrong_choice = True
    
def optimized_menu():
    wrong_choice = False
    while True:
        print_stuff_shared_menu("Optimized")
        print_stuff(f'6. Edit Profit Threshold ({config.THRESHOLD * 100} %)')
        print_stuff("7. Return to previous menu")
        
        if wrong_choice:
            wrong_choice = False
            choice = input("Choix invalide. Choisissez une option valide [1-X] : ")
        else:
            choice = input("Votre choix : ")
        
        if choice == "1":
            file_path = "data/dataset0_Python+P7.csv"
            optimized.get_best_combinations(file_path)
        elif choice == "2":
            file_path = "data/dataset1_Python+P7.csv"
            optimized.get_best_combinations(file_path)
        elif choice == "3":
            file_path = "data/dataset2_Python+P7.csv"
            optimized.get_best_combinations(file_path)
        elif choice == "4":
            new_value = option_input("Actions")
            config.MAX_ACTIONS = new_value
        elif choice == "5":
            new_value = option_input("Budget")
            config.MAX_BUDGET = new_value
        elif choice == "6":
            new_value = option_input("Threshold")
            config.THRESHOLD = new_value / 100        
        elif choice == "7":
            break
        else:
            wrong_choice = True

def main():   
    wrong_choice = False
    while True:
        clear_screen()
        print_stuff("\nAlgoInvest&Trade")
        print_stuff("Optimisation d'achat d'actions")
        print_stuff("\nMain Menu :")
        print_stuff("1. Bruteforce")
        print_stuff("2. Optimized")
        if config.LOGS:
            print_stuff("3. Deactivate Logs")
        else:
            print_stuff("3. Activate Logs")
        print_stuff(f'4. Console theme ({config.FAVORITE_COLOR})')
        print_stuff("5. Quitter")
        
        if wrong_choice:
            wrong_choice = False
            choice = input("Choix invalide. Choisissez une option valide [1-X] : ")
        else:
            choice = input("Votre choix : ")

        if choice == "1":
            bruteforce_menu()
        elif choice == "2":
            optimized_menu()
        elif choice == "3":
            config.LOGS = not config.LOGS
        elif choice == "4":
            backgrounds = ['0', '8', '1', '3']
            foregrounds = ['4','5','6','7','9','a','b','c','d','e','f']
            config.FAVORITE_COLOR = random.choice(backgrounds) + random.choice(foregrounds)
            cmd = f'color {config.FAVORITE_COLOR}'
            os.system(cmd)
        elif choice == "5":
            break
        else:
            wrong_choice = True


if __name__ == '__main__':

    try:
        cmd = 'mode 130,35'
        os.system(cmd)
        cmd = f'color {config.FAVORITE_COLOR}'
        os.system(cmd)
        main()
    
    except Exception as e:
        print_stuff("Une erreur est survenue:")
        traceback.print_exc()
