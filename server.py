from fastmcp import FastMCP
from typing import Annotated

mcp = FastMCP(
    "Calculadora Alcool x Gasolina",
    instructions="Ajuda a decidir qual combustivel compensa mais: alcool ou gasolina, baseado no consumo real do seu veiculo."
)


def calcular_combustivel_interno(km_l_gasolina: float, preco_gasolina: float,
                                  km_l_alcool: float, preco_alcool: float) -> dict:
    """Calcula qual combustivel compensa mais."""

    if km_l_gasolina <= 0 or preco_gasolina <= 0 or km_l_alcool <= 0 or preco_alcool <= 0:
        raise ValueError("Todos os valores devem ser maiores que zero")

    custo_por_km_gasolina = preco_gasolina / km_l_gasolina
    custo_por_km_alcool = preco_alcool / km_l_alcool

    compensa_mais = "Alcool" if custo_por_km_alcool < custo_por_km_gasolina else "Gasolina"
    economia = abs(custo_por_km_gasolina - custo_por_km_alcool)
    porcentagem_economia = (economia / max(custo_por_km_gasolina, custo_por_km_alcool)) * 100

    ponto_equilibrio = (km_l_alcool / km_l_gasolina) * 100
    preco_equilibrio_alcool = preco_gasolina * (km_l_alcool / km_l_gasolina)

    return {
        "compensa_mais": compensa_mais,
        "custo_por_km_gasolina": round(custo_por_km_gasolina, 4),
        "custo_por_km_alcool": round(custo_por_km_alcool, 4),
        "economia_por_km": round(economia, 4),
        "porcentagem_economia": round(porcentagem_economia, 2),
        "ponto_equilibrio_porcentagem": round(ponto_equilibrio, 2),
        "preco_equilibrio_alcool": round(preco_equilibrio_alcool, 2),
        "recomendacao": f"Compensa abastecer com {compensa_mais}. Voce economiza R$ {economia:.4f} por km rodado.",
        "detalhes": f"O alcool compensa ate R$ {preco_equilibrio_alcool:.2f} ({ponto_equilibrio:.1f}% do preco da gasolina)."
    }


@mcp.tool()
def calcular_combustivel(
    km_l_gasolina: Annotated[float, "Quantos km seu carro faz por litro de GASOLINA. Exemplo: 12.5"],
    preco_gasolina: Annotated[float, "Preco atual da GASOLINA no posto (R$/litro). Exemplo: 5.89"],
    km_l_alcool: Annotated[float, "Quantos km seu carro faz por litro de ALCOOL. Exemplo: 8.5"],
    preco_alcool: Annotated[float, "Preco atual do ALCOOL no posto (R$/litro). Exemplo: 3.79"]
) -> dict:
    """
    Descobre qual combustivel compensa mais: ALCOOL ou GASOLINA.

    Compara o custo por km rodado de cada combustivel, usando o consumo real do seu carro.

    COMO USAR:
    1. Informe quantos km/L seu carro faz com gasolina (ex: 12.5)
    2. Informe o preco da gasolina no posto (ex: 5.89)
    3. Informe quantos km/L seu carro faz com alcool (ex: 8.5)
    4. Informe o preco do alcool no posto (ex: 3.79)

    EXEMPLO PRATICO:
    - Gasolina: 12.5 km/L a R$ 5.89
    - Alcool: 8.5 km/L a R$ 3.79
    - Resultado: Alcool compensa! Economia de 5.8% por km
    """
    return calcular_combustivel_interno(km_l_gasolina, preco_gasolina, km_l_alcool, preco_alcool)


@mcp.tool()
def calcular_economia_mensal(
    km_l_gasolina: Annotated[float, "km/L com gasolina. Exemplo: 12.5"],
    preco_gasolina: Annotated[float, "Preco gasolina R$/L. Exemplo: 5.89"],
    km_l_alcool: Annotated[float, "km/L com alcool. Exemplo: 8.5"],
    preco_alcool: Annotated[float, "Preco alcool R$/L. Exemplo: 3.79"],
    km_mensal: Annotated[float, "Quantos km voce roda por MES. Exemplo: 1500"]
) -> dict:
    """
    Calcula quanto voce ECONOMIZA por mes e por ano escolhendo o combustivel certo.

    Informe quantos km voce roda por mes e descubra:
    - Custo mensal com gasolina vs alcool
    - Economia mensal em reais
    - Economia anual em reais

    EXEMPLO PRATICO:
    - Carro: 12.5 km/L gasolina, 8.5 km/L alcool
    - Precos: Gasolina R$ 5.89, Alcool R$ 3.79
    - Rodando 1500 km/mes
    - Resultado: Economia de R$ 47/mes = R$ 564/ano com alcool!
    """
    resultado = calcular_combustivel_interno(km_l_gasolina, preco_gasolina, km_l_alcool, preco_alcool)

    custo_mensal_gasolina = (km_mensal / km_l_gasolina) * preco_gasolina
    custo_mensal_alcool = (km_mensal / km_l_alcool) * preco_alcool
    economia_mensal = abs(custo_mensal_gasolina - custo_mensal_alcool)
    economia_anual = economia_mensal * 12

    litros_gasolina_mes = km_mensal / km_l_gasolina
    litros_alcool_mes = km_mensal / km_l_alcool

    return {
        **resultado,
        "km_mensal": km_mensal,
        "consumo_mensal": {
            "litros_gasolina": round(litros_gasolina_mes, 1),
            "litros_alcool": round(litros_alcool_mes, 1)
        },
        "custo_mensal_gasolina": round(custo_mensal_gasolina, 2),
        "custo_mensal_alcool": round(custo_mensal_alcool, 2),
        "economia_mensal": round(economia_mensal, 2),
        "economia_anual": round(economia_anual, 2),
        "resumo": f"Rodando {km_mensal} km/mes, voce economiza R$ {economia_mensal:.2f}/mes (R$ {economia_anual:.2f}/ano) abastecendo com {resultado['compensa_mais']}."
    }


