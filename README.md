# OC_06_JustStreamIt  :movie_camera:  
  
# ● Description du projet  
Site web JustStreamIt affichant les meilleurs films d'une bdd en passant par une api. Il permet de générer un affichage clair et intuitif des films les mieux notés. En plus d'une premiere grille des meilleurs films, le site propose deux autres grilles de rangement par genre et une quatrieme grille à choix libre. Le site interroge une API qui va chercher dans une base de données de films les éléments requis pour la construction et l'affichage de la page web. La page générée est responsive mobile + tablette + desktop et utilise vanilla css + vanilla javascript.  
  
Le projet répond à ce cahier des charges :  
https://s3.eu-west-1.amazonaws.com/course.oc-static.com/projects/Python+FR/P6+-+D%C3%A9velopper+une+interface+utilisateur+pour+une+application+web+Python/Cahier+des+charges+%E2%80%93+JustStreamIt.pdf  
Et respecte la maquette :  
https://www.figma.com/design/6KzVM5R2pOBX637RcVWjJ7/Maquettes-JustStreamIt?node-id=0-1  
  
# ● Comment installer et démarrer l'application  
1. Prérequis :  
    Avoir Python 3 installé  
    Avoir téléchargé et installé l'API :  
    git clone https://github.com/OpenClassrooms-Student-Center/OCMovies-API-EN-FR "local\folder"  
    Avoir téléchargé et dézipé l'archive du projet sur votre disque dur,  
    Ou clonez le repo avec cette commande :  
  ```  
  git clone https://github.com/SachaaBoris/OC_06_JustStreamIt.git "local\folder"  
  ```  
  
2. Installer l'environnement virtuel :  
    Depuis votre console favorite, naviguez jusqu'au repertoire de l'API  
    Pour créer l'environnement virtuel rentrez la ligne de commande : `py -m venv ./venv`  
    Activez ensuite l'environnement virtuel en rentrant la commande : `venv\Scripts\activate`  
    Installer les requirements du projet avec la commande : `py -m pip install -r requirements.txt`  
	Créez la bdd locale avec la commande : `py manage.py create_db`  
  
3. Démarrer le serveur :  
    Toujours dans la console et à la racine de l'API, lancez un serveur avec la commande : `py manage.py runserver`  
  
4. Se connecter au site web :  
	Ouvrez just_stream_it.html avec votre browser préféré.  
	Ou tappez l'url : file:///C:/chemin_vers_le_fichier/just_stream_it.html  
  
---  
  
[![CC BY 4.0][cc-by-shield]][cc-by]  
  
This work is licensed under a [Creative Commons Attribution 4.0 International License][cc-by].  
  
[cc-by]: http://creativecommons.org/licenses/by/4.0/  
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg  
