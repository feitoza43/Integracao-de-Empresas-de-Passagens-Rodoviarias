"""
Registro central de adaptadores (padrão Factory + Registry).

Como funciona:
- Cada adaptador se auto-registra chamando `RegistroAdaptadores.registrar(...)`.
- O IntegracaoService consulta este registro para obter o adaptador correto.
- Adicionar uma nova empresa = criar o adaptador + uma linha de registro aqui.
  O restante da aplicação não precisa ser alterado (OCP — Open/Closed Principle).
"""

from adaptadores.base import AdaptadorPassagem


class RegistroAdaptadores:
    """
    Mantém o mapeamento chave_empresa → instância de AdaptadorPassagem.

    Uso:
        RegistroAdaptadores.registrar("rapido_norte", AdaptadorRapidoNorte())
        adaptador = RegistroAdaptadores.obter("rapido_norte")
    """

    _adaptadores: dict[str, AdaptadorPassagem] = {}

    @classmethod
    def registrar(cls, chave: str, adaptador: AdaptadorPassagem) -> None:
        """Registra um adaptador para a chave informada."""
        if not isinstance(adaptador, AdaptadorPassagem):
            raise TypeError(f"Adaptador deve herdar de AdaptadorPassagem, recebeu {type(adaptador)}")
        cls._adaptadores[chave] = adaptador

    @classmethod
    def obter(cls, chave: str) -> AdaptadorPassagem:
        """
        Retorna o adaptador registrado para a chave.
        Lança KeyError com mensagem amigável se não encontrado.
        """
        if chave not in cls._adaptadores:
            disponiveis = list(cls._adaptadores.keys())
            raise KeyError(
                f"Nenhum adaptador registrado para '{chave}'. "
                f"Empresas disponíveis: {disponiveis}"
            )
        return cls._adaptadores[chave]

    @classmethod
    def listar(cls) -> list[str]:
        """Retorna a lista de chaves registradas."""
        return list(cls._adaptadores.keys())


# ---------------------------------------------------------------------------
# Registro das empresas conhecidas
# Adicionar nova empresa: importar adaptador + chamar registrar() aqui.
# ---------------------------------------------------------------------------

from adaptadores.rapido_norte import AdaptadorRapidoNorte
from adaptadores.expresso_brasil import AdaptadorExpressoBrasil
from adaptadores.viacao_sol import AdaptadorViacaoSol
from adaptadores.regional import AdaptadorRegional  # Desafio Extra

RegistroAdaptadores.registrar("rapido_norte",    AdaptadorRapidoNorte())
RegistroAdaptadores.registrar("expresso_brasil", AdaptadorExpressoBrasil())
RegistroAdaptadores.registrar("viacao_sol",      AdaptadorViacaoSol())
RegistroAdaptadores.registrar("regional",  AdaptadorRegional())  # Desafio Extra
