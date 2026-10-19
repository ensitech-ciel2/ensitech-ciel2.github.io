# GLPI — Cours

**Matière :** Informatique — **Modules :** E4 (installation/configuration), E5 (exploitation)
**Dernière mise à jour :** 04/09/2026
**Statut :** fichier évolutif — à compléter à chaque nouveau cours/TP sur GLPI

---

## 1. Qu'est-ce que GLPI et pourquoi l'utiliser ?

**GLPI** (Gestion Libre de Parc Informatique) est un logiciel open source de **gestion de parc informatique et de helpdesk (assistance)**. Dans une entreprise, il répond à deux besoins qui vont toujours de pair :

1. **Inventorier** ce que possède l'entreprise (ordinateurs, imprimantes, logiciels, licences, contrats de maintenance...) — c'est la partie *gestion de parc*.
2. **Suivre les incidents et demandes** des utilisateurs (« mon PC ne démarre plus », « j'ai besoin d'un nouvel accès ») — c'est la partie *helpdesk*, organisée autour du concept de **ticket**.

C'est cette double casquette qui explique pourquoi GLPI touche à la fois l'E4 (le déployer, le configurer) et l'E5 (l'exploiter au quotidien) : c'est un même outil, mais deux métiers différents — celui qui l'installe n'est pas forcément celui qui l'utilise tous les jours pour traiter des tickets.

---

## 2. Installation de GLPI (E4)

### 2.1 Pourquoi Docker ?

GLPI a besoin, pour fonctionner, d'un serveur web, d'un interpréteur PHP et d'une base de données (MariaDB/MySQL). Plutôt que d'installer chacun de ces composants séparément (et de gérer leurs versions, leurs dépendances, leurs conflits), on utilise **Docker** : chaque composant tourne dans son propre conteneur isolé, déjà préconfiguré pour fonctionner avec les autres. Un fichier `docker-compose.yml` décrit l'ensemble de ces conteneurs et permet de tous les démarrer d'une seule commande — une architecture **multi-conteneurs orchestrée**.

Pour héberger Docker sous Windows, on passe par **WSL** (Windows Subsystem for Linux), qui permet de faire tourner un vrai noyau Linux (ici Ubuntu 24.04) directement depuis Windows, sans machine virtuelle complète.

### 2.2 Procédure d'installation

**Étape 1 — Préparer l'environnement WSL.** En cas de souci (ex. mot de passe oublié sur la distribution), on peut repartir de zéro :
```powershell
wsl --unregister -d Ubuntu-24.04
wsl --install -d Ubuntu-24.04
```
`--unregister` désinscrit et supprime la distribution ; `--install` la retélécharge et la réinstalle proprement.

**Étape 2 — Récupérer et lancer le fichier docker-compose.**
```bash
mkdir glpi-docker
# placer le fichier docker-compose fourni dans ce dossier
cd glpi-docker
docker compose up -d
```
Le flag `-d` (*detached*) lance les conteneurs en arrière-plan.

### 2.3 Comprendre et résoudre les erreurs classiques

**a) Une dépendance manque sur l'hôte.** MariaDB n'était pas installé sur la machine WSL, alors que le conteneur GLPI s'attend à pouvoir s'y connecter :
```bash
sudo apt install mariadb-server
```

**b) L'utilisateur n'a pas les droits d'exécuter Docker.** Sous Linux, l'accès au démon Docker est réservé aux membres du groupe système `docker` :
```bash
sudo usermod -aG docker $USER
```
L'appartenance à un groupe Linux est lue **à l'ouverture de la session**, pas en temps réel. Sous WSL, la manière fiable de "fermer la session" est d'arrêter complètement la machine virtuelle Linux sous-jacente :
```powershell
wsl --shutdown
```
puis de relancer Ubuntu.

### 2.4 Vérifier que tout est en ordre

```bash
groups              # liste les groupes de l'utilisateur courant
getent group docker  # affiche les membres du groupe "docker"
```

> **Note de Claude :** le brouillon original mentionnait la commande `wsh --install` — vraisemblablement une coquille pour `wsl --install`, corrigée ci-dessus.

---

## 3. Exploitation de GLPI — le cycle de vie d'un ticket (E5)

### 3.1 Le principe général du helpdesk

```
Signalement → Prise en charge → Traitement (suivis/tâches) → Escalade éventuelle → Résolution → Clôture
```

Comprendre ce cycle est plus important que de mémoriser les clics GLPI : c'est ce schéma qui structure le métier de technicien support, quel que soit l'outil utilisé.

### 3.2 Les briques de configuration préalables

Avant d'exploiter GLPI efficacement, un administrateur (E4) doit avoir configuré des **utilisateurs**, des **groupes d'assistance** (ex. « N1-Helpdesk », « N2-Système ») et des **niveaux de service / SLA**. En tout début de déploiement (comme sur l'instance travaillée en TP, GLPI 11.0.6, 5 utilisateurs), aucun de ces éléments n'est encore configuré — la phase de **paramétrage** précède toujours la phase d'usage.

### 3.3 Les deux façons de créer un ticket

- **Côté utilisateur final** : *Administration → Formulaire → Signaler un incident*.
- **Côté technicien** : *Assistance → Créer un ticket*.

### 3.4 Déroulé complet d'un ticket — étude de cas (profil Outlook corrompu)

1. **Signalement** : Marie MARTIN signale un problème avec son Outlook.
2. **Prise en charge (N1)** : le technicien N1 s'auto-attribue le ticket et ajoute un **suivi** informant l'utilisateur que sa demande est prise en compte.
3. **Diagnostic et action** : profil Outlook recréé, documenté sous forme de **tâche** (durée : 15 minutes).
4. **Escalade (N1 → N2)** : problème lié au serveur Exchange → réaffectation au groupe N2, avec une **note interne** (visible uniquement des techniciens) transmettant les détails techniques.
5. **Résolution (N2)** : redémarrage du service Exchange, clôture du ticket avec description de la solution.

**Distinction clé :** un **suivi** est un message dans l'historique (public ou privé) ; une **tâche** est une action de travail enregistrée avec un temps passé.

### 3.5 Priorité, urgence et impact

La **priorité** croise deux facteurs : l'**urgence** (vitesse de traitement attendue) et l'**impact** (nombre de personnes/services affectés). Un incident très urgent mais à faible impact n'a pas la même priorité qu'un incident moins urgent mais à fort impact.

### 3.6 Les SLA

Un **SLA** fixe un engagement de délai (ex. « résolu sous 4h »), associé à une catégorie de tickets ou d'utilisateurs (ex. un SLA « VIP » pour la direction). Se configure via *Configuration → Niveaux de service → Ajouter*.

### 3.7 Le pilotage via les statistiques

*Assistance → Statistiques* : catégorie la plus fréquente, technicien le plus actif, temps moyen de résolution, taux de satisfaction — des indicateurs qui permettent d'identifier les points de friction récurrents.

---

## 4. Lexique

| Terme | Définition courte |
|---|---|
| Ticket | Unité de suivi d'un incident ou d'une demande |
| Suivi | Message ajouté à l'historique d'un ticket (public ou privé) |
| Tâche | Action de travail enregistrée avec un temps passé |
| SLA | Engagement contractuel de délai de traitement |
| Priorité | Urgence × Impact |
| Escalade | Transfert d'un ticket à un niveau de compétence supérieur |
