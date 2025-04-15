#Projet-DevWeb-IOT

Le but de ce projet est de développer une plateforme numérique intelligente qui regroupe divers services/fonctionnalités pour les utilisateurs dans le cadre d'une maison intélligente. 

## Pré-requis
    - SE : Distribuitions Linux (Ubuntu, Debian, Manjaro, etc);
## Lacement du projet
    - `git clone git@github.com:FelipeZani/Projet-DevWeb-IOT.git`
    - `bash rac.sh`

##Contenu rac.sh
```
#!/bin/bash
if [ ! -d 'venv' ]
then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi
python3 app.py
```
## Parties Manquantes du cahier de charge
Contrôler l'état d'un objet (activer/désactiver, mettre à jour);

Configurer les paramètres d'utilisation des objets connectés (par ex. température cible pour un thermostat, horaire de fonctionnement pour une lumière);

Identifier les objets inefficaces (selon les paramètres d'utilisation) ou nécessitant une maintenance. (prendre objets random et les mettre dans le rapport);

Définir les règles de fonctionnement globales des objets et des outils/services (par exemple, priorités énergétiques, gestion des alertes, etc.);

