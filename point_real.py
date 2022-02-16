
# Y**2 = X**3 + 2X + 8
# Ejemplos de puntos: (0, 4), (-1, raíz quadrada de 5)

class EllipticPointR(object):
    def __init__(self, x0, y0):
        self.x = x0
        self.y = y0
        # Esto va a ser True si el punto es el punto del infinito
        # Será False si no.
        # Acordamos que es el punto del infinito si x0 es None
        # y y0 es None
        if x0 == None and y0 == None:
            self.is_infinite = True
        else:
            self.is_infinite = False

    def __repr__(self):
        # Aquí decimos que tiene que hacer el programa cuando
        # escribimos print([un Point])
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        # Aquí damos un criterio para que dos instancias de esta
        # clase (self y other) sean iguales.
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __add__(self, other):
        # Aquí definimos lo que resulta de sumar este
        # Point (el self) con otro Point (el other)
        P1 = self
        P2 = other
        if P1.is_infinite:
            # En este caso el primer punto (self, o P1) es O
            # Por lo tanto self + other = other
            return P2
        if P2.is_infinite:
            # Lo mismo que antes, pero al revés
            return P1
        if P1.x == P2.x and P1.y == -(P2.y):
            # Recordad que un punto cuyas coordenadas son
            # None, None se establece como el punto del infinito
            # segun nuestra definición __init__
            return EllipticPointR(None, None)
        if P1 != P2:
            lambda_ = (other.y-self.y)/(other.x-self.x)  # esto lo rellenaremos luego
        elif P1 == P2:
            lambda_ =  (3*(self.x)**2+A)/(2*self.y)  # esto lo rellenaremos luego

        x3 = lambda_ ** 2 - P1.x - P2.x
        y3 = lambda_ * (P1.x - x3) - P1.y
        new_point = EllipticPointR(x3, y3)
        return new_point


if __name__ == "__main__":
    
    A = 2
    B = 4
    # Y^2 = X^3 + AX +B
    punto2 = EllipticPointR(0, 2)
    punto3 = EllipticPointR(-1, 1)

    punto_suma = punto2 + punto3

    print(punto_suma)
    x, y= punto_suma.x, punto_suma.y
    assert y**2 == x**3 + A*x + B
