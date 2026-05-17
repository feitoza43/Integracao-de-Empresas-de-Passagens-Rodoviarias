"""
Adaptador para a Empresa D — Regional (Desafio Extra).

Demonstra como adicionar uma NOVA empresa sem alterar nenhuma linha
do código principal (IntegracaoService, main.py, etc.).

Payload fictício da empresa:
{
  "transportadora": "Regional",
  "partida": {
    "cidade": "Fortaleza",
    "timestamp": "1749560400"          ← Unix timestamp (epoch)
  },
  "chegada": {
    "cidade": "Teresina",
    "timestamp": "1749582000"
  },
  "tarifa_brl": "189,90"              ← string com vírgula decimal (formato BR)
}
"""

from datetime import datetime
from adaptadores.base import AdaptadorPassagem
from models.passagem import Passagem


class AdaptadorRegional(AdaptadorPassagem):
    """
    Converte o formato da Regional para o modelo interno.

    Peculiaridades tratadas:
    - horários como Unix timestamp (string);
    - valor como string BR com vírgula decimal ("189,90").
    """

    _CAMPOS_OBRIGATORIOS = ["transportadora", "partida", "chegada", "tarifa_brl"]

    def empresa_suportada(self) -> str:
        return "Regional"

    def adaptar(self, payload: dict) -> Passagem:
        self._validar_campos(payload, self._CAMPOS_OBRIGATORIOS)

        return Passagem(
            empresa=payload["transportadora"],
            origem=payload["partida"]["cidade"],
            destino=payload["chegada"]["cidade"],
            horario_saida=self._parse_timestamp(payload["partida"]["timestamp"]),
            horario_chegada=self._parse_timestamp(payload["chegada"]["timestamp"]),
            valor=self._parse_tarifa(payload["tarifa_brl"]),
        )

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _parse_timestamp(value: str) -> datetime:
        """Converte Unix timestamp (string ou int) para datetime."""
        try:
            return datetime.fromtimestamp(int(value))
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Timestamp inválido: {value!r}") from exc

    @staticmethod
    def _parse_tarifa(value: str) -> float:
        """Converte string no formato BR ('189,90') para float (189.90)."""
        try:
            return round(float(str(value).replace(",", ".")), 2)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Tarifa inválida: {value!r}") from exc
