# Virtualisation — Serveurs ESXi de la classe (Hyper1 et Hyper2)

**Matière :** Informatique — **Modules :** E4 (installation/configuration), E5 (exploitation)
**Dernière mise à jour :** 09/10/2026
**Statut :** fichier évolutif — à compléter au fil des TP sur ces serveurs

---

## 1. Contexte : deux serveurs pour les projets de la classe

La classe dispose d'un **accès total à deux serveurs** physiques, pour y déployer des **projets** et des **machines virtuelles (VM)**. Le second serveur permet aussi d'avoir des **sauvegardes** « en cas de pépin ».

| Serveur | Modèle | Nom dans le TP |
|---|---|---|
| Serveur 1 | Dell R640 | **Hyper1** |
| Serveur 2 | Dell R620 | **Hyper2** |

> **Note de Claude :** dans le brouillon, ce tableau portait les en-têtes « Hyperviseur de type 1 » et « Hyperviseur de type 2 ». Il s'agit probablement d'une confusion avec les noms « Hyper1 » et « Hyper2 » : les deux serveurs utilisent **ESXi**, qui est un hyperviseur de **type 1** (installé directement sur le matériel, sans système d'exploitation hôte). Hyper1 et Hyper2 sont simplement deux serveurs différents, pas deux types d'hyperviseur.

**Rappel — types d'hyperviseurs :**
- **Type 1** (*bare metal*) : s'installe directement sur le matériel (ex. VMware ESXi, Proxmox). C'est le choix des serveurs de production.
- **Type 2** : s'installe *dans* un système d'exploitation existant (ex. VMware Workstation, VirtualBox). Utilisé pour les tests (c'est le cas du [[TP-pfSense-SquidGuard-Proxy-Filtrant|TP pfSense]]).

## 2. Organisation prévue

**Exemple donné en cours :** sur Hyper1, un étudiant (Rudy) a une **base de données**, un **Debian 13**, un **Windows 10** et un **pfSense** : cela fait **4 VM**. Si, pour une raison ou une autre, sa base de données sur Hyper1 ne fonctionne plus, il peut aller récupérer celle d'**Hyper2**, qui sert de **sauvegarde**. *(Voir le cours [[SQL-Bases-de-donnees]] pour la partie base de données.)*

- Quand un utilisateur utilise plusieurs machines, on parle d'un **« groupe de machines »**.
- **À terme**, les deux serveurs contiendront les **mêmes données**.
- **Pour l'instant**, la classe est divisée en **deux groupes**, et chaque groupe utilise **un serveur**.

## 3. Gestion des comptes

- À partir du compte **root**, on crée ses **propres utilisateurs** (tous administrateurs).
- Il ne faut **surtout pas supprimer le compte root** : c'est la **porte de secours** en cas d'oubli de mots de passe (on parle de compte « de dernier recours »).

**Pourquoi des comptes individuels ?** Avec un compte par personne, on sait **qui a fait quoi** (traçabilité) et on peut retirer l'accès d'une personne sans changer le mot de passe de tout le monde. Le compte root, partagé, ne devrait servir qu'en urgence.

> **Note de Claude :** le brouillon contient le mot de passe root du serveur d'exercice, donné en cours. Je ne l'ai **volontairement pas recopié** dans ce cours : un mot de passe n'a pas sa place dans un document de cours, même pour un serveur de TP. Garde-le dans ton brouillon d'origine, ou mieux, dans un gestionnaire de mots de passe. (Bonne pratique E6 : un mot de passe partagé et distribué en clair est à changer dès que possible.)

## 4. Se connecter et créer son utilisateur (ESXi Host Client)

Le serveur Hyper1 répond à l'adresse IP **172.22.89.101**. Le serveur est administré avec l'interface web **ESXi Host Client** (on l'ouvre dans un navigateur à l'adresse du serveur).

**Étape 1 — Créer son compte :**
1. Se connecter avec le compte root.
2. Aller dans **Gérer → Sécurité et Utilisateurs → Utilisateurs**.
3. Cliquer sur **« Ajouter un utilisateur »**.

**Étape 2 — Lui donner les droits :**
1. Aller dans **Host → Actions → Autorisations**.
2. Choisir son nom d'utilisateur et l'ajouter avec le rôle **Administrateur**.
3. Se **déconnecter**, puis se **reconnecter avec sa propre session**.

## 5. Déposer les images ISO dans le « dépôt »

Pour créer des VM, il faut d'abord récupérer les **images d'installation (ISO)** et les déposer dans le **dépôt** du serveur (en vocabulaire VMware : la **banque de données**, ou *datastore*, l'espace de stockage du serveur).

Procédure notée en cours : **Stockage → Banque de données →** créer une banque de données au **nom de la machine** (ex. `Debian13`), puis y **ajouter l'ISO**. Le téléchargement de l'ISO est assez long.

> **Note de Claude :** dans ESXi, une banque de données correspond normalement à un espace de stockage (un disque ou un volume) dans lequel on crée des **dossiers** et on envoie les fichiers (ISO...) via l'explorateur de banque de données. Le brouillon décrit la création d'une banque de données « au nom de la machine » : il s'agit peut-être plutôt d'un dossier à ce nom dans la banque de données. À vérifier lors du prochain TP.

## 6. Créer et installer les VM

- On crée les VM sur le serveur : **une VM par étudiant et par machine**.
- Une fois toutes les VM créées, on peut les **configurer en les lançant**.
- On commence par **Debian 13** avec la **« Graphic Install »** : on renseigne le **nom de la machine**, le **mot de passe root**, le **compte utilisateur**, etc.

## 7. Accès depuis un poste et licence

- **Depuis un poste Linux (« workstation »)** : *Fichiers → Connect to server →* adresse du serveur (`172.22.89.101`). *(Le brouillon ne précise pas ce que l'on y consulte ; probablement les fichiers du serveur, comme le dépôt d'ISO.)*
- **Licence ESXi** : récupérer une clé sur **GitHub**, puis **Gérer → Attribut de licence → Attribuer une licence**, et saisir la clé.

## 8. À compléter

- Création pas à pas d'une VM (ressources, réseau, ISO).
- Configuration réseau des VM, puis déploiement des autres machines (Windows 10, pfSense, base de données).
- Mise en place de la sauvegarde entre Hyper1 et Hyper2.

## 9. Lexique

| Terme | Définition |
|---|---|
| Hyperviseur | Logiciel qui permet de faire tourner plusieurs machines virtuelles sur un même serveur |
| ESXi | Hyperviseur de type 1 de VMware |
| VM | Machine virtuelle : un ordinateur simulé par logiciel |
| ISO | Image d'un disque d'installation |
| Banque de données (datastore) | Espace de stockage du serveur ESXi |
| Root | Compte administrateur principal, à réserver aux urgences |
