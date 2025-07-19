import csv as csv
import math as mt

def clamp(value, min, max):
    """Borne value dans l'intervalle min et max.

    arg:
        value: nombre a borner.
        min: Borne inferieur, il doit etre inferieur a max.
        max: Borne superieur, il doit etre superieur a min.
    
    Return:
        Si value est dans l'intervalle alors il retourne value.
        Si value est inferieur a min alors il retourne min.
        Si value est superieur a max alors il retourne max.
    Raise:
        valueError: si min > max.
    """
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value

def import_csv(fichier):
    """Import un fichier en l'ouvrant et le lisant, et renvoie une liste de dictionnaires.
    Arg:
        fichier: le nom du fichier a lire(sans le .csv)
    Return:
        une liste ou chaque ligne est representer par un dict
        {nom_de_colonne: value}.
    """
    lecteur = csv.DictReader(open(fichier + '.csv', 'r'))
    return [dict(ligne) for ligne in lecteur]

def export_csv(source_file ,dest_file , order):
    """Copie un CSV en réordonnant/filtrant les colonnes.

    Args:
        source_file: Nom (sans .csv) du fichier d’entrée.
        dest_file:  Nom (sans .csv) du fichier de sortie.
        order:      Ordre désiré des colonnes (noms identiques au header).
    """
    with open(source_file + '.csv', 'r') as src:
        lecteur = csv.DictReader(src)
        with open(dest_file + '.csv', 'w', newline='') as fichier:
            dic = csv.DictWriter(fichier, fieldnames=order)
            dic.writeheader()
            for ligne in lecteur:
                dic.writerow(ligne)

def lerp(a, b, ratio):
    """Interpolation linéaire entre `a` et `b`.

    Args:
        a: Valeur de départ.
        b: Valeur d’arrivée.
        t: Rapport de 0.0 à 1.0 inclus (0 ⇒ a, 1 ⇒ b).

    Returns:
        Valeur intermédiaire.
    """
    return (b -  a) * ratio + a

def mean(iterable):
    """Renvoie la moyenne d’un itérable de nombres.

    Args:
        values: Séquence ou itérateur contenant int/float ou leurs chaînes.

    Returns:
        Moyenne arithmétique en float.

    Raises:
        ValueError: Si l’itérable est vide.
    """
    count = 0
    n = 0
    for j in iterable:
        count = count + float(j)
        n += 1
    if n > 0:
        count = count / n
    else:
        count = 0
    return count

def sort_insertion(iterable):
    """trie la liste par insertion.

    Args:
        iterable: La liste a trier.
    
    Returns:
        la liste trier.
    """
    for i in range(1, len(iterable)):
        key = iterable[i]
        j = i - 1
        while j >= 0 and iterable[j] > key:
            iterable[j + 1] = iterable[j]
            j -= 1
        iterable[j + 1] = key
    return iterable

def median(iterable):
    """ trouve la median des list pair et impair.

    Args:
        iterable: la liste ou il faut trouver la medianne.
    
    Returns:
        renvoie la medianne, si la liste est pair c'est un nombre entre les deux nombre au milieu de la liste et en float 
        et si elle est inpair c'est le nombre au milieur.
    
    Raises:
        valueError: median() d'un iterable vide.
    """
    value = sort_insertion(list(iterable))
    size = len(value)
    if size == 0:
        raise ValueError("median() d'un iterable vide")
    if size % 2 == 0:
        i = size // 2
        return (value[i - 1] + value[i]) / 2
    else:
        i = size // 2
        return float(value[i])

