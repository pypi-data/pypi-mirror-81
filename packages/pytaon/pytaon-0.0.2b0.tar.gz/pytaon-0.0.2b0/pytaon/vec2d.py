from typing import Union, Tuple
from numbers import Number
from math import sqrt, pi

VecLike = Union["Vec2d", Tuple[Number, Number]]
RADS_TO_DEGREES = 180 / pi
DEGREES_TO_RADS = pi / 180


class Vec2d:
    """
    Vetor em 2 dimensões. Suporta operações básicas e mostra propriedades do
    vetor como métodos.
    """

    # Propriedades e atributos
    x: float
    y: float

    @property
    def angle(self):
        """
        Ângulo com relação ao eixo x em radianos.
        """
        raise NotImplementedError

    @angle.setter
    def angle(self, value):
        raise NotImplementedError

    @property
    def angle_degrees(self):
        """
        Ângulo com relação ao eixo x em graus.
        """
        raise NotImplementedError

    @angle_degrees.setter
    def angle_degrees(self, value):
        raise NotImplementedError

    @property
    def length(self):
        """
        Módulo do vetor.
        """
        raise NotImplementedError

    @length.setter
    def length(self, value):
        raise NotImplementedError

    @property
    def length_sqrd(self):
        """
        Módulo do vetor ao quadrado.
        """
        raise NotImplementedError

    # Métodos estáticos
    @classmethod
    def unit_x(cls) -> "Vec2d":
        """
        Vetor unitário na direção x.
        """
        return cls(1.0, 0.0)

    @classmethod
    def unit_y(cls) -> "Vec2d":
        """
        Vetor unitário na direção y.
        """
        return cls(0.0, 1.0)

    @classmethod
    def zero(cls):
        """
        Vetor de tamanho nulo.
        """
        return cls(0.0, 0.0)

    def __init__(self, x, y=None):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"Vec2d({self.x}, {self.y})"

    def __neg__(self):
        raise NotImplementedError

    def __pos__(self):
        raise NotImplementedError

    def __abs__(self):
        return self.length

    # Operações matemáticas
    def __add__(self, other):  # self + other
        if isinstance(other, (Vec2d, tuple)):
            x, y = other
            return Vec2d(self.x + x, self.y + y)
        return NotImplemented

    __radd__ = __add__  # other + self == self + other

    def __iadd__(self, other):  # self += other
        x, y = other
        self.x += x
        self.y += y
        return self

    def __sub__(self, other):
        if isinstance(other, (Vec2d, tuple)):
            x, y = other
            return Vec2d(self.x - x, self.y - y)
        return NotImplemented

    def __rsub__(self, other):
        raise NotImplementedError

    def __isub__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2d(self.x * other, self.y * other)
        return NotImplemented

    __rmul__ = __mul__

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __matmul__(self, other):
        if isinstance(other, (int, float)):
            x, y = other
            return self.x * x + self.y * y
        return NotImplemented

    __rmatmul__ = __matmul__

    def __truediv__(self, other):  # self * (1 / other)
        return self.__mul__(1 / other)

    def __itruediv__(self, other):  # self /= other
        return self.__imul__(1 / other)

    # Comparações
    def __eq__(self, other):
        if isinstance(other, (Vec2d, tuple)):
            x, y = other
            return x == self.x and y == self.y
        return NotImplemented

    # Comportamento de sequências
    def __len__(self):
        return 2

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, idx):
        raise NotImplementedError

    def __setitem__(self, idx, value):
        raise NotImplementedError

    # Métodos da classe
    def copy(self):
        """
        Retorna cópia do vetor.
        """
        raise NotImplementedError

    def cross(self, other: VecLike) -> float:
        """
        Retorna componente z do produto vetorial com outro vetor.
        
        ``u.cross(v) -> u.x * v.y - u.y * v.x``
        """
        raise NotImplementedError

    def dot(self, other: VecLike) -> float:
        """
        Retorna o produto escalar com outro vetor.
        
        ``v1.dot(v2) -> v1.x*v2.x + v1.y*v2.y``
        """
        raise NotImplementedError

    def get_angle_between(self, other: VecLike) -> float:
        """
        Retorna ângulo entre self e outro vetor (em radianos).
        """
        raise NotImplementedError

    def get_angle_degrees_between(self, other: VecLike) -> float:
        """
        Retorna ângulo entre self e outro vetor (em graus).
        """
        raise NotImplementedError

    def get_dist_sqrd(self, other: VecLike) -> float:
        """
        Retorna o quadrado da distância entre self e outro vetor.
        """
        raise NotImplementedError

    def get_distance(self, other: VecLike) -> float:
        """
        Retorna a distância entre self e outro vetor.
        """
        return sqrt(self.get_dist_sqrd(other))

    def normalized(self) -> "Vec2d":
        """
        Retorna cópia normalizada do vetor.
        """
        raise NotImplementedError

    def normalize_return_length(self) -> float:
        """
        Normaliza vetor e retorna tamanho antes da normalização.
        """
        raise NotImplementedError

    def interpolate_to(self, other: VecLike, range: float) -> "Vec2d":
        """
        Interpola vetor até other no intervalo controlado por range.

        Range varia de forma que se range=0.0, retorna self, range=1.0 retorna other
        e valores intermediários produzem interpolações. 
        """
        raise NotImplementedError

    def perpendicular(self) -> "Vec2d":
        """
        Retorna vetor perpendicular na direção 90 graus anti-horário.
        """
        raise NotImplementedError

    def perpendicular_normal(self) -> "Vec2d":
        """
        Retorna vetor normalizado e perpendicular na direção 90 graus anti-horário.
        """
        return self.perpendicular().normalized()

    def projection(self, other: VecLike) -> "Vec2d":
        """
        Projeta vetor em cima de outro vetor.
        """
        raise NotImplementedError

    def rotate(self, angle: float):
        """
        Rotaciona vetor pelo ângulo em radianos.
        """
        raise NotImplementedError

    def rotate_degrees(self, angle: float):
        """
        Rotaciona vetor pelo ângulo em graus.
        """
        self.rotate(angle * DEGREES_TO_RADS)

    def rotated(self, angle: float) -> "Vec2d":
        """
        Cria novo vetor rotacionado ângulo em radianos.
        """
        raise NotImplementedError

    def rotated_degrees(self, angle: float) -> "Vec2d":
        """
        Cria novo vetor rotacionado ângulo em graus.
        """
        return self.rotated(angle * DEGREES_TO_RADS)


#
# Funções auxiliares
#
def asvec2d(obj) -> "Vec2d":
    """
    Converte objeto para Vec2d, caso não seja vetor. 
    """
    if isinstance(obj, Vec2d):
        return obj
    elif isinstance(obj, tuple):
        x, y = obj
        return Vec2d(x, y)

    kind = type(obj).__name__  # Extrai nome do tipo de obj.
    raise TypeError(f"não pode converter {kind} em Vec2d")
