# Dérivation — Cours

**Matière :** Maths
**Dernière mise à jour :** 01/10/2026
**Statut :** fichier évolutif — à compléter à chaque nouveau cours sur les dérivées

---

## 1. À quoi sert la dérivée ?

La **dérivée** d'une fonction $f$, notée $f'$, mesure **la vitesse à laquelle $f$ varie**. Concrètement, $f'(a)$ est la **pente de la tangente** à la courbe de $f$ au point d'abscisse $a$ :
- si $f'(a) > 0$, la courbe **monte** à cet endroit ;
- si $f'(a) < 0$, la courbe **descend** ;
- si $f'(a) = 0$, la tangente est horizontale (c'est souvent un minimum ou un maximum).

C'est pour cela qu'on dérive presque toujours une fonction quand on veut **étudier ses variations** : le signe de $f'$ donne directement le sens de variation de $f$ (voir l'exercice complet dans [[Etudes-de-fonctions]]).

*(Exemple physique : si $x(t)$ est la position d'un objet, sa dérivée $x'(t)$ est sa vitesse.)*

Les fonctions polynômes sont **dérivables sur $\mathbb{R}$** : on peut calculer leur dérivée en n'importe quel point.

## 2. Dérivées des fonctions usuelles

| Fonction $f(x)$ | Dérivée $f'(x)$ |
|---|---|
| constante $k$ | $0$ |
| $x$ | $1$ |
| $x^n$ | $n\,x^{n-1}$ |
| $\dfrac{1}{x}$ | $-\dfrac{1}{x^2}$ |
| $\sqrt{x}$ | $\dfrac{1}{2\sqrt{x}}$ |
| $e^x$ | $e^x$ |
| $\ln(x)$ | $\dfrac{1}{x}$ |

## 3. Règles de calcul

Pour deux fonctions $u$ et $v$ dérivables et un nombre $k$ :

| Opération | Formule |
|---|---|
| Somme | $(u + v)' = u' + v'$ |
| Multiplication par un nombre | $(k\,u)' = k\,u'$ |
| Produit | $(u\,v)' = u'v + u\,v'$ |
| Inverse | $\left(\dfrac{1}{u}\right)' = -\dfrac{u'}{u^2}$ |
| Quotient | $\left(\dfrac{u}{v}\right)' = \dfrac{u'v - u\,v'}{v^2}$ |
| **Puissance d'une fonction** | $\left(u^n\right)' = n \times u' \times u^{n-1}$ |

### Zoom sur la règle de la puissance d'une fonction

C'est la règle vue en cours. Quand une **expression entière** est élevée à une puissance $n$, la dérivée s'obtient en 3 gestes :
1. on fait descendre l'exposant $n$ en facteur ;
2. on **réécrit l'expression** avec l'exposant diminué de 1 : $u^{n-1}$ ;
3. on **multiplie par la dérivée de ce qu'il y a à l'intérieur** : $u'$.

> **Note de Claude :** le rappel du brouillon était écrit « $f'(x) = n \times u(x)^{n}{}' \times u(x)^{n-1}$ ». Le facteur du milieu est une coquille : ce n'est pas la dérivée de « $u(x)^n$ » mais celle de $u(x)$, c'est-à-dire $u'(x)$. La formule correcte est $f'(x) = n \times u'(x) \times u(x)^{n-1}$ (les exemples du brouillon, eux, appliquent bien la bonne formule).

## 4. Exemples résolus

### Exemple 1 : $f(x) = (-2x + 1)^2$

On reconnaît la forme $u^n$ avec $u(x) = -2x + 1$ (donc $u'(x) = -2$) et $n = 2$ :
$$f'(x) = 2 \times (-2) \times (-2x + 1)^{1} = -4 \times (-2x + 1) = 8x - 4$$

**Vérification** (en développant d'abord) : $f(x) = 4x^2 - 4x + 1$, donc $f'(x) = 8x - 4$ ✓.

### Exemple 2 : $f(x) = (-x^2 + 2)^2$

Ici $u(x) = -x^2 + 2$, donc $u'(x) = -2x$, et $n = 2$ :
$$f'(x) = 2 \times (-2x) \times (-x^2 + 2) = -4x\,(-x^2 + 2) = 4x^3 - 8x$$

**Vérification** : $f(x) = x^4 - 4x^2 + 4$, donc $f'(x) = 4x^3 - 8x$ ✓.

### Exemple 3 : $f(x) = 2x^2 - x + 1$ (dérivable sur $\mathbb{R}$)

C'est un polynôme : on dérive terme à terme.
$$f'(x) = 2 \times 2x - 1 + 0 = 4x - 1$$

> **Note de Claude :** dans le brouillon, cette dernière fonction est écrite « $(2x^2 - x + 1)$ » sans exposant visible (il a peut-être été perdu à la mise en forme). Si la consigne comportait un exposant, la règle de la puissance s'applique. Exemple si l'exposant était 3 : avec $u(x) = 2x^2 - x + 1$ et $u'(x) = 4x - 1$, on obtient $f'(x) = 3\,(4x - 1)\,(2x^2 - x + 1)^2$. À vérifier avec l'énoncé d'origine.

## 5. Méthode générale pour dériver

1. **Identifier la forme** de la fonction : somme ? produit ? quotient ? puissance d'une expression ?
2. **Nommer** les morceaux ($u$, $v$) et **calculer leurs dérivées** ($u'$, $v'$) à part, au brouillon.
3. **Appliquer la formule** correspondante.
4. **Simplifier** (factoriser si possible : c'est ce qui permet ensuite d'étudier le signe de $f'$).
5. **Vérifier** si c'est possible (en développant, ou en testant avec une valeur simple).

## 6. Lexique

| Terme | Définition |
|---|---|
| Dérivée $f'$ | Fonction qui donne, en chaque point, la pente de la tangente à la courbe de $f$ |
| Tangente | Droite qui "touche" la courbe en un point avec la même pente qu'elle |
| Dérivable sur $D$ | Fonction pour laquelle la dérivée existe en tout point de $D$ |
