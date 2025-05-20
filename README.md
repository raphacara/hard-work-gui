# hard-work-gui

### Hard Work GUI

> Simulateur d'application de traitement de données en temps réel, avec interface graphique.

---

### Description

L'application ouvre une fenêtre Tkinter affichant :

* Une file de jobs (30+ tâches) passant par les états **Pending**, **Processing**, **Completed** ou **Failed**
* Un panneau de logs colorés (INFO, WARNING, ERROR) avec export, copie et effacement
* Un onglet **Metrics** affichant en temps réel les graphiques CPU, mémoire et disque via Matplotlib
* Thème **sombre/claire** basculable, filtrage des tâches, contrôle de la vitesse de simulation
* Popups aléatoires pour simuler des alertes système

---

### Fonctionnalités principales

* 🎛️ **Contrôles** : Pause/Resume, réglage de la vitesse
* 🔍 **Recherche** : Filtrer les tâches par nom
* 📊 **Graphiques** : CPU (%), Mémoire (%), Disk IO (%) mis à jour en continu
* 📂 **Logs** : Exporter, copier, vider via le menu Fichier
* 🎨 **Thème** : Mode sombre et clair
* 🖱️ **Détails** : Clic droit sur une tâche pour voir sa durée et son début


### Utilisation

Lancez l'application :

```bash
python3 hard_work_gui.py
```

---

### Contribuer

Les contributions sont bienvenues !

1. Forkez le dépôt.
2. Créez une branche (`git checkout -b feature/ma-amélioration`).
3. Commitez vos changements (`git commit -m "Ajout : ..."`).
4. Poussez et ouvrez une Pull Request.

---

### Licence

MIT © 2025 FakeCorp

---

*Amusez-vous bien à faire tourner l'appli !*
