# Projet-DevWeb-IOT
Le but de ce projet est de développer une plateforme numérique intelligente qui regroupe divers services/fonctionnalités pour les utilisateurs dans le cadre d'une maison intélligente. 

## Pré-requis
- SE : Distribuitions Linux (Ubuntu, Debian, Manjaro, etc)
## Lacement du projet
    git clone git@github.com:FelipeZani/Projet-DevWeb-IOT.git && bash rac.sh

## Contenu rac.sh
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

