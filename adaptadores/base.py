"""
Contrato (interface) que todo adaptador de empresa deve implementar.

Uso do padrão Adapter (GoF) combinado com o princípio OCP (SOLID):
- cada nova empresa adiciona apenas um novo adaptador;
- o código principal (IntegracaoService) nunca precisa ser alterado.

A classe abstrata também serve como documentação viva do contrato esperado.
"""

from abc import ABC, abstractmethod
from models.passagem import Passagem


class AdaptadorPassagem(ABC):
    """
    Interface base para adaptadores de APIs de empresas rodoviárias.

    Subclasses devem:
    1. Implementar `adaptar(payload)` convertendo o dict bruto em Passagem.
    2. Implementar `empresa_suportada()` retornando o identificador da empresa.
    3. Lançar `ValueError` em caso de payload inválido ou campos ausentes.
    """

    @abstractmethod
    def adaptar(self, payload: dict) -> Passagem:
        """
        Converte o payload bruto da empresa para o modelo interno Passagem.

        :param payload: dicionário com os dados recebidos da API da empresa.
        :returns: objeto Passagem padronizado.
        :raises ValueError: se campos obrigatórios estiverem ausentes ou inválidos.
        :raises TypeError: se o tipo de algum campo for inesperado.
        """

    @abstractmethod
    def empresa_suportada(self) -> str:
        """
        Retorna o identificador único da empresa (usado no registro do factory).
        """

    def _validar_campos(self, payload: dict, campos: list[str]) -> None:
        """
        Valida que todos os campos obrigatórios estão presentes no payload.
        Método utilitário reutilizável por qualquer subclasse.
        """
        ausentes = [c for c in campos if c not in payload]
        if ausentes:
            raise ValueError(
                f"[{self.empresa_suportada()}] Campos obrigatórios ausentes no payload: {ausentes}. "
                f"Payload recebido: {payload}"
            )