@mcp.tool()
def simular_abastecimento(
    km_l_gasolina: Annotated[float, "km/L com gasolina. Exemplo: 12.5"],
    preco_gasolina: Annotated[float, "Preco gasolina R$/L. Exemplo: 5.89"],
    km_l_alcool: Annotated[float, "km/L com alcool. Exemplo: 8.5"],
    preco_alcool: Annotated[float, "Preco alcool R$/L. Exemplo: 3.79"],
    valor_abastecimento: Annotated[float, "Quanto voce vai gastar em R$. Exemplo: 200"]
) -> dict:
    """
    Simula quantos KM voce roda gastando um valor especifico.

    Descubra qual combustivel rende mais km para o seu dinheiro!

    EXEMPLO PRATICO:
    - Voce tem R$ 200 para abastecer
    - Com gasolina: roda 424 km
    - Com alcool: roda 449 km
    - Resultado: Alcool rende 25 km a mais!
    """
    litros_gasolina = valor_abastecimento / preco_gasolina
    litros_alcool = valor_abastecimento / preco_alcool

    km_gasolina = litros_gasolina * km_l_gasolina
    km_alcool = litros_alcool * km_l_alcool

    melhor = "Gasolina" if km_gasolina > km_alcool else "Alcool"
    diferenca_km = abs(km_gasolina - km_alcool)

    return {
        "valor_abastecimento": valor_abastecimento,
        "gasolina": {
            "litros": round(litros_gasolina, 2),
            "autonomia_km": round(km_gasolina, 1),
            "custo_por_km": round(valor_abastecimento / km_gasolina, 4)
        },
        "alcool": {
            "litros": round(litros_alcool, 2),
            "autonomia_km": round(km_alcool, 1),
            "custo_por_km": round(valor_abastecimento / km_alcool, 4)
        },
        "melhor_opcao": melhor,
        "diferenca_km": round(diferenca_km, 1),
        "resumo": f"Com R$ {valor_abastecimento:.2f}: Gasolina = {km_gasolina:.0f} km | Alcool = {km_alcool:.0f} km. {melhor} rende {diferenca_km:.0f} km a mais!"
    }


@mcp.tool()
def dicas_economia() -> dict:
    """
    Dicas para economizar combustivel e a famosa REGRA DOS 70%.

    Retorna:
    - Como saber se alcool compensa (regra dos 70%)
    - Tabela de consumo medio por tipo de carro
    - 6 dicas praticas para economizar

    Use quando quiser aprender a economizar ou nao souber o consumo do seu carro.
    """
    return {
        "regra_dos_70_porcento": {
            "explicacao": "Divida o preco do ALCOOL pelo preco da GASOLINA. Se der MENOS que 0.70, compensa ALCOOL!",
            "formula": "preco_alcool / preco_gasolina < 0.70 = ALCOOL",
            "exemplo": {
                "gasolina": "R$ 5.89",
                "alcool": "R$ 3.79",
                "calculo": "3.79 / 5.89 = 0.64 (64%)",
                "resultado": "64% < 70% = Compensa ALCOOL!"
            },
            "importante": "Essa regra e uma MEDIA. O calculo exato depende do consumo do SEU carro."
        },
        "consumo_medio_por_carro": {
            "hatch_popular": {"gasolina": "12-14 km/L", "alcool": "8-10 km/L", "exemplos": "Onix, HB20, Argo"},
            "sedan_medio": {"gasolina": "10-12 km/L", "alcool": "7-9 km/L", "exemplos": "Corolla, Civic, Cruze"},
            "suv_compacto": {"gasolina": "9-11 km/L", "alcool": "6-8 km/L", "exemplos": "Creta, Compass, T-Cross"},
            "suv_grande": {"gasolina": "7-9 km/L", "alcool": "5-7 km/L", "exemplos": "SW4, Amarok, Ranger"}
        },
        "dicas_para_economizar": [
            {"dica": "Calibre os pneus toda semana", "economia": "ate 10%"},
            {"dica": "Evite aceleracoes bruscas", "economia": "ate 20%"},
            {"dica": "Use o ar-condicionado com moderacao", "economia": "ate 15%"},
            {"dica": "Retire peso desnecessario do carro", "economia": "ate 5%"},
            {"dica": "Faca manutencao em dia (filtros, velas, oleo)", "economia": "ate 10%"},
            {"dica": "Planeje rotas para evitar transito", "economia": "ate 15%"}
        ],
        "como_descobrir_consumo_do_seu_carro": [
            "1. Encha o tanque completamente",
            "2. Zere o hodometro parcial",
            "3. Rode normalmente ate precisar abastecer",
            "4. Encha o tanque novamente e anote os litros",
            "5. Divida os km rodados pelos litros abastecidos",
            "Exemplo: 450 km / 38 litros = 11.8 km/L"
        ]
    }
