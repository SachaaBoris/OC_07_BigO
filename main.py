from modules import bruteforce
from modules import optimized_greedy
from modules import optimized_dynamic
import traceback
import argparse
import os
import sys
import random
import config


# args must be :
# "bruteforce"/"greedy"/"dynamic"(str), "filepath"(str), max_money(int), log_to_file(bool)

enter_menu_msg = "Appuyez sur entrée pour être rediriger vers le menu."

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
    print_stuff("1. Dataset 1 (20 actions set)")
    print_stuff("2. Dataset 2 (1000 actions set)")
    print_stuff("3. Dataset 3 (1000 actions set)")
    print_stuff(f'4. Edit Max Budget ({config.MAX_BUDGET}€)')
    print_stuff("5. Return to previous menu")


def bruteforce_menu():
    wrong_choice = False
    while True:
        print_stuff_shared_menu("Bruteforce")

        if wrong_choice:
            wrong_choice = False
            choice = input(
                "Choix invalide. Choisissez une option valide [1-X] : ")
        else:
            choice = input("Votre choix : ")

        if choice == "1":
            file_path = "data/dataset1.csv"
        elif choice == "2":
            file_path = "data/dataset2.csv"
        elif choice == "3":
            file_path = "data/dataset3.csv"
        elif choice == "4":
            new_value = option_input("Budget")
            config.MAX_BUDGET = new_value
        elif choice == "5":
            break
        else:
            wrong_choice = True

        if choice in ["1", "2", "3"]:
            bruteforce.get_best_combinations(file_path)


def optimized_menu(type):
    wrong_choice = False
    while True:
        print_stuff_shared_menu("Optimized")

        if wrong_choice:
            wrong_choice = False
            choice = input(
                "Choix invalide. Choisissez une option valide [1-X] : ")
        else:
            choice = input("Votre choix : ")

        if choice == "1":
            file_path = "data/dataset1.csv"
        elif choice == "2":
            file_path = "data/dataset2.csv"
        elif choice == "3":
            file_path = "data/dataset3.csv"
        elif choice == "4":
            new_value = option_input("Budget")
            config.MAX_BUDGET = new_value
        elif choice == "5":
            break
        else:
            wrong_choice = True

        if choice in ["1", "2", "3"]:
            if type == 'optimized':
                optimized_greedy.get_best_combinations(file_path)
            else:
                optimized_dynamic.get_best_combinations(file_path)

def show_help():
    print_stuff("\nAlgoInvest&Trade")
    print_stuff("Optimisation d'achat d'actions, v1.0")
    print_stuff("\nHelp :")
    print_stuff("there are 4 arguments you can use with this script")
    print_stuff('algorithm(str), "filepath"(path), max_money(int), log_to_file(bool)')
    print_stuff("algorithm can be one of : 'bruteforce', 'greedy' or 'dynamic'")
    print_stuff("filepath should be your csv source (make sure it has a name,price,profit head tag)")
    print_stuff("max_money will put a limit to your wallet, default is set to 500€")
    print_stuff("log_to_file, if true, will output the printed results to zz_actions.log")
    print_stuff('example : py main.py "bruteforce" "C:/path/to/file.csv" 500 True')
    print_stuff("\nCopyleft : Sacha Boris, 09/2024")
    printlogo()
    input(f'{enter_menu_msg}')


def main_menu():
    wrong_choice = False
    while True:
        clear_screen()
        print_stuff("\nAlgoInvest&Trade")
        print_stuff("Optimisation d'achat d'actions")
        print_stuff("\nMain Menu :")
        print_stuff("1. Bruteforce")
        print_stuff("2. Optimized (greedy)")
        print_stuff("3. Dynamic (knapsack)")
        if config.LOGS:
            print_stuff("4. Deactivate Logs")
        else:
            print_stuff("4. Activate Logs")
        print_stuff(f'5. Console theme ({config.FAVORITE_COLOR})')
        print_stuff("6. Help")
        print_stuff("7. Quit")

        if wrong_choice:
            wrong_choice = False
            choice = input(
                "Choix invalide. Choisissez une option valide [1-X] : ")
        else:
            choice = input("Votre choix : ")

        if choice == "1":
            bruteforce_menu()
        elif choice == "2":
            optimized_menu('optimized')
        elif choice == "3":
            optimized_menu('dynamic')
        elif choice == "4":
            config.LOGS = not config.LOGS
        elif choice == "5":
            themes = [
                '09', '06', '07', '0b',
                '0f', '0a', '0e', '0c',
                '8e', '87', '3e', '1b', '1f'
                ]
            config.FAVORITE_COLOR = random.choice(themes)
            cmd = f'color {config.FAVORITE_COLOR}'
            os.system(cmd)
        elif choice == "6":
            show_help()
        elif choice == "7":
            break
        else:
            wrong_choice = True


def main():
    if len(sys.argv) != 5:
        print(f'{len(sys.argv)}')
        printlogo()
        print("GUI d'algorithmes d'optimisation d'achat d'actions :")
        input(f'{enter_menu_msg}')
        config.GUI = True
        main_menu()  # Appeler le menu principal
        return

    parser = argparse.ArgumentParser(
        description="Script d'optimisation d'achat d'actions.")
    parser.add_argument('methode', type=str, choices=['bruteforce', 'greedy', 'dynamic'],
                        help="La méthode à utiliser pour l'optimisation.")
    parser.add_argument('filepath', type=str,
                        help="Le chemin vers le fichier CSV contenant les données.")
    parser.add_argument('maxmoney', type=int,
                        help="Le budget maximum pour l'optimisation.")
    parser.add_argument('logtofile', type=bool,
                        help="Activer ou désactiver les logs.")

    try:
        args = parser.parse_args()

        print(f'{args}')
        # Vérifier si le fichier existe
        if not os.path.exists(args.filepath):
            printlogo()
            print("Erreur : Le fichier spécifié n'existe pas.")
            input(f'{enter_menu_msg}')
            config.GUI = True
            main_menu()
            return

        # Convertir les arguments en variables
        config.MAX_BUDGET = args.maxmoney
        config.LOGS = args.logtofile

        # Appeler la méthode appropriée en fonction des arguments
        if args.methode == 'bruteforce':
            config.GUI = False
            bruteforce.get_best_combinations(args.filepath)
        elif args.methode == 'greedy':
            config.GUI = False
            optimized_greedy.get_best_combinations(args.filepath)
        elif args.methode == 'dynamic':
            config.GUI = False
            optimized_dynamic.get_best_combinations(args.filepath)

    except argparse.ArgumentError as e:
        printlogo()
        print(f"Erreur d'argument : {e}")
        input(f'{enter_menu_msg}')
        config.GUI = True
        main_menu()

    except SystemExit:
        # Capture l'erreur provoquée par argparse et redirige vers le menu
        # principal
        printlogo()
        input(f'{enter_menu_msg}')
        config.GUI = True
        main_menu()


def printlogo():
    print("")
    print("                           ,,")
    print("                         ,,,,")
    print("                      ,,,,,,,         .,")
    print("                    .,,,,,,,,      .,,,,")
    print("                    .,,,,,,,,    .,,,,,,")
    print("                    .,,,,,,,,  .,,,,,,,,")
    print("                    .,,,,,,,,  ,,,,,,,,, ,,,,,")
    print("                    .,,,,,,,,  ,,,,,,,,,  .,,,,,")
    print("               ,,,  .,,,,,,,,  ,,,,,,,,,   ,,,,,,")
    print("             ,,,,,  .,,,,,,,,  ,,,,,,,,,    ,,,,,.")
    print("          .,,,,,,,  .,,,,,,,,  ,,,,,,,,,   ,,,,,,")
    print("          ,,,,,,,,  .,,,,,,,,  ,,,,,,,,, .,,,,,,")
    print("      .,. ,,,,,,,,  .,,,,,,,,  ,,,,,,,,,,,,,,,,")
    print("    .,,.  ,,,,,,,,  .,,,,,,,,  ,,,,,,,,,,,,,,")
    print("    ,,.   ,,,,,,,,  .,,,,,,,,  ,,,,,,,,,,,,.")
    print("   ,,,    ,,,,,,,,  .,,,,,,,,  ,,,,,,,,,,")
    print("  ,,,,    ,,,,,,,,  .,,,,,,,,,,,,,,,,,,.")
    print("  ,,,,,   ,,,,,,,,  .,,,,,,,,,,,,,,,.")
    print("   ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
    print("    .,,,,,,,,,,,,,,,,,,,,,,")
    print("         ,,,,,,,,,,, .")
    print("")


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
