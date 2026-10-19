# SysML — Langage de modélisation de systèmes

**Matière :** Informatique — **Module :** E4 (conception)
**Dernière mise à jour :** 25/09/2026
**Statut :** fichier évolutif
**Contexte :** SysML et un diagramme de GANTT sont obligatoires dans tous les projets de BTS (voir aussi [[Vie-de-la-formation-Alternance|rapport d'alternance]]).

---

## 1. Qu'est-ce que SysML ?

**SysML** (*SYStems Modeling Language*, Langage de Modélisation de Systèmes) est un outil permettant de représenter des objets techniques sous forme de schémas normalisés, appelés **diagrammes**. C'est un langage "de technicien" : son intérêt est de permettre à des personnes différentes (chef de projet, développeur, client...) de décrire et de comprendre le même système de la même façon, sans ambiguïté — un peu comme un plan d'architecte standardisé, compréhensible par n'importe quel professionnel du bâtiment.

## 2. Les principaux diagrammes SysML

| Diagramme | Ce qu'il représente |
|---|---|
| Diagramme des exigences (*requirement diagram*) | Le cahier des charges fonctionnel du système : "le système doit...". Reprend les exigences du CdCF (Cahier des Charges Fonctionnel). |
| Diagramme des cas d'utilisation | Les services offerts par l'objet à ses utilisateurs (acteurs) : décrit **ce que fait** l'objet du point de vue de l'utilisateur, mais jamais **comment** il le fait. |
| Diagramme de définition de bloc | La liste de tous les blocs et sous-blocs qui composent l'objet — une sorte d'inventaire structuré des composants. |
| Diagramme de contexte | Les éléments extérieurs (acteurs) qui interagissent avec l'objet — ce qui est "autour" du système. |
| Diagramme des blocs internes | Comment l'information, l'énergie et la matière **circulent** à travers l'objet, entre ses différents blocs internes. |
| Diagramme d'activité | Le comportement de l'objet, sous forme d'enchaînement d'actions et de décisions (choix d'action selon une condition). |
| Diagramme de séquence | L'enchaînement chronologique des échanges entre les différents éléments du système. |
| Diagramme d'états (*state machine diagram*) | Les différents états possibles du système et les événements qui font passer de l'un à l'autre. |

**Point méthodologique à retenir :** ces diagrammes ne sont pas redondants entre eux — chacun répond à une question différente (*quoi* pour les exigences, *qui interagit* pour le contexte, *comment ça circule* pour les blocs internes, *dans quel ordre* pour la séquence/l'activité). Un dossier de projet complet combine généralement plusieurs de ces diagrammes, chacun éclairant un aspect différent du même système.

## 3. Une précision importante : qu'est-ce qu'une API ?

> **Note de Claude :** le brouillon contenait une définition erronée de l'API (« l'interface personnelle, l'IHM, accessible de partout »). Il est important de corriger ce point, car API et IHM sont deux notions bien distinctes en informatique.

Une **API** (*Application Programming Interface*, interface de programmation applicative) est un ensemble de règles et de points d'accès qui permet à **deux programmes** (et non deux humains) de communiquer entre eux — par exemple, une application mobile qui interroge un serveur pour récupérer des données, ou un objet connecté (Arduino) qui envoie ses mesures à un serveur via des requêtes HTTP (voir le [[TP-Arduino-NodeJS-IoT|TP Arduino/Node.js]], qui met en œuvre exactement ce principe).

Une **IHM** (Interface Homme-Machine) est, à l'inverse, ce avec quoi un **humain** interagit directement : un écran, des boutons, une page web visuelle. Une application peut très bien avoir une IHM (l'écran que voit l'utilisateur) **et** exposer une API en parallèle (par laquelle d'autres programmes viennent chercher des données), ce sont deux couches différentes du même système, pas deux noms pour la même chose.
