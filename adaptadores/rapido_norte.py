"""
Adaptador para a Empresa A — Viação Rápido Norte.

Payload esperado:
{
  "empresa": "Rapido Norte",
  "origem": "Fortaleza",
  "destino": "Recife",
  "saida": "2026-06-10 08:00",
  "chegada": "2026-06-10 18:30",
  "valor": 199.90
}
"""

from adaptadores.base import AdaptadorPassagem
from models.passagem import Passagem
from utils.parsers import parse_datetime, parse_valor


class AdaptadorRapidoNorte(AdaptadorPassagem):
    """
    Converte o formato da Viação Rápido Norte para o modelo interno.

    Peculiaridades tratadas:
    - campos 'saida'/'chegada' em vez de 'horario_saida'/'horario_chegada';
    - valor como float direto.
    """

    _CAMPOS_OBRIGATORIOS = ["empresa", "origem", "destino", "saida", "chegada", "valor"]

    def empresa_suportada(self) -> str:
        return "rapido_norte"

    def adaptar(self, payload: dict) -> Passagem:
        self._validar_campos(payload, self._CAMPOS_OBRIGATORIOS)

        return Passagem(
            empresa=payload["empresa"],
            origem=payload["origem"],
            destino=payload["destino"],
            horario_saida=parse_datetime(payload["saida"]),
            horario_chegada=parse_datetime(payload["chegada"]),
            valor=parse_valor(payload["valor"]),
        )
