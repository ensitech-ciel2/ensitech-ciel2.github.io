# Les principales menaces réseau

**Matière :** Informatique — **Module :** E6 (protection des données et des accès)
**Dernière mise à jour :** 18/09/2026
**Statut :** fichier évolutif — à compléter à chaque nouveau cours de cybersécurité

---

## 1. Pourquoi cartographier les menaces ?

Avant de savoir se défendre (pare-feu, proxy filtrant, politique de mots de passe...), un technicien doit savoir **nommer et classer** les menaces auxquelles un réseau est exposé : c'est ce panorama qui justifie ensuite chaque mesure de protection mise en place (voir par exemple le [[TP-pfSense-SquidGuard-Proxy-Filtrant|TP pfSense/SquidGuard]], qui répond directement au risque de navigation non contrôlée).

## 2. Tableau des menaces principales

| Menace | Description | Vecteur typique | Impact potentiel |
|---|---|---|---|
| Malware / Ransomware | Logiciel malveillant chiffrant les données de la victime | Pièce jointe email / lien piégé | Perte de données / rançon exigée |
| Phishing | Usurpation d'identité pour voler des identifiants (credentials) | Email frauduleux / faux site web | Vol de comptes / fuite de données |
| DDoS | Saturation d'un service par un flux massif de requêtes | Botnet coordonné | Indisponibilité du service |
| Sniffing réseau | Interception du trafic non chiffré | Accès physique ou Wi-Fi non sécurisé | Vol de mots de passe / données sensibles |
| Intrusion (scan de ports) | Exploration des ports ouverts pour trouver des failles | Outils nmap / metasploit | Prise de contrôle du système |
| Point d'accès Wi-Fi rogue | Faux AP imitant un réseau légitime | Wi-Fi public | Attaque man-in-the-middle |
| Attaque par force brute | Tentatives de connexion répétées jusqu'à trouver le bon mot de passe | SSH / RDP / interface web | Compromission d'un compte admin |

*Source citée en cours : ANSSI — Panorama de la cybermenace 2023. Les ransomwares sont la menace n°1 en France depuis 2020.*

## 3. Pour aller plus loin sur chaque menace

- **Ransomware** : la meilleure protection reste la sauvegarde régulière et **déconnectée** du réseau (un ransomware chiffre aussi les sauvegardes accessibles en ligne) — payer la rançon n'offre jamais de garantie de récupération.
- **Phishing** : repose sur l'erreur humaine plutôt que sur une faille technique — la sensibilisation des utilisateurs est donc au moins aussi importante que les outils de filtrage d'email.
- **DDoS** : un botnet est un réseau de machines compromises (souvent à l'insu de leurs propriétaires) contrôlées à distance pour mener l'attaque en masse.
- **Sniffing** : c'est l'argument technique derrière l'obligation de chiffrer les échanges (HTTPS plutôt que HTTP, WPA2/WPA3 plutôt qu'un Wi-Fi ouvert — voir le [[Wifi-802-11|cours sur le Wi-Fi]]).
- **Scan de ports** : un port ouvert n'est pas une faille en soi, mais chaque service exposé est une surface d'attaque supplémentaire — d'où le principe de fermer tout port/service non strictement nécessaire.
- **AP rogue** : un utilisateur qui se connecte sans vérifier peut transmettre tout son trafic (y compris ses mots de passe) à un attaquant qui se fait passer pour le réseau légitime — d'où l'importance de vérifier le SSID et le certificat avant de se connecter à un réseau public.
- **Force brute** : se contre par une politique de verrouillage de compte après N tentatives, l'authentification à plusieurs facteurs (MFA), et l'interdiction des mots de passe par défaut.

## 4. Lexique

| Terme | Définition |
|---|---|
| Ransomware | Malware qui chiffre les données puis exige une rançon pour les déchiffrer |
| Phishing | Technique d'ingénierie sociale visant à voler des identifiants |
| Botnet | Réseau de machines compromises contrôlées à distance |
| MITM (Man-in-the-middle) | Attaque où l'attaquant s'interpose entre deux parties communicantes |
| MFA | Authentification multi-facteurs (mot de passe + second facteur) |
