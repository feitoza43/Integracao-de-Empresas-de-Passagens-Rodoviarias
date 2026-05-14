"""
Adaptador para a Empresa C — Viação Sol.

Payload esperado:
{
  "viacao": "Viacao Sol",
  "rota": {
    "inicio": "Fortaleza",
    "fim": "Joao Pessoa"
  },
  "horarios": {
    "saida": "10/06/2026 21:00",
    "chegada": "11/06/2026 05:45"
  },
  "valor_centavos": 25990
}
"""

from adaptadores.base import AdaptadorPassagem
from models.passagem import Passagem
from utils.parsers import parse_datetime, centavos_para_reais


class AdaptadorViacaoSol(AdaptadorPassagem):
    """
    Converte o formato da Viação Sol para o modelo interno.

    Peculiaridades tratadas:
    - dados de rota aninhados em objeto 'rota';
    - horários aninhados em objeto 'horarios' com formato BR (dd/mm/yyyy HH:MM);
    - valor em centavos inteiros (ex: 25990 → R$ 259,90).
    """

    _CAMPOS_OBRIGATORIOS = ["viacao", "rota", "horarios", "valor_centavos"]

    def empresa_suportada(self) -> str:
        return "viacao_sol"

    def adaptar(self, payload: dict) -> Passagem:
        self._validar_campos(payload, self._CAMPOS_OBRIGATORIOS)

        rota = payload["rota"]
        if "inicio" not in rota or "fim" not in rota:
            raise ValueError(
                f"[{self.empresa_suportada()}] Objeto 'rota' deve conter 'inicio' e 'fim'. "
                f"Recebido: {rota}"
            )

        horarios = payload["horarios"]
        if "saida" not in horarios or "chegada" not in horarios:
            raise ValueError(
                f"[{self.empresa_suportada()}] Objeto 'horarios' deve conter 'saida' e 'chegada'. "
                f"Recebido: {horarios}"
            )

        return Passagem(
            empresa=payload["viacao"],
            origem=rota["inicio"],
            destino=rota["fim"],
            horario_saida=parse_datetime(horarios["saida"]),
            horario_chegada=parse_datetime(horarios["chegada"]),
            valor=centavos_para_reais(payload["valor_centavos"]),
        )
