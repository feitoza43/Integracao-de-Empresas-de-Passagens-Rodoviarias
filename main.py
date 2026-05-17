"""
Ponto de entrada da aplicação — demonstração das integrações.

Execute com:
    cd bus_platform
    python main.py

Os payloads das empresas A, B e C são carregados diretamente
dos arquivos JSON fornecidos pelas empresas parceiras.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from services.integracao_service import IntegracaoService

JSON_DIR = os.path.join(os.path.dirname(__file__), "data")


def carregar_json(nome_arquivo: str) -> dict:
    """Lê um arquivo JSON da pasta data/ e retorna o dicionário."""
    caminho = os.path.join(JSON_DIR, nome_arquivo)
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


PAYLOAD_REGIONAL = {
    "transportadora": "Regional",
    "partida": {
        "cidade": "Fortaleza",
        "timestamp": "1749560400",
    },
    "chegada": {
        "cidade": "Teresina",
        "timestamp": "1749582000",
    },
    "tarifa_brl": "189,90",
}


def separador(titulo: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}")


def main() -> None:
    service = IntegracaoService()

    separador("Empresas registradas na plataforma")
    print(f"  {service.empresas_disponiveis()}")

    cenarios = [
        ("rapido_norte",    carregar_json("Viação_Rápido_Norte.json"), "Empresa A — Viação Rápido Norte  [JSON externo]"),
        ("expresso_brasil", carregar_json("Expresso_Brasil.json"),     "Empresa B — Expresso Brasil       [JSON externo]"),
        ("viacao_sol",      carregar_json("Viação_Sol.json"),          "Empresa C — Viação Sol            [JSON externo]"),
        ("regional",  PAYLOAD_REGIONAL,                          "Empresa D — Regional              [Desafio Extra]"),
    ]

    for chave, payload, descricao in cenarios:
        separador(descricao)
        print(f"  Payload : {json.dumps(payload, ensure_ascii=False)}")
        passagem = service.converter(chave, payload)
        print(f"  Objeto  : {passagem}")
        print(f"  Dict    : {passagem.to_dict()}")

    separador("Tratamento de payload inválido")

    print("\n[1] Empresa não registrada:")
    try:
        service.converter("empresa_fantasma", {})
    except KeyError as e:
        print(f"  KeyError capturado → {e}")

    print("\n[2] Payload com campos ausentes (Rápido Norte):")
    try:
        service.converter("rapido_norte", {"empresa": "Fantasma"})
    except ValueError as e:
        print(f"  ValueError capturado → {e}")

    print("\n[3] Payload com tipo errado (não é dict):")
    try:
        service.converter("rapido_norte", "payload_errado") # type: ignore
    except TypeError as e:
        print(f"  TypeError capturado → {e}")

    separador("Execução concluída com sucesso!")


if __name__ == "__main__":
    main()
