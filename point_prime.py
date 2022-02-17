from utils import inverse_mod_p, modular_sqrt


class EllipticCurvePrime(object):
    def __init__(self, A, B, p):
        self.A = A
        self.B = B
        self.p = p

        # Aquí guardaremos todos los puntos de la curva
        self.points = [EllipticPointPrime(None, None)]
        
        print("\n\n================================\n"
              f"Welcome to the elliptic curve {self}\n")
        
    def __repr__(self):
        return f"E: Y^2 = X^3 + {self.A}*X + {self.B} over the prime {self.p}"

    def find_all_points(self):
        """Encuentra todos los puntos de la curva elíptica"""
        print("Finding all points in the curve...")
        for x_coord in range(self.p):
            self._process_x_coord_candidate(x_coord)
        print("Done\n")

    def find_some_points(self, num_points_to_find):
        for x in range(self.p):
            self._process_x_coord_candidate(x)
            if len(self.points) > num_points_to_find:
                break
        print(f"Found points: {self.points}\n")

    def _process_x_coord_candidate(self, x_coord):
        y_coord = self._try_find_y_coord(x_coord)
        if y_coord is not None:
            # Si ha encontrado una coordenada y, entonces obtenemos los
            # siguientes puntos
            point1 = EllipticPointPrime(x_coord, y_coord)
            point2 = EllipticPointPrime(x_coord, -y_coord % p)
            self.points.append(point1)
            self.points.append(point2)
        # Procesamos aparte el caso en que la 2a coordenada es 0
        self._process_0_y_coord(x_coord)

    def _process_0_y_coord(self, x_coord):
        candidate_point = EllipticPointPrime(x_coord, 0)
        if self.has_point(candidate_point, verbose=False):
            self.points.append(candidate_point)

    def _right_side_fun(self, x):
        return (x ** 3 + self.A * x + B) % p

    def _try_find_y_coord(self, x_coord):
        right_side = self._right_side_fun(x_coord)
        # modular_sqrt devuelve una raíz cuadrada si existe,
        # si no, devuelve 0
        sqrt_root = modular_sqrt(right_side, self.p)
        return sqrt_root

    def has_point(self, point, verbose=True):
        if (point.y ** 2) % p == self._right_side_fun(point.x):
            if verbose:
                print(f"The point {point} belongs to {self}\n")
            return True
        else:
            if verbose: 
                print(f"The point {point} DOES NOT belong to {self}\n")
            return False
            


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
        if self.is_infinite:
            return "infinite"
        else:
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
    

def get_inverse_of_point(point):
    return EllipticPointPrime(point.x, (-point.y)%p)

def mult_point_by_num(point, number):
    if number == 0:
        return EllipticPointPrime(None, None)
    new_point = EllipticPointPrime(point.x, point.y)
    for _ in range(number-1):
        new_point = new_point + point
    return new_point


def log(base, point):
    # Buscamos  el logaritmo del punto en base `base_point`
    # por fuerza bruta
    try:
        temp_point = EllipticPointPrime(base.x, base.y)
        for num in range(1, p):
            if temp_point == point:
                print(f"The log of {point} in base {base} is {num}\n")
                return num
            temp_point = temp_point + base
        print("Log not found\n")
    except:
        print("Log not found\n"


if __name__ == "__main__":
    # Parametros generales
    p = 1046527
    A = 0
    B = 7
    
    # Declaración de la curva elíptica
    ec = EllipticCurvePrime(A, B, p)
    
    # Esto imprimirá el el número de puntos de la curva elíptica que requiramos
    ec.find_some_points(num_points_to_find=10)

    # Esto crea el punto (60268, 35105)
    P = EllipticPointPrime(60268, 35105)
    # Y esto crea otro punto
    Q = EllipticPointPrime(719386, 925426)

    # Esto nos dice si P pertenece a la curvpa elíptica ec
    ec.has_point(P)
    # Lo mismo con Q
    ec.has_point(Q)
    
    # Esto suma P y Q segun la operacion de la curva elíptica
    # y llama R al resultado
    R = P+Q
    # El resultado debería estar en la curva:
    ec.has_point(R)
    
    # Comprobando que `mult_point_by_num` funciona ok
    assert P+P+P+P+P==mult_point_by_num(P,5)
    
    # Calculamos el log de P en base Q
    log_num = log(Q, P)
    
    # Comprobando que la función `log` funciona ok
    assert mult_point_by_num(Q,log_num) == P

    print("Goodbye\n================================\n\n")
