import random

from .models import Pedido


def gerar_codigo_unico() -> int:

    codigo = random.randint(10000, 99999)
    while Pedido.objects.filter(codigo_do_pedido=codigo).exists():
        codigo = random.randint(10000, 99999)
    return codigo



def converter_para_int(valor) -> int:

    try:
        return int(valor)
    except (TypeError, ValueError):
        return 0
    
