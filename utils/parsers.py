"""
Utilitários de padronização reutilizados por todos os adaptadores.

Centralizar a lógica de parsing aqui garante que:
- adaptadores fiquem enxutos e focados no mapeamento de campos;
- alterações de formato afetam apenas este módulo.
"""

from datetime import datetime
from typing import Union


# Formatos de data suportados (order matters: mais específico → mais genérico)
_DATE_FORMATS = [
    "%Y-%m-%dT%H:%M:%S",   # ISO-8601 com T: 2026-06-11T07:00:00
    "%Y-%m-%d %H:%M",       # Simples com espaço: 2026-06-10 08:00
    "%Y-%m-%d %H:%M:%S",    # Com segundos:       2026-06-10 08:00:00
    "%d/%m/%Y %H:%M",       # BR sem segundos:    10/06/2026 21:00
    "%d/%m/%Y %H:%M:%S",    # BR com segundos:    10/06/2026 21:00:00
]


def parse_datetime(value: str) -> datetime:
    """
    Converte uma string de data/hora para um objeto datetime padronizado.

    Tenta sequencialmente os formatos registrados em _DATE_FORMATS.
    Lança ValueError com mensagem descritiva se nenhum formato funcionar.
    """
    if not isinstance(value, str):
        raise TypeError(f"Esperava string para data/hora, recebeu {type(value).__name__!r}: {value!r}")

    value = value.strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    raise ValueError(
        f"Formato de data/hora não reconhecido: {value!r}. "
        f"Formatos suportados: {_DATE_FORMATS}"
    )


def parse_valor(value: Union[int, float, dict]) -> float:
    """
    Converte diferentes representações de valor monetário para float em BRL.

    Suporte a:
    - float/int direto: 199.90, 199
    - dict com chave 'valor': {"valor": 149.50, "moeda": "BRL"}
    - inteiro em centavos detectado por convenção (chave externa 'valor_centavos')
      → neste caso o adaptador já deve dividir por 100 antes de chamar esta função.
    """
    if isinstance(value, (int, float)):
        return round(float(value), 2)

    if isinstance(value, dict):
        if "valor" not in value:
            raise ValueError(f"Dict de valor sem chave 'valor': {value!r}")
        return round(float(value["valor"]), 2)

    raise TypeError(
        f"Tipo não suportado para valor monetário: {type(value).__name__!r}: {value!r}"
    )


def centavos_para_reais(centavos: int) -> float:
    """Converte valor em centavos (inteiro) para reais (float)."""
    if not isinstance(centavos, (int, float)):
        raise TypeError(f"Esperava número para centavos, recebeu {type(centavos).__name__!r}")
    return round(int(centavos) / 100, 2)
