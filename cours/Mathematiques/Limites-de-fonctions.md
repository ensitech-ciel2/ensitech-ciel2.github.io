# Limites de fonctions et asymptotes — Cours

**Matière :** Maths
**Dernière mise à jour :** 08/10/2026
**Statut :** fichier évolutif — à compléter à chaque nouveau cours sur les limites

---

## 1. L'idée de limite

Calculer une **limite**, c'est répondre à la question : *« vers quelle valeur la fonction s'approche-t-elle quand $x$ se rapproche d'une valeur (ou devient immense) ? »*

On note par exemple $\lim_{x \to +\infty} f(x)$ : ce que devient $f(x)$ quand $x$ devient de plus en plus grand. Le résultat peut être un nombre (la courbe se stabilise), $+\infty$ ou $-\infty$ (la courbe part vers le haut ou le bas), ou parfois "pas de limite".

## 2. Limites à connaître

| Fonction | Limite en $+\infty$ | Limite en $-\infty$ |
|---|---|---|
| $x$ | $+\infty$ | $-\infty$ |
| $x^2$ | $+\infty$ | $+\infty$ |
| $\dfrac{1}{x}$ | $0$ | $0$ |
| $e^x$ | $+\infty$ | $0$ |
| $\ln(x)$ | $+\infty$ | *(non défini)* |

Et aux bornes finies : $\lim_{x \to 0^+} \ln(x) = -\infty$ ; $\lim_{x \to 0^+} \dfrac{1}{x} = +\infty$.

## 3. Techniques de calcul

- **Somme/produit/quotient :** on calcule la limite de chaque morceau, puis on combine ($+\infty + 1 = +\infty$, etc.).
- **Polynôme en $\pm\infty$ :** seul le **terme de plus haut degré** compte (on dit qu'il "domine"). Exemple : $3x - 125$ se comporte comme $3x$ quand $x$ est très grand.
- **Fraction rationnelle en $\pm\infty$ :** on garde le terme dominant du numérateur et celui du dénominateur, puis on simplifie. Exemple : $\dfrac{t^2 + 31}{t^2 - 9}$ se comporte comme $\dfrac{t^2}{t^2} = 1$.
- **Formes indéterminées :** les cas comme $\dfrac{\infty}{\infty}$ ou $\infty - \infty$ ne donnent pas directement de résultat : il faut transformer l'expression (factoriser le terme dominant, simplifier).

## 4. Interpréter une limite graphiquement : les asymptotes

Une **asymptote** est une droite dont la courbe se rapproche de plus en plus (sans forcément la toucher).

| Résultat du calcul | Interprétation graphique |
|---|---|
| $\lim_{x \to \pm\infty} f(x) = \ell$ (un nombre) | **Asymptote horizontale** d'équation $y = \ell$ |
| $\lim_{x \to a} f(x) = \pm\infty$ | **Asymptote verticale** d'équation $x = a$ |
| $\lim_{x \to \pm\infty} \big(f(x) - (mx + p)\big) = 0$ | **Asymptote oblique** d'équation $y = mx + p$ |
| $\lim_{x \to \pm\infty} f(x) = \pm\infty$ (sans les cas ci-dessus) | Pas d'asymptote horizontale : la courbe "part à l'infini" |

Exemples complets d'asymptote verticale et oblique : voir l'exercice 9 dans [[Etudes-de-fonctions]].

---

## 5. Exercice 7 — Déterminer les limites en $-\infty$ et en $+\infty$, et interpréter

### 1) $f(x) = 3x - 125$

C'est une fonction affine : le terme dominant est $3x$.
$$\lim_{x \to +\infty} (3x - 125) = +\infty \qquad\qquad \lim_{x \to -\infty} (3x - 125) = -\infty$$
*(par exemple, $3 \times (-\infty) = -\infty$).*

**Interprétation graphique :** la courbe est une droite de pente 3, qui monte vers la droite et descend vers la gauche : **pas d'asymptote horizontale**.

> **Note de Claude :** le brouillon écrivait « $f(x) = \lim_{x\to+\infty} 3x - 125 = \lim_{x \to -\infty} 3x = 3(-\infty) = -\infty$ ». Cette ligne mélange les deux limites : le calcul $3(-\infty) = -\infty$ correspond à la limite en $-\infty$. Il manquait la limite en $+\infty$, qui vaut $+\infty$ (ci-dessus).

### 6) $f(t) = \dfrac{t^2 + 31}{(t+3)(t-3)}$

On commence par développer le dénominateur : $(t+3)(t-3) = t^2 - 9$. Donc :
$$f(t) = \frac{t^2 + 31}{t^2 - 9}$$

**Limite en $\pm\infty$** (forme $\dfrac{\infty}{\infty}$ : on factorise le terme dominant, $t^2$) :
$$f(t) = \frac{t^2\left(1 + \frac{31}{t^2}\right)}{t^2\left(1 - \frac{9}{t^2}\right)} = \frac{1 + \frac{31}{t^2}}{1 - \frac{9}{t^2}} \;\xrightarrow[t \to \pm\infty]{}\; \frac{1 + 0}{1 - 0} = 1$$

**Interprétation graphique :** la droite d'équation $y = 1$ est une **asymptote horizontale** à la courbe, en $+\infty$ **et** en $-\infty$.

**Pour aller plus loin (complément) :** le dénominateur s'annule en $t = 3$ et $t = -3$, où le numérateur vaut $40$ (positif). Ces deux valeurs sont donc des **asymptotes verticales** :

| Limite | Valeur |
|---|---|
| $t \to 3^+$ | $+\infty$ |
| $t \to 3^-$ | $-\infty$ |
| $t \to -3^-$ | $+\infty$ |
| $t \to -3^+$ | $-\infty$ |

> **Note de Claude :** le brouillon écrivait « $\dfrac{t^2 - 9}{-t^2 - 9}$ » pour le dénominateur développé, ce qui est une coquille : $(t+3)(t-3) = t^2 - 9$. Le résultat final du brouillon ($\lim = \lim \dfrac{t^2}{t^2} = 1$) est, lui, correct.

---

## 6. Lexique

| Terme | Définition |
|---|---|
| Limite | Valeur vers laquelle tend $f(x)$ quand $x$ tend vers une valeur donnée (ou vers $\pm\infty$) |
| Asymptote | Droite dont la courbe se rapproche indéfiniment |
| Forme indéterminée | Situation ($\frac{\infty}{\infty}$, $\infty - \infty$...) où il faut transformer l'expression avant de conclure |
