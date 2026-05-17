"""
Testes automatizados da plataforma de passagens.

Execute com:
    cd bus_platform
    python -m pytest tests/ -v
    # ou diretamente:
    python tests/test_integracao.py
"""

import sys
import os
import unittest
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.integracao_service import IntegracaoService
from models.passagem import Passagem
from utils.parsers import parse_datetime, parse_valor, centavos_para_reais
from adaptadores.rapido_norte import AdaptadorRapidoNorte
from adaptadores.expresso_brasil import AdaptadorExpressoBrasil
from adaptadores.viacao_sol import AdaptadorViacaoSol
from adaptadores.regional import AdaptadorTransNordeste


class TestAdaptadorRapidoNorte(unittest.TestCase):
    """Testes do adaptador da Empresa A."""

    def setUp(self):
        self.adaptador = AdaptadorRapidoNorte()
        self.payload_valido = {
            "empresa": "Rapido Norte",
            "origem": "Fortaleza",
            "destino": "Recife",
            "saida": "2026-06-10 08:00",
            "chegada": "2026-06-10 18:30",
            "valor": 199.90,
        }

    def test_converte_payload_valido(self):
        passagem = self.adaptador.adaptar(self.payload_valido)
        self.assertIsInstance(passagem, Passagem)
        self.assertEqual(passagem.empresa, "Rapido Norte")
        self.assertEqual(passagem.origem, "Fortaleza")
        self.assertEqual(passagem.destino, "Recife")
        self.assertEqual(passagem.valor, 199.90)

    def test_horarios_convertidos_corretamente(self):
        passagem = self.adaptador.adaptar(self.payload_valido)
        self.assertIsInstance(passagem.horario_saida, datetime)
        self.assertIsInstance(passagem.horario_chegada, datetime)
        self.assertEqual(passagem.horario_saida, datetime(2026, 6, 10, 8, 0))
        self.assertEqual(passagem.horario_chegada, datetime(2026, 6, 10, 18, 30))

    def test_campo_ausente_lanca_value_error(self):
        payload_incompleto = {k: v for k, v in self.payload_valido.items() if k != "saida"}
        with self.assertRaises(ValueError):
            self.adaptador.adaptar(payload_incompleto)

    def test_empresa_suportada(self):
        self.assertEqual(self.adaptador.empresa_suportada(), "rapido_norte")


class TestAdaptadorExpressoBrasil(unittest.TestCase):
    """Testes do adaptador da Empresa B."""

    def setUp(self):
        self.adaptador = AdaptadorExpressoBrasil()
        self.payload_valido = {
            "nome_empresa": "Expresso Brasil",
            "cidade_origem": "Fortaleza",
            "cidade_destino": "Natal",
            "horario_saida": "2026-06-11T07:00:00",
            "horario_chegada": "2026-06-11T15:20:00",
            "preco_passagem": {"valor": 149.50, "moeda": "BRL"},
        }

    def test_converte_payload_valido(self):
        passagem = self.adaptador.adaptar(self.payload_valido)
        self.assertIsInstance(passagem, Passagem)
        self.assertEqual(passagem.empresa, "Expresso Brasil")
        self.assertEqual(passagem.origem, "Fortaleza")
        self.assertEqual(passagem.destino, "Natal")
        self.assertAlmostEqual(passagem.valor, 149.50)

    def test_valor_extraido_de_objeto_aninhado(self):
        passagem = self.adaptador.adaptar(self.payload_valido)
        self.assertEqual(passagem.valor, 149.50)

    def test_data_iso8601_com_T_parseada(self):
        passagem = self.adaptador.adaptar(self.payload_valido)
        self.assertEqual(passagem.horario_saida, datetime(2026, 6, 11, 7, 0, 0))
        self.assertEqual(passagem.horario_chegada, datetime(2026, 6, 11, 15, 20, 0))

    def test_campo_preco_ausente_lanca_value_error(self):
        payload_sem_preco = {k: v for k, v in self.payload_valido.items() if k != "preco_passagem"}
        with self.assertRaises(ValueError):
            self.adaptador.adaptar(payload_sem_preco)


class TestAdaptadorViacaoSol(unittest.TestCase):
    """Testes do adaptador da Empresa C."""

    def setUp(self):
        self.adaptador = AdaptadorViacaoSol()
        self.payload_valido = {
            "viacao": "Viacao Sol",
            "rota": {"inicio": "Fortaleza", "fim": "Joao Pessoa"},
            "horarios": {"saida": "10/06/2026 21:00", "chegada": "11/06/2026 05:45"},
            "valor_centavos": 25990,
        }

    def test_converte_payload_valido(self):
        passagem = self.adaptador.adaptar(self.payload_valido)
        self.assertIsInstance(passagem, Passagem)
        self.assertEqual(passagem.empresa, "Viacao Sol")
        self.assertEqual(passagem.origem, "Fortaleza")
        self.assertEqual(passagem.destino, "Joao Pessoa")

    def test_valor_centavos_convertido_para_reais(self):
        passagem = self.adaptador.adaptar(self.payload_valido)
        self.assertAlmostEqual(passagem.valor, 259.90)

    def test_data_formato_br_parseada(self):
        passagem = self.adaptador.adaptar(self.payload_valido)
        self.assertEqual(passagem.horario_saida, datetime(2026, 6, 10, 21, 0))
        self.assertEqual(passagem.horario_chegada, datetime(2026, 6, 11, 5, 45))

    def test_rota_aninhada_ausente_lanca_value_error(self):
        payload_sem_rota = {k: v for k, v in self.payload_valido.items() if k != "rota"}
        with self.assertRaises(ValueError):
            self.adaptador.adaptar(payload_sem_rota)

    def test_rota_sem_campo_inicio_lanca_value_error(self):
        payload = {**self.payload_valido, "rota": {"fim": "Joao Pessoa"}}
        with self.assertRaises(ValueError):
            self.adaptador.adaptar(payload)


