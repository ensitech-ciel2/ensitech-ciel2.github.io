# Suites numériques — Cours

**Matière :** Maths
**Dernière mise à jour :** 17/09/2026
**Statut :** fichier évolutif — à compléter à chaque nouveau cours sur les suites

---

## 1. Pourquoi étudier les suites ?

Une suite numérique modélise l'évolution d'une grandeur **par étapes discrètes** (jour après jour, mesure après mesure, itération après itération) plutôt que de façon continue. C'est un outil pertinent en informatique et en physique : le nombre de connexions à un serveur chaque jour, la tension d'un condensateur mesurée seconde par seconde, la capacité de stockage d'une base de données qui double chaque année, sont naturellement des suites.

## 2. Définition générale

Une **suite numérique** est une liste de nombres rangés dans un ordre précis, notée $(U_n)_{n \in \mathbb{N}} = (u_0, u_1, u_2, \dots)$. Chaque $U_n$ est un **terme**, $n$ est son **rang**.

Deux façons de définir la règle qui gouverne une suite :
- une **formule de récurrence**, qui donne un terme à partir du précédent (il faut calculer tous les termes un par un pour atteindre un rang donné) ;
- une **formule explicite**, qui donne directement $U_n$ en fonction de $n$ seul.

---

## 3. Suites arithmétiques (rappel)

Une suite est **arithmétique** si l'on passe d'un terme au suivant en **ajoutant toujours la même valeur** $r$ (la raison) — modèle d'une évolution "à vitesse constante".

- Récurrence : $U_{n+1} = U_n + r$
- Explicite : $U_n = U_0 + n \times r$

**Variation :** $r > 0$ → croissante ($\lim = +\infty$) ; $r < 0$ → décroissante ($\lim = -\infty$) ; $r = 0$ → constante.

**Somme des $n+1$ premiers termes :**
$$S_n = \frac{(n+1)(U_0 + U_n)}{2}$$
*(intuition : les termes étant régulièrement espacés, leur moyenne est celle du premier et du dernier terme ; il suffit de la multiplier par le nombre de termes.)*

---

## 4. Suites géométriques

Une suite est **géométrique** si l'on passe d'un terme au suivant en **multipliant** toujours par la même valeur $q$ (la raison) — modèle d'une évolution "en facteur constant" (croissance de population, intérêts composés, décharge exponentielle, doublement d'une capacité de stockage...).

**Exemple d'introduction :** $u_0 = 5$, et l'on multiplie par 2 à chaque étape : $u_0=5,\ u_1=10,\ u_2=20,\ u_3=40...$ — c'est une suite géométrique de raison $q=2$ et de premier terme 5, définie par $\{u_0 = 5,\ U_{n+1} = 2u_n\}$.

- Récurrence : $U_{n+1} = q \times U_n$
- Explicite (à partir de $U_0$) : $U_n = U_0 \times q^n$
- Explicite **à partir d'un terme quelconque** $U_p$ (formule plus générale, utile quand on ne connaît pas $U_0$) : $U_n = U_p \times q^{\,n-p}$

**Différence clé avec l'arithmétique :** l'arithmétique ajoute une quantité fixe (évolution linéaire, une droite sur un graphique), la géométrique multiplie par un facteur fixe (évolution exponentielle, une courbe qui s'envole ou s'écrase vers 0).

### 4.1 Exercices résolus — trouver l'expression explicite

**a)** $u_0 = 3$ et $U_{n+1} = 4u_n$ → suite géométrique de raison $q=4$, premier terme connu :
$$U_n = U_0 \times q^n = 3 \times 4^n$$

**b)** $u_1 = 5$ et $U_{n+1} = 2u_n$ → ici c'est $U_1$ qui est connu, pas $U_0$. On utilise la formule générale $U_n = U_p \times q^{n-p}$ avec $p=1$ :
$$U_n = U_1 \times q^{\,n-1} = 5 \times 2^{\,n-1}$$

**c) Cas où deux termes non consécutifs sont connus** — $u_4 = 8$ et $u_7 = 512$ :

*Étape 1 — trouver la raison.* On relie les deux termes connus avec la formule générale $U_n = U_p \times q^{n-p}$, en prenant pour $p$ le rang le plus petit connu (ici 4) et pour $n$ le plus grand (ici 7) :
$$U_7 = U_4 \times q^{7-4} = U_4 \times q^3$$
$$512 = 8 \times q^3 \quad\Rightarrow\quad q^3 = 64 \quad\Rightarrow\quad q = \sqrt[3]{64} = 4$$
*(la racine cubique de 64 est 4, car $4^3 = 64$)*

*Étape 2 — remonter jusqu'à $U_0$.* On sait que $U_4 = U_0 \times q^4$, donc :
$$8 = U_0 \times 4^4 = U_0 \times 256 \quad\Rightarrow\quad U_0 = \frac{8}{256} = \frac{1}{32} = 0{,}03125$$

