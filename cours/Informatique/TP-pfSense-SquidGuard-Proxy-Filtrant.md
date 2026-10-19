# TP — Proxy filtrant avec pfSense, Squid et SquidGuard

**Matière :** Informatique — **Modules :** E4 (installation/config), E5 (exploitation), E6 (protection des accès)
**Dernière mise à jour :** 18/09/2026
**Statut :** fichier évolutif — à compléter au fil du TP

---

## 1. Contexte et objectif du TP

L'objectif est de mettre en place un **proxy filtrant** capable de bloquer l'accès à certaines catégories de sites (réseaux sociaux) ainsi qu'à un site nommément désigné (tf1.fr et ses alias), pour un poste client donné. Ce TP illustre concrètement la réponse à une menace du quotidien en entreprise : l'usage non maîtrisé d'Internet par les collaborateurs (temps perdu, fuite de données, exposition à des sites malveillants — voir le [[Menaces-Reseau-Cybersecurite|cours sur les menaces réseau]]).

**Poste client :** prévu à l'origine sous Windows 11, remplacé en pratique par une VM Debian 13 déjà installée.

## 2. Les briques techniques et leur rôle

### 2.1 pfSense — le pare-feu

**pfSense** est un système d'exploitation de pare-feu/routeur open source, basé sur **FreeBSD** (une famille de systèmes de type Linux/Unix). Il s'installe comme n'importe quel OS, dans une VM dédiée.

> Rappel important : un **hyperviseur de type 2** s'installe *dans* un système d'exploitation hôte (ex. VMware Workstation sur Windows) ; un **hyperviseur de type 1** s'installe directement sur le matériel, sans OS hôte. Le TP utilise ici un hyperviseur de type 2.

**Configuration VM pour l'installation de pfSense (via VMware) :**
- 2 Go de RAM
- 20 Go de disque dur
- **2 interfaces réseau** (une pour le WAN, une pour le LAN — un pare-feu doit toujours avoir au moins deux interfaces pour pouvoir filtrer le trafic *entre* deux réseaux)

### 2.2 Le principe de la DMZ

Dans une architecture d'entreprise typique, le serveur web accessible depuis Internet est placé dans une **DMZ** (zone démilitarisée) : un segment réseau isolé, situé de l'autre côté du pare-feu par rapport au réseau interne. Le principe : si le serveur exposé sur Internet est compromis, l'attaquant se retrouve dans la DMZ, pas directement dans le réseau interne de l'entreprise. Les switchs des serveurs suivent la même logique (de l'autre côté du firewall), tandis que les postes/switchs des utilisateurs internes restent de notre côté du firewall, protégés.

### 2.3 SquidGuard — le filtrage applicatif

**Squid** est un serveur **proxy** : il s'intercale entre les postes clients et Internet, et relaie leurs requêtes web. **SquidGuard** est un module additionnel de Squid qui permet d'**autoriser ou d'interdire** l'accès à des sites ou catégories de sites, un peu comme un pare-feu, mais au niveau applicatif (URL/nom de domaine) plutôt qu'au niveau réseau (IP/port).

## 3. Architecture réseau retenue

- **LAN pfSense** : `192.168.1.1/24`
- **DHCP** : plage `192.168.1.100` à `192.168.1.200`
- **WAN** : en mode NAT côté VMware
- **LAN** : en mode **LAN Segment** côté VMware (et non *Host-only*) — ce choix évite un conflit avec le DHCP interne propre à VMware, qui aurait pu distribuer des adresses en parallèle du DHCP pfSense sur le même segment.

## 4. Contraintes imposées par l'énoncé du TP

- **SSL/MITM Mode = Splice All** (obligatoire) : ce mode ne déchiffre pas le trafic HTTPS lui-même, contrairement à un mode d'interception complet — utile ici car l'objectif est de filtrer par nom de domaine, pas d'inspecter le contenu chiffré.
- **SSL Proxy Port = 3129**, qui doit correspondre à la règle NAT automatique redirigeant le LAN (port 443) vers `127.0.0.1:3129`.
- **CA Squid** nommée `pfsense-squidCA` (autorité de certification utilisée par Squid pour l'interception SSL).

## 5. Règles de filtrage à mettre en œuvre

- **Blocage des réseaux sociaux** via la liste de catégories **UT1** (une liste de blacklists de catégories de sites, largement utilisée avec SquidGuard).
- **Blocage personnalisé** de `tf1.fr` et de ses alias (autres domaines redirigeant vers le même site).

## 6. Bug rencontré et résolution

Le champ **SSL Proxy Port** avait été réglé par erreur sur **3029** au lieu de **3129**. Conséquence : toute tentative de connexion HTTPS transparente échouait (un test `nc` vers ce port restait en *timeout*, signe que rien n'écoutait sur ce port). La résolution consiste à corriger le port pour qu'il corresponde exactement à celui attendu par la règle NAT automatique (3129, cf. §4).

> **Retour d'expérience à retenir :** en cas de blocage réseau "silencieux" (rien ne se passe, pas de message d'erreur explicite), tester la connectivité brute avec un outil comme `nc` (netcat) sur le port concerné permet souvent d'isoler rapidement si le problème vient du service lui-même (port fermé/mal configuré) ou d'une étape plus en amont (règle de pare-feu, routage...).

## 7. À compléter

- Étapes détaillées de configuration de SquidGuard une fois pfSense/Squid installés.
- Tests de validation (accès refusé aux réseaux sociaux et à tf1.fr, accès normal au reste d'Internet).

---

## 8. Lexique

| Terme | Définition |
|---|---|
| pfSense | Distribution pare-feu/routeur open source basée sur FreeBSD |
| DMZ | Zone réseau isolée entre Internet et le réseau interne, hébergeant les services exposés |
| Proxy | Serveur intermédiaire relayant les requêtes entre client et Internet |
| SquidGuard | Module de filtrage d'URL/catégories pour le proxy Squid |
| SSL/MITM Splice | Mode d'interception HTTPS sans déchiffrement du contenu |