def stddev(iterable, sample=False):
    """Fait un ecart type sur un échantillon ou une population.

    Args:
        iterable: la liste qui est un echantillon ou une population.
        sample: si il est sur False c'est une population et si il est sur True c'est un echantillon.
    
    Returns:
        renvoie l'ecart type de la liste.
    Raises:
        ValueError: sttdev() necessite au moins 1 (ou 2) valeur.
    """
    nums = [float(x) for x in iterable]
    j = 0
    result = 0
    m = mean(nums)
    size = len(nums)
    if (size == 0 or (sample and size == 1)):
        raise ValueError("stddev() nécessite au moins 1 (ou 2) valeur")
    while j < size:
        nums[j] = nums[j] - m
        result += nums[j] * nums[j]
        j += 1
    divisor = size - 1 if sample else size
    result = result / divisor
    return mt.sqrt(result)

def factoriel_iter(n):
    """Factoriel de n (≥ 0) via iteration.
    """
    if not isinstance(n, int):
        raise TypeError("factorial_iter() attend un entier")
    if n < 0:
        raise ValueError("factorial_iter() n'est pas défini pour n < 0")
    i = 1
    value = 1
    while i <= n:
        value *= i
        i += 1
    return value

def factoriel_loop(n, i, value):
    if i <= n:
        value = factoriel_loop(n, i + 1, value * i)
    return value

def factoriel_rec(n):
    """Factoriel de n (≥ 0) via récursion terminale.

    Attention : CPython ne fait pas d’optimisation TCO,
    donc RecursionError pour de très grands n.
    """
    if not isinstance(n, int):
        raise TypeError("factorial_iter() attend un entier")
    if n < 0:
        raise ValueError("factorial_iter() n'est pas défini pour n < 0")
    return factoriel_loop(n, 1, 1)

def strlen(iterable):
    """recuperer la longueur d'un tableau.

    Args:
        iterable: le tableau dont on veux calculer la longueur.
    """
    len = 0
    for _ in iterable:
        len += 1
    return len

def new_tab(iterable):
    """cree une deep copie du premier tableau.

    Args:
        iterable: le tableau a copier.
    """
    new = []
    for i in iterable:
        new += [i]
    return new

def is_prime(n):
    """permet de savoir si un nombre et premier ou pas.
    
    Args:
        n: le nombre a testé.
    Returns:
        il envoi soit true si c'est un nombre premier et false si ce n'est pas un nombre premier.
    """
    result = 1
    len = 2
    if n <= 0:
        return False
    while result < n:
        len = 2
        while len < n:
            if result * len == n:
                return False
            len += 1
        if result > n / 2:
            return True
        result += 1
    return True

def gcd(a, b):
    """Trouve le plus grand diviseur commun.
    
    Args:
        a: le premier nombre a verifier.
        b: le deuxieme nombre a verifier.
    Returns:
        il envoi le plus grand diviseur commun.
    """
    result = 1
    j = 1
    i = 1
    tab_a = []
    tab_b = []
    while i <= a  and i <= b:
        j = 0
        while j <= a  and j <= b:
            if i * j == a:
               tab_a += [j]
               tab_a += [i]
            if i * j == b:
               tab_b += [i]
               tab_b += [j]
            j += 1
        i += 1
    i = 0
    while strlen(tab_a) > i:
        j = 0
        while strlen(tab_b) > j:
            if tab_b[j] == tab_a[i] and tab_b[j] > result:
                result = tab_b[j]
            j += 1
        i += 1
    return result

def is_container(x):
    """ teste si c'est un container
    Args:
        x: element a testé.
    Returns: envoie true ou false.
    """
    try:
        iter(x)
    except TypeError:
        return False
    return not isinstance(x, (str, bytes))

def flatten(nested_iterable, depth=-1):
    """Applatissement des listes imbriquées.
    Args:
        nested_iterable: l'element qui contient tout les listes.
        depth: la profondeur a definir pour l'applatissement,
        si il est egal a -1 on fait tout, sinon on va jusqu'a 0.
    Returns: envoi la nouvelle liste applatie."""
    y = []
    for item in nested_iterable:
        if depth != 0 and is_container(item):
            y += flatten(item, depth - 1)
        else:
            y += [item]
    return y

