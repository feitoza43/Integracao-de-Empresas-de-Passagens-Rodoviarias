# Plataforma de Passagens de Ônibus 🚌

Solução de integração com múltiplos provedores de passagens, convertendo
formatos heterogêneos de APIs externas para um modelo interno padronizado.

---

## Estrutura do Projeto

```
bus_platform/
├── main.py                          # Demonstração de execução
├── models/
│   └── passagem.py                  # Modelo interno padronizado
├── adaptadores/
│   ├── base.py                      # Contrato (interface abstrata)
│   ├── registro.py                  # Registry + Factory de adaptadores
│   ├── rapido_norte.py              # Empresa A
│   ├── expresso_brasil.py           # Empresa B
│   ├── viacao_sol.py                # Empresa C
│   └── regional.py                  # Empresa D (Desafio Extra — Regional)
├── services/
│   └── integracao_service.py        # Orquestrador principal
├── utils/
│   └── parsers.py                   # Helpers de data e valor monetário
└── tests/
    └── test_integracao.py           # Testes automatizados
```

---

## Como Executar

```bash
# Demonstração completa
cd bus_platform
python main.py

# Testes automatizados
python -m pytest tests/ -v
# ou
python tests/test_integracao.py
```

---

## Decisões de Arquitetura

### 1. Padrão Adapter (GoF)
Cada empresa externa tem seu próprio `AdaptadorXxx`, responsável por
traduzir o payload bruto para o modelo `Passagem`. Isso isola completamente
o "dialeto" de cada API do restante da aplicação.

### 2. Open/Closed Principle (SOLID — OCP)
O código principal (`IntegracaoService`) está **fechado para modificação**
e **aberto para extensão**. Adicionar uma nova empresa requer apenas:
1. Criar `adaptadores/nova_empresa.py` herdando de `AdaptadorPassagem`;
2. Registrá-la em `adaptadores/registro.py` com uma linha.

Nenhum outro arquivo precisa ser tocado.

### 3. Registry Pattern
`RegistroAdaptadores` é um dicionário centralizado `chave → adaptador`.
O `IntegracaoService` pergunta ao registro qual adaptador usar —
nunca instancia nem conhece adaptadores diretamente.
Isso aplica o **Dependency Inversion Principle (DIP)**: o serviço depende
da abstração (`AdaptadorPassagem`), não de implementações concretas.

### 4. Single Responsibility Principle (SRP)
| Componente | Responsabilidade única |
|---|---|
| `Passagem` | Estrutura de dados interna |
| `AdaptadorXxx` | Mapeamento do formato de uma empresa |
| `RegistroAdaptadores` | Descoberta de adaptadores por chave |
| `IntegracaoService` | Orquestração do fluxo |
| `parsers.py` | Normalização de datas e valores |

### 5. Padronização de Datas e Valores
`utils/parsers.py` centraliza a lógica de conversão:
- **Datas**: tenta múltiplos formatos sequencialmente (ISO-8601, BR, Unix timestamp);
- **Valores**: suporta float direto, objeto `{"valor": X}` e centavos inteiros.

Qualquer novo formato de data/valor é adicionado apenas neste arquivo.

### 6. Tratamento de Payload Inválido
Cada adaptador valida campos obrigatórios via `_validar_campos()` (método
do template na classe base), lançando `ValueError` descritivo com os campos
ausentes. Erros de tipo lançam `TypeError`.

---

## Exemplo de Saída

```
============================================================
  Empresas registradas na plataforma
============================================================
  ['rapido_norte', 'expresso_brasil', 'viacao_sol', 'regional']

============================================================
  Empresa A — Viação Rápido Norte
============================================================
  Objeto : Passagem(empresa='Rapido Norte', origem='Fortaleza', destino='Recife', saida='2026-06-10 08:00:00', chegada='2026-06-10 18:30:00', valor=R$199.90)

...

============================================================
  Empresa D — Regional (Desafio Extra)
============================================================
  Objeto : Passagem(empresa='Regional', origem='Fortaleza', destino='Teresina', saida='...', chegada='...', valor=R$189.90)

...

============================================================
  Tratamento de payload inválido
============================================================
[1] Empresa não registrada:
  KeyError capturado → "Nenhum adaptador registrado para 'empresa_fantasma'. ..."

[2] Payload com campos ausentes (Rápido Norte):
  ValueError capturado → "[rapido_norte] Campos obrigatórios ausentes no payload: ['saida', 'chegada', 'valor']. ..."
```

---

## Adicionando Nova Empresa (Exemplo)

```python
# 1. Criar adaptadores/nova_empresa.py
from adaptadores.base import AdaptadorPassagem
from models.passagem import Passagem
from utils.parsers import parse_datetime, parse_valor

class AdaptadorNovaEmpresa(AdaptadorPassagem):
    def empresa_suportada(self):
        return "nova_empresa"

    def adaptar(self, payload):
        self._validar_campos(payload, ["nome", "de", "para", "saida", "chegada", "preco"])
        return Passagem(
            empresa=payload["nome"],
            origem=payload["de"],
            destino=payload["para"],
            horario_saida=parse_datetime(payload["saida"]),
            horario_chegada=parse_datetime(payload["chegada"]),
            valor=parse_valor(payload["preco"]),
        )

# 2. Registrar em adaptadores/registro.py (apenas esta linha):
from adaptadores.nova_empresa import AdaptadorNovaEmpresa
RegistroAdaptadores.registrar("nova_empresa", AdaptadorNovaEmpresa())
```

**Nenhum outro arquivo precisa ser alterado.** ✅
