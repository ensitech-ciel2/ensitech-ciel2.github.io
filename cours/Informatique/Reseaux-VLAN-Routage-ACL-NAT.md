# Réseaux — VLANs, routage inter-VLAN, ACL et NAT

**Matière :** Informatique — **Modules :** E5 (exploitation), E6 (protection des données/accès)
**Dernière mise à jour :** 04/09/2026
**Statut :** fichier évolutif — à compléter à chaque nouveau TP réseau
**Contexte :** TP réalisé sur vrai matériel Cisco (switch + routeur), pas en simulateur.

---

## 1. Pourquoi segmenter un réseau en VLANs ?

Sans segmentation, tous les postes d'une entreprise partagent le même **domaine de diffusion** (broadcast domain) : chaque broadcast (ARP, DHCP...) est reçu par toutes les machines, ce qui devient inefficace à mesure que le réseau grandit, et dangereux car un poste compromis dans un service (ex. accueil) peut alors « voir » et attaquer directement des postes sensibles d'un autre service (ex. direction).

Un **VLAN** (*Virtual LAN*) crée, sur un même switch physique, plusieurs réseaux logiques étanches entre eux au niveau 2 (Ethernet). Deux machines dans deux VLANs différents ne peuvent pas communiquer directement, même branchées sur le même switch — il faut passer par un routeur, avec des règles d'ACL (cf. §4).

**Un switch niveau 2** ne connaît que les VLANs et les adresses MAC ; **un switch niveau 3** ajoute la connaissance des adresses IP et peut router lui-même entre VLANs sans routeur externe. Dans ce TP, le routage est fait par un routeur dédié.

---

## 2. Configuration du switch

### 2.1 Les deux modes d'un port switch

- **Mode access** : le port appartient à un seul VLAN — utilisé pour un poste utilisateur, une imprimante...
- **Mode trunk** : le port transporte le trafic de **plusieurs** VLANs simultanément, en marquant chaque trame avec un tag 802.1Q indiquant son VLAN d'origine.

### 2.2 Créer un VLAN et l'assigner

```
enable
configure terminal
vlan 20
 name RH
exit
```
```
interface range fa0/1-5
 switchport mode access
 switchport access vlan 20
exit
```

### 2.3 Configurer un trunk

```
interface range fa0/1-5
 switchport mode trunk
 switchport trunk allowed vlan 20,30,40
end
```
`switchport trunk allowed vlan` restreint volontairement les VLANs autorisés à traverser ce lien — bonne pratique de sécurité.

### 2.4 Sauvegarder et vérifier

```
copy running-config startup-config     # sauvegarde la config active au démarrage
show interface brief                   # à exécuter en mode enable, PAS en mode config
```
`running-config` est la configuration active (perdue au redémarrage si non sauvegardée) ; `startup-config` est celle chargée au démarrage.

---

## 3. Le routage inter-VLAN (router-on-a-stick)

### 3.1 Principe

La technique du **router-on-a-stick** relie le routeur au switch par un **seul câble en mode trunk**, avec une **sous-interface virtuelle par VLAN** côté routeur (chacune étant un découpage logique de la même interface physique).

```
[Switch]  --- port trunk (VLANs 10/20/30/40) ---  [Routeur]  --- WAN (DHCP) ---  Internet
```

### 3.2 Plan d'adressage utilisé

| VLAN | Nom | Réseau | Passerelle |
|---|---|---|---|
| 10 | Administration | 192.168.10.0/24 | 192.168.10.254 |
| 20 | RH | 192.168.20.0/24 | 192.168.20.254 |
| 30 | DSI | 192.168.30.0/24 | 192.168.30.254 |
| 40 | Secrétariat | 192.168.40.0/24 | 192.168.40.254 |

Convention : la passerelle est systématiquement `.254` (le `.0` identifie le réseau, le `.255` le broadcast).

### 3.3 Configuration des sous-interfaces

```
interface GigabitEthernet0/0/1
 description WAN-INTERNET
 ip address dhcp
 ip nat outside
 no shutdown
exit

interface GigabitEthernet0/0/0.10
 ip nat inside
 ip access-group ACL-VLAN10 in
exit

interface GigabitEthernet0/0/0.20
 ip nat inside
 ip access-group ACL-VLAN20 in
exit

interface GigabitEthernet0/0/0.30
 ip nat inside
 ip access-group ACL-VLAN30 in
exit

interface GigabitEthernet0/0/0.40
 ip nat inside
 ip access-group ACL-VLAN40 in
exit
```
`ip nat inside`/`outside` indiquent de quel côté se trouve le LAN et Internet (rend le NAT possible, §5). `ip access-group ... in` applique une ACL au trafic entrant sur la sous-interface (venant du VLAN vers le routeur).

---

## 4. Les ACL (Access Control Lists)

### 4.1 Principe

