"""
Serviço de integração — ponto central de orquestração.

Recebe payloads brutos + identificador da empresa,
delega a conversão ao adaptador correto e retorna um objeto Passagem.

Este módulo NÃO conhece nenhuma empresa específica; conhece apenas
o contrato AdaptadorPassagem e o RegistroAdaptadores.
Isso garante baixo acoplamento e facilidade de expansão (DIP — Dependency Inversion).
"""

from adaptadores.registro import RegistroAdaptadores
from models.passagem import Passagem


class IntegracaoService:
    """
    Orquestra a integração com múltiplas empresas rodoviárias.

    Responsabilidades:
    - Receber o payload e a chave da empresa.
    - Delegar ao adaptador correto (obtido do registro).
    - Tratar e relançar erros com contexto adicional.
    """

    def converter(self, empresa_chave: str, payload: dict) -> Passagem:
        """
        Converte um payload bruto de uma empresa para o modelo interno Passagem.

        :param empresa_chave: identificador da empresa (ex: "rapido_norte").
        :param payload: dicionário com os dados brutos recebidos da API.
        :returns: objeto Passagem padronizado.
        :raises KeyError: se a empresa não estiver registrada.
        :raises ValueError: se o payload for inválido.
        """
        if not isinstance(payload, dict):
            raise TypeError(
                f"Payload deve ser um dicionário, recebeu {type(payload).__name__!r}"
            )

        adaptador = RegistroAdaptadores.obter(empresa_chave)
        return adaptador.adaptar(payload)

    def empresas_disponiveis(self) -> list[str]:
        """Retorna a lista de empresas com adaptadores registrados."""
        return RegistroAdaptadores.listar()