class TestAdaptadorTransNordeste(unittest.TestCase):
    """Testes do adaptador da Empresa D (Desafio Extra)."""

    def setUp(self):
        self.adaptador = AdaptadorTransNordeste()
        self.payload_valido = {
            "transportadora": "TransNordeste",
            "partida": {"cidade": "Fortaleza", "timestamp": "1749560400"},
            "chegada": {"cidade": "Teresina", "timestamp": "1749582000"},
            "tarifa_brl": "189,90",
        }

    def test_converte_payload_valido(self):
        passagem = self.adaptador.adaptar(self.payload_valido)
        self.assertIsInstance(passagem, Passagem)
        self.assertEqual(passagem.empresa, "TransNordeste")
        self.assertEqual(passagem.origem, "Fortaleza")
        self.assertEqual(passagem.destino, "Teresina")

    def test_tarifa_string_br_convertida(self):
        passagem = self.adaptador.adaptar(self.payload_valido)
        self.assertAlmostEqual(passagem.valor, 189.90)

    def test_timestamp_unix_convertido(self):
        passagem = self.adaptador.adaptar(self.payload_valido)
        self.assertIsInstance(passagem.horario_saida, datetime)
        self.assertIsInstance(passagem.horario_chegada, datetime)

    def test_timestamp_invalido_lanca_value_error(self):
        payload = {**self.payload_valido, "partida": {"cidade": "X", "timestamp": "nao-e-numero"}}
        with self.assertRaises(ValueError):
            self.adaptador.adaptar(payload)


class TestIntegracaoService(unittest.TestCase):
    """Testes de integração via IntegracaoService."""

    def setUp(self):
        self.service = IntegracaoService()

    def test_empresas_disponiveis_nao_vazio(self):
        empresas = self.service.empresas_disponiveis()
        self.assertIsInstance(empresas, list)
        self.assertGreater(len(empresas), 0)

    def test_converter_rapido_norte(self):
        payload = {
            "empresa": "Rapido Norte",
            "origem": "Fortaleza",
            "destino": "Recife",
            "saida": "2026-06-10 08:00",
            "chegada": "2026-06-10 18:30",
            "valor": 199.90,
        }
        passagem = self.service.converter("rapido_norte", payload)
        self.assertIsInstance(passagem, Passagem)

    def test_empresa_nao_registrada_lanca_key_error(self):
        with self.assertRaises(KeyError):
            self.service.converter("empresa_inexistente", {})

    def test_payload_invalido_tipo_errado_lanca_type_error(self):
        with self.assertRaises(TypeError):
            self.service.converter("rapido_norte", "payload_string")

    def test_payload_com_campos_ausentes_lanca_value_error(self):
        with self.assertRaises(ValueError):
            self.service.converter("rapido_norte", {"empresa": "X"})

    def test_to_dict_retorna_campos_corretos(self):
        payload = {
            "empresa": "Rapido Norte",
            "origem": "Fortaleza",
            "destino": "Recife",
            "saida": "2026-06-10 08:00",
            "chegada": "2026-06-10 18:30",
            "valor": 199.90,
        }
        passagem = self.service.converter("rapido_norte", payload)
        d = passagem.to_dict()
        self.assertIn("empresa", d)
        self.assertIn("origem", d)
        self.assertIn("destino", d)
        self.assertIn("horario_saida", d)
        self.assertIn("horario_chegada", d)
        self.assertIn("valor", d)


class TestParsers(unittest.TestCase):
    """Testes unitários dos utilitários de parsing."""

    def test_parse_datetime_formato_simples(self):
        dt = parse_datetime("2026-06-10 08:00")
        self.assertEqual(dt, datetime(2026, 6, 10, 8, 0))

    def test_parse_datetime_iso8601(self):
        dt = parse_datetime("2026-06-11T07:00:00")
        self.assertEqual(dt, datetime(2026, 6, 11, 7, 0, 0))

    def test_parse_datetime_formato_br(self):
        dt = parse_datetime("10/06/2026 21:00")
        self.assertEqual(dt, datetime(2026, 6, 10, 21, 0))

    def test_parse_datetime_formato_invalido_lanca_value_error(self):
        with self.assertRaises(ValueError):
            parse_datetime("formato-invalido")

    def test_parse_datetime_tipo_errado_lanca_type_error(self):
        with self.assertRaises(TypeError):
            parse_datetime(12345)

    def test_parse_valor_float_direto(self):
        self.assertAlmostEqual(parse_valor(199.90), 199.90)

    def test_parse_valor_dict(self):
        self.assertAlmostEqual(parse_valor({"valor": 149.50, "moeda": "BRL"}), 149.50)

    def test_parse_valor_dict_sem_chave_lanca_value_error(self):
        with self.assertRaises(ValueError):
            parse_valor({"preco": 100})

    def test_centavos_para_reais(self):
        self.assertAlmostEqual(centavos_para_reais(25990), 259.90)

    def test_centavos_para_reais_tipo_errado(self):
        with self.assertRaises(TypeError):
            centavos_para_reais("nao-numero")


if __name__ == "__main__":
    unittest.main(verbosity=2)
