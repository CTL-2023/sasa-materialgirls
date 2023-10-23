
import matplotlib.pyplot as plt
import numpy as np

def plot_outer_outline(x1, r1, x2, r2):
    # Erstellen Sie eine Figur und eine Achse
    fig, ax = plt.subplots()

    # Erstellen Sie einen Bereich von x-Werten
    x = np.linspace(x1 - r1, x2 + r1, 400)

    # Berechnen Sie die obere Halbkreisfunktion
    upper_semi_circle = np.sqrt(r1**2 - (x - x1)**2)

    # Berechnen Sie die untere Halbkreisfunktion
    lower_semi_circle = np.sqrt(r2**2 - (x - x2)**2)

    # Zeichnen Sie den äußeren Umriss, indem Sie das Maximum der beiden Funktionen verwenden
    y_outer = np.maximum(upper_semi_circle, lower_semi_circle)

    # Zeichnen Sie die Kurve
    ax.plot(x, y_outer, label='ausserer Umriss', color='blue')

    # Legende und Achsentitel hinzufügen
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # Plot anzeigen
    plt.show()

# Beispiel: Umriss zweier überlappender Halbkreise
x1, r1 = 2, 4
x2, r2 = 7, 2
plot_outer_outline(x1, r1, x2, r2)



#Monte-Carlo
import random

def monte_carlo_integration(func, a, b, n):
    area = 0
    for _ in range(n):
        x = random.uniform(a, b)  # Zufälliger x-Wert im Intervall [a, b]
        y = random.uniform(0, max(func(x), 0))  # Zufälliger y-Wert im Bereich der Funktion
        if y <= func(x):
            area += 1

    return area / n * (b - a)

# Beispiel: Berechnung des Integrals von f(x) = x^2 von 0 bis 1
result = monte_carlo_integration(lambda x: x**2, 0, 1, 100000)
print("Approximiertes Integral:",result)