*Étape 3 — écrire la formule explicite complète :*
$$U_n = \frac{1}{32} \times 4^n$$

### 4.2 Somme des $n+1$ premiers termes d'une suite géométrique

**Propriété** (pour $q \neq 1$) :
$$1 + q + q^2 + \dots + q^n = \frac{1 - q^{n+1}}{1 - q}$$

Et plus généralement, pour une suite géométrique de premier terme $U_0$ :
$$S_n = U_0 \times \frac{1 - q^{n+1}}{1 - q}$$

**Exemple** — suite $u_0 = 3$, $U_{n+1} = 4u_n$ (raison $q=4$), somme des 11 premiers termes ($S_{10}$) :
$$S_{10} = \frac{1 - 4^{11}}{1 - 4} = \frac{4^{11} - 1}{3}$$
*(en multipliant numérateur et dénominateur par $-1$ pour obtenir une forme positive plus lisible)*

### 4.3 Sens de variation d'une suite géométrique

Le sens de variation dépend à la fois du signe de $U_0$ et de la valeur de $q$ :

**Si $U_0 > 0$ :**
- $q > 1$ → suite **croissante**
- $0 < q < 1$ → suite **décroissante**

**Si $U_0 < 0$ :**
- $q > 1$ → suite **décroissante**
- $0 < q < 1$ → suite **croissante**

**Cas particuliers :**
- $q = 1$ → suite constante
- $q \le 0$ → la suite **n'est pas monotone** : elle alterne de signe à chaque terme (oscille), car multiplier par un nombre négatif inverse le signe à chaque étape.

### 4.4 Comportement à l'infini (limite)

Pour une suite géométrique de raison $q$ :
- Si $q > 1$ : la suite diverge vers $+\infty$ si $U_0 > 0$, vers $-\infty$ si $U_0 < 0$. *(Exemple simple : $U_n = 2^n$ avec $U_0=1$ — la suite explose : 1, 2, 4, 8, 16... → $+\infty$.)*
- Si $-1 < q < 1$ : $\lim_{n \to +\infty} U_n = 0$. *(Exemple simple : $U_n = 0{,}5^n$ — la suite s'écrase vers 0 : 1, 0,5, 0,25, 0,125...)*
- Si $q \le -1$ (et $U_0 \neq 0$) : la suite **diverge sans limite** — elle oscille avec une amplitude qui augmente (ou reste constante si $q=-1$) sans jamais se stabiliser.

### 4.5 Exercices résolus — applications

**Exercice — capacité de stockage.** Une base de données possède 2 To de stockage ; la direction double cette capacité chaque année.
1. C'est une suite géométrique de raison $q = 2$ (on multiplie par 2 chaque année).
2. Formule explicite : $U_n = U_0 \times q^n = 2 \times 2^n$
3. Capacité au bout de 6 ans : $U_6 = 2 \times 2^6 = 2 \times 64 = 128$ To.
4. La suite est croissante, car $q > 1$ et $U_0 > 0$ (cf. §4.3).

**Exercice — décharge d'une batterie.** Une batterie de smartphone perd 8 % de sa charge à chaque heure d'utilisation, en partant de 100 %.
1. C'est une suite géométrique : perdre 8 % signifie qu'il **reste 92 %** de la charge précédente à chaque heure — donc $U_0 = 100$ et $q = 0{,}92$ (et non 0,08 : c'est un piège classique de confondre le taux de perte et la raison, qui est le facteur multiplicatif restant).

---

## 5. Suites constantes et suites par récurrence générale

Une suite est **constante** ($U_n = k$ pour tout $n$) : c'est un cas particulier d'arithmétique ($r=0$) ou de géométrique ($q=1$).

Certaines suites ne rentrent dans aucune des deux familles ci-dessus (ex. $U_{n+1} = 0{,}5 \times U_n + 3$) : il n'existe pas toujours de formule explicite simple, on calcule alors pas à pas terme après terme.

## 6. Suites particulières à connaître

- $U_n = \dfrac{1}{n}$ : tend vers 0 — modélise une grandeur qui s'atténue avec l'itération.
- $U_n = (-1)^n$ : alterne entre $+1$ et $-1$ ($u_0=1, u_1=-1, u_2=1...$) — modélise un signal binaire ou une oscillation.

---

## 7. Lexique

| Terme | Définition courte |
|---|---|
| Raison | Valeur ajoutée ($r$, arithmétique) ou multipliée ($q$, géométrique) à chaque étape |
| Suite arithmétique | Évolution "à vitesse constante" (ajout d'une quantité fixe) |
| Suite géométrique | Évolution "en facteur constant" (multiplication par un facteur fixe) |
| Divergence | La suite ne tend vers aucune limite finie |
