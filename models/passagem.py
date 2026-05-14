"""
Modelo interno padronizado de Passagem.
Toda integração com empresas externas deve resultar em um objeto deste tipo.
"""

from datetime import datetime


class Passagem:
    """
    Representa uma passagem de ônibus no formato interno da plataforma.

    Todos os adaptadores de empresas devem produzir instâncias desta classe,
    garantindo que o restante da aplicação trabalhe com um contrato único e estável.
    """

    def __init__(
        self,
        empresa: str,
        origem: str,
        destino: str,
        horario_saida: datetime,
        horario_chegada: datetime,
        valor: float,
    ):
        self.empresa = empresa
        self.origem = origem
        self.destino = destino
        self.horario_saida = horario_saida
        self.horario_chegada = horario_chegada
        self.valor = valor

    def __repr__(self) -> str:
        return (
            f"Passagem("
            f"empresa='{self.empresa}', "
            f"origem='{self.origem}', "
            f"destino='{self.destino}', "
            f"saida='{self.horario_saida}', "
            f"chegada='{self.horario_chegada}', "
            f"valor=R${self.valor:.2f}"
            f")"
        )

    def to_dict(self) -> dict:
        """Serializa a passagem para dicionário (útil para logs e testes)."""
        return {
            "empresa": self.empresa,
            "origem": self.origem,
            "destino": self.destino,
            "horario_saida": self.horario_saida.isoformat(),
            "horario_chegada": self.horario_chegada.isoformat(),
            "valor": round(self.valor, 2),
        }