Une ACL est une liste ordonnée de règles `permit`/`deny` évaluées **dans l'ordre, jusqu'à la première correspondance** — point le plus important à comprendre : l'ordre des lignes change le résultat. Une ACL se termine toujours par un **deny implicite**, d'où l'ajout fréquent d'un `permit ... any` final explicite.

### 4.2 Cahier des charges du TP

- **VLAN 10** : Internet, communication avec VLAN 20, ping (ICMP) autorisé vers VLAN 30.
- **VLAN 20** : Internet, communication avec VLAN 10.
- **VLAN 30** : tous les droits.
- **VLAN 40** : Internet uniquement, plus ping autorisé vers VLAN 30.

### 4.3 Configuration rédigée

```
ip access-list extended ACL-VLAN10
 permit ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
 deny ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255
 deny ip 192.168.10.0 0.0.0.255 192.168.40.0 0.0.0.255
 permit ip 192.168.10.0 0.0.0.255 any
exit

ip access-list extended ACL-VLAN20
 permit ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
 deny ip 192.168.20.0 0.0.0.255 192.168.30.0 0.0.0.255
 deny ip 192.168.20.0 0.0.0.255 192.168.40.0 0.0.0.255
 permit ip 192.168.20.0 0.0.0.255 any
exit

ip access-list extended ACL-VLAN30
 permit ip 192.168.30.0 0.0.0.255 any
exit

ip access-list extended ACL-VLAN40
 deny ip 192.168.40.0 0.0.0.255 192.168.10.0 0.0.0.255
 deny ip 192.168.40.0 0.0.0.255 192.168.20.0 0.0.0.255
 deny ip 192.168.40.0 0.0.0.255 192.168.30.0 0.0.0.255
 permit ip 192.168.40.0 0.0.0.255 any
exit
```

Le second bloc (ex. `0.0.0.255`) est un **masque générique (wildcard mask)**, l'inverse d'un masque de sous-réseau : `0.0.0.255` signifie « les 3 premiers octets doivent correspondre exactement, le dernier est ignoré ».

### 4.4 Point de vigilance identifié dans cette rédaction

Le cahier des charges prévoit que VLAN 10 **et** VLAN 40 puissent *pinguer* VLAN 30. Or les lignes `deny ip ... 192.168.30.0 ...` bloquent **tout protocole**, y compris ICMP, avant que le `permit ... any` final ne soit atteint. Tel quel, le ping vers le VLAN 30 serait refusé pour ces deux VLANs.

**Correction à envisager** (à valider avec le professeur) — insérer un `permit icmp` **avant** le `deny ip` :
```
ip access-list extended ACL-VLAN10
 permit ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
 permit icmp 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255
 deny ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255
 deny ip 192.168.10.0 0.0.0.255 192.168.40.0 0.0.0.255
 permit ip 192.168.10.0 0.0.0.255 any
exit
```
(même principe à appliquer sur `ACL-VLAN40`).

---

## 5. NAT et PAT — sortir vers Internet

### 5.1 Pourquoi le NAT ?

Les adresses `192.168.x.x` sont des adresses **privées**, non routables sur Internet. Le **NAT** traduit ces adresses en une adresse publique au moment où le trafic sort vers Internet, et inversement pour le retour.

### 5.2 Le PAT (NAT avec overload)

Avec une seule IP publique pour de nombreux postes internes, on utilise le **PAT** (*Port Address Translation*, ou *NAT overload*) : tous les postes partagent la même IP publique, chaque connexion étant distinguée par un port différent côté externe.

```
ip access-list standard NAT-INTERNET
 permit 192.168.10.0 0.0.0.255
 permit 192.168.20.0 0.0.0.255
 permit 192.168.30.0 0.0.0.255
 permit 192.168.40.0 0.0.0.255
exit

ip nat inside source list NAT-INTERNET interface GigabitEthernet0/0/1 overload
```
Cette ACL est une **ACL standard** (filtre uniquement sur la source) : son rôle n'est pas de bloquer du trafic mais de désigner quels réseaux ont le droit d'être NATés vers Internet.

---

## 6. Étapes suivantes / à faire

- Corriger les ACL VLAN10 et VLAN40 pour le ping vers le VLAN 30 (§4.4).
- Sauvegarder la configuration finale (`copy running-config startup-config`).
- Exporter la configuration via un serveur **TFTP** pour vérification/archivage externe.

---

## 7. Lexique

| Terme | Définition courte |
|---|---|
| VLAN | Réseau local virtuel, isolant le trafic au niveau 2 |
| Trunk | Lien transportant plusieurs VLANs, trames marquées 802.1Q |
| Router-on-a-stick | Routage inter-VLAN via un seul lien trunk et des sous-interfaces |
| ACL | Liste de règles permit/deny évaluées dans l'ordre, deny implicite final |
| Wildcard mask | Masque inversé utilisé dans les ACL |
| NAT | Traduction d'adresse privée ↔ publique |
| PAT / overload | NAT avec partage d'une seule IP publique via les ports |
