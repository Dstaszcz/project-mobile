# Dokumentacja do aplikacji pozwalającej analizować funkcję matematyczne
## Daniel Staszczyszyn 

Aplikacja pozwala wpisać dowolną funkcję w formacie "y = f(x)".
Następnie aplikacja wyświetla narysowaną funkcję i zmienia się w zależności od położenia suwaków.

## Zależności
Aplikacja posiada pole tekstowe, w którym należy wpisać funkcję którą chce się analizować w sposób: "25*x**2 + 13*x - 5" 
- Potęgi należy zapisywać za pomocą symbola "**"
- Pomiędzy współczynnikiem a znakiem "x" musi znajdować się symbol "*"

Aplikacja posiada trzy suwaki odpowiedzialne za:
- 1 i 2 - Modyfikowanie zakresu dziedziny funkcji (Od -20 do 20, z różnicą 1)
- 3 - Modyfikowanie zakresu pomiędzy x'ami (Między 0.1 a 1.0 z różnicą 0.1)
- Wartości te zostały ustawione w takim zakresie aby wykres był czytelny

Po wpisaniu swojej funkcji oraz dostosowaniu dziedziny, należy wcisnąć przycisk ("Show function analysis") 
aby zobczyć własności funkcji.

## Wartości początkowe:
- x_min: -1.0
- x_max: 1.0
- y_min: -5.0
- y_max: 5.0
- step: 0.1
- Function: 1*x**2 -> x^2