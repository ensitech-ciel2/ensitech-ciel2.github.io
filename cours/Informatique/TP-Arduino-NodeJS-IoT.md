# TP — Objet connecté (IoT) avec Arduino, Node.js et une API REST

**Matière :** Informatique — **Modules :** E4 (conception), E5 (mise en œuvre)
**Dernière mise à jour :** 25/09/2026
**Statut :** fichier évolutif — à compléter au fil du TP
**Matériel requis :** un Arduino Wifi R4 (voir [[Vie-de-la-formation-Alternance|rappel d'achat]]).

---

## 1. Architecture générale de la solution

```
Arduino Wifi R4 (capteurs, client HTTP)
        │  Wifi (LAN/Internet, HTTP/HTTPS)
        ▼
Node.js + Express (API REST, port 3000)
        │
        ▼
Base de données (fichier JSON ou SQLite)
```

L'Arduino relève une mesure (ex. température) et l'envoie, via le Wi-Fi, à un petit serveur applicatif qui l'enregistre et la rend consultable — c'est l'architecture de base d'à peu près tout objet connecté grand public.

## 2. Pourquoi Node.js pour l'IoT ?

- **Modèle non bloquant / événementiel** : Node.js peut gérer des centaines de capteurs simultanément sans avoir besoin de créer un thread dédié pour chacun — chaque requête est traitée dès qu'elle arrive, sans que le serveur reste "bloqué" à attendre la précédente.
- **Écosystème npm** : de nombreuses bibliothèques prêtes à l'emploi existent pour les besoins IoT courants (Express pour le serveur web, MQTT pour la communication capteur/serveur, SQLite pour le stockage, WebSocket pour du temps réel).
- **JSON natif** : JavaScript analyse et génère nativement du JSON, le format d'échange de données quasi universel entre objets connectés et serveurs.

## 3. Les 4 verbes HTTP de REST

Une **API REST** organise ses opérations autour de 4 actions standard, associées chacune à un verbe HTTP :

| Verbe | Action |
|---|---|
| **GET** | Lire une ressource |
| **POST** | Créer / envoyer une nouvelle donnée |
| **PUT** | Modifier une ressource existante |
| **DELETE** | Supprimer une ressource |

## 4. Créer un serveur Express.js

```bash
npm init -y              # initialise le projet (package.json)
npm install express      # installe le framework Express
touch server.js          # crée le fichier principal du serveur
node server.js           # lance le serveur
```

Tout le code du serveur se place dans `server.js`.

## 5. Définir les routes REST du projet

| Route | Verbe | Rôle |
|---|---|---|
| `/api/sensors` | GET | Lire toutes les mesures |
| `/api/sensors/:id` | GET | Lire une mesure précise (par son identifiant) |
| `/api/sensors` | POST | Enregistrer une nouvelle mesure |
| `/api/sensors/:id` | DELETE | Supprimer une mesure |

## 6. Envoyer des données depuis l'Arduino

- **Bibliothèque Wi-Fi** : `WiFiS3.h` (intégrée à l'Arduino Wifi R4).
- **Client HTTP** : `WiFiClient`, combiné à la construction manuelle d'une requête HTTP/1.1.
- **Format de données** : JSON, généré côté Arduino avec la bibliothèque `ArduinoJSON`.
- **Méthode utilisée** : une requête **HTTP POST** envoyée vers le serveur Node.js, contenant la mesure au format JSON.

## 7. Stocker les données côté Node.js

| Solution | Niveau | Caractéristiques |
|---|---|---|
| Fichier JSON | Débutant | Zéro dépendance, très simple à écrire — idéal pour prototyper, mais pas de requêtes complexes possibles et lent dès que le volume de données augmente |
| SQLite | Intermédiaire | Vraie base de données, fichier unique, requêtes SQL possibles |
| MongoDB | Avancé | Base de données NoSQL orientée documents, adaptée à un plus gros volume |

## 8. Tester l'API REST avec curl

```bash
curl http://localhost:3000/api/sensors                # lire toutes les mesures (GET)
curl -X POST http://localhost:3000/api/sensors         # envoyer une nouvelle mesure (POST)
```

## 9. Sécurité de base à prévoir

- **Clé API simple** : protéger les routes sensibles avec une clé secrète transmise dans l'en-tête (header) de la requête.
- **Validation des données reçues** : toujours vérifier la cohérence/le format des données envoyées par l'Arduino avant de les stocker (une mesure aberrante ou malformée ne doit pas planter le serveur).
- **CORS et variables d'environnement** : gérer précisément quelles origines (quels sites/applications) ont le droit d'appeler l'API, et ne jamais coder en dur un secret (clé API, mot de passe) directement dans le code — le placer dans une variable d'environnement.

## 10. Synthèse — ce que ce TP permet de savoir faire

- Créer un serveur Node.js avec Express.
- Définir des routes REST (GET, POST, DELETE...).
- Recevoir et parser du JSON envoyé par un Arduino.
- Stocker ces données (fichier JSON ou SQLite selon le besoin).

## 11. À compléter

- Déroulé pratique du TP (code complet du serveur, câblage/capteur utilisé côté Arduino, résultats obtenus).

---

## 12. Lexique

| Terme | Définition |
|---|---|
| API REST | Interface permettant à deux programmes d'échanger des données via des requêtes HTTP standardisées |
| Endpoint / route | Une URL précise de l'API, associée à une action (ex. `GET /api/sensors`) |
| JSON | Format texte léger d'échange de données structurées |
| Non bloquant (event-driven) | Modèle d'exécution où le serveur ne s'arrête pas d'attendre une opération pour en traiter une autre |
