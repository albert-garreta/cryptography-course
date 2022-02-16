from utils import inverse_mod_p, modular_sqrt


class EllipticCurvePrime(object):
    def __init__(self, A, B, p):
        self.A = A
        self.B = B
        self.p = p
        
        # Aquí guardaremos todos los puntos de la curva 
        # Es un conjunto en lugar de una lista para evitar
        # puntos repetidos. Empezamos poniendo el punto del infinito
        self.points = {EllipticPointPrime(None, None)}
        
    def find_all_points(self):
        """Encuentra todos los puntos de la curva elíptica"""
        for x_coord in range(self.p):
            self._process_x_coord_candidate(x_coord)
            
    def _process_x_coord_candidate(self, x_coord):
        y_coord = self._try_find_y_coord(x_coord)
        if y_coord is not None:
            # Si ha encontrado una coordenada y, entonces obtenemos los
            # siguientes puntos
            point1 = EllipticPointPrime(x_coord, y_coord)
            point2 = EllipticPointPrime(x_coord, -y_coord % p)
            self.points.add(point1)
            self.points.add(point2)
            
            
    def _right_side_fun(self, x):
        return (x ** 3 + self.A * x + B) % p

    def _try_find_y_coord(self, x_coord):
        
        right_side = self._right_side_fun(x_coord)
        # modular_sqrt devuelve una raíz cuadrada si existe,
        # si no, devuelve 0
        sqrt_root = modular_sqrt(right_side, self.p)
        return sqrt_root

    def has_point(self, point):
        return (point.y ** 2) % p == self._right_side_fun(point.x)


class EllipticPointPrime(object):
    def __init__(self, x0, y0):
        self.x = x0
        self.y = y0
        # `self.is_infinite` va a ser True si el punto es el punto del infinito
        # Será False si no.
        # Acordamos que es el punto del infinito si x0 es None
        # y y0 es None
        if x0 == None and y0 == None:
            self.is_infinite = True
        else:
            self.is_infinite = False
            self.x = self.x % p
            self.y = self.y % p

    def __repr__(self):
        # Aquí decimos que tiene que hacer el programa cuando
        # escribimos print([un Point])
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        # Aquí damos un criterio para que dos instancias de esta
        # clase (self y other) sean iguales.
        if self.x % p == other.x % p and self.y % p == other.y % p:
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
            return EllipticPointPrime(None, None)
        if P1 != P2:
            lambda_ = ((P2.y - P1.y) * inverse_mod_p(P2.x - P1.x, p)) % p
        elif P1 == P2:
            lambda_ = ((3 * (P1.x) ** 2 + A) * inverse_mod_p(2 * P1.y, p)) % p
        x3 = (lambda_ ** 2 - P1.x - P2.x) % p
        y3 = (lambda_ * (P1.x - x3) - P1.y) % p
        new_point = EllipticPointPrime(x3, y3)
        return new_point

    def mult_by_n(self, number):
        new_point = EllipticPointPrime(self.x, self.y)
        for _ in range(number-1):
            new_point = new_point + new_point
        return new_point



if __name__ == "__main__":
    A = 10
    B = 4
    p = 191
    ec = EllipticCurvePrime(A, B, p)
    ec.find_all_points()
    print(ec.points)
    P=EllipticPointPrime(43, 165)
    has = ec.has_point(P)
    print(has)

    Q = P.mult_by_n(10)
    print(Q)
    print(Q+Q)