"""
Adaptador para a Empresa B — Expresso Brasil.

Payload esperado:
{
  "nome_empresa": "Expresso Brasil",
  "cidade_origem": "Fortaleza",
  "cidade_destino": "Natal",
  "horario_saida": "2026-06-11T07:00:00",
  "horario_chegada": "2026-06-11T15:20:00",
  "preco_passagem": {
    "valor": 149.50,
    "moeda": "BRL"
  }
}
"""

from adaptadores.base import AdaptadorPassagem
from models.passagem import Passagem
from utils.parsers import parse_datetime, parse_valor


class AdaptadorExpressoBrasil(AdaptadorPassagem):
    """
    Converte o formato da Expresso Brasil para o modelo interno.

    Peculiaridades tratadas:
    - nomes de campos distintos (nome_empresa, cidade_origem, cidade_destino);
    - data no formato ISO-8601 com 'T';
    - valor encapsulado em objeto {"valor": X, "moeda": "BRL"}.
    """

    _CAMPOS_OBRIGATORIOS = [
        "nome_empresa", "cidade_origem", "cidade_destino",
        "horario_saida", "horario_chegada", "preco_passagem",
    ]

    def empresa_suportada(self) -> str:
        return "expresso_brasil"

    def adaptar(self, payload: dict) -> Passagem:
        self._validar_campos(payload, self._CAMPOS_OBRIGATORIOS)

        return Passagem(
            empresa=payload["nome_empresa"],
            origem=payload["cidade_origem"],
            destino=payload["cidade_destino"],
            horario_saida=parse_datetime(payload["horario_saida"]),
            horario_chegada=parse_datetime(payload["horario_chegada"]),
            valor=parse_valor(payload["preco_passagem"]),
        )
