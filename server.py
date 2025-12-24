from fastmcp import FastMCP

mcp = FastMCP("calculadora-alcool-gasolina")


def calcular_combustivel_interno(km_l_gasolina: float, preco_gasolina: float,
                                  km_l_alcool: float, preco_alcool: float) -> dict:
    """Calcula qual combustivel compensa mais."""

    # Validacao
    if km_l_gasolina <= 0 or preco_gasolina <= 0 or km_l_alcool <= 0 or preco_alcool <= 0:
        raise ValueError("Todos os valores devem ser maiores que zero")

    # Custo por km
    custo_por_km_gasolina = preco_gasolina / km_l_gasolina
    custo_por_km_alcool = preco_alcool / km_l_alcool

    # Qual compensa mais
    compensa_mais = "Alcool" if custo_por_km_alcool < custo_por_km_gasolina else "Gasolina"
    economia = abs(custo_por_km_gasolina - custo_por_km_alcool)
    porcentagem_economia = (economia / max(custo_por_km_gasolina, custo_por_km_alcool)) * 100

    # Ponto de equilibrio
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
    km_l_gasolina: float,
    preco_gasolina: float,
    km_l_alcool: float,
    preco_alcool: float
) -> dict:
    """Calcula qual combustivel compensa mais: alcool ou gasolina.
    Compara o custo por quilometro de cada combustivel baseado no consumo do veiculo.

    Use this when user wants to know which fuel is better, compare alcohol vs gasoline,
    or calculate fuel efficiency.

    Args:
        km_l_gasolina: Consumo do veiculo com gasolina em km/litro (ex: 12.5)
        preco_gasolina: Preco da gasolina em reais por litro (ex: 5.49)
        km_l_alcool: Consumo do veiculo com alcool em km/litro (ex: 8.8)
        preco_alcool: Preco do alcool em reais por litro (ex: 3.79)
    """

    return calcular_combustivel_interno(km_l_gasolina, preco_gasolina, km_l_alcool, preco_alcool)


@mcp.tool()
def calcular_economia_mensal(
    km_l_gasolina: float,
    preco_gasolina: float,
    km_l_alcool: float,
    preco_alcool: float,
    km_mensal: float
) -> dict:
    """Calcula a economia mensal ao escolher o combustivel mais vantajoso.
    Baseado na quilometragem rodada por mes.

    Use this when user wants to know monthly or yearly savings on fuel.

    Args:
        km_l_gasolina: Consumo do veiculo com gasolina em km/litro (ex: 12.5)
        preco_gasolina: Preco da gasolina em reais por litro (ex: 5.49)
        km_l_alcool: Consumo do veiculo com alcool em km/litro (ex: 8.8)
        preco_alcool: Preco do alcool em reais por litro (ex: 3.79)
        km_mensal: Quilometragem rodada por mes (ex: 1000)
    """

    resultado = calcular_combustivel_interno(km_l_gasolina, preco_gasolina, km_l_alcool, preco_alcool)

    # Custos mensais
    custo_mensal_gasolina = (km_mensal / km_l_gasolina) * preco_gasolina
    custo_mensal_alcool = (km_mensal / km_l_alcool) * preco_alcool
    economia_mensal = abs(custo_mensal_gasolina - custo_mensal_alcool)
    economia_anual = economia_mensal * 12

    # Litros consumidos por mes
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
    km_l_gasolina: float,
    preco_gasolina: float,
    km_l_alcool: float,
    preco_alcool: float,
    valor_abastecimento: float
) -> dict:
    """Simula quanto voce roda com um valor de abastecimento.
    Compara a autonomia entre alcool e gasolina para o mesmo valor gasto.

    Use this when user wants to know how far they can go with a specific amount of money.

    Args:
        km_l_gasolina: Consumo do veiculo com gasolina em km/litro (ex: 12.5)
        preco_gasolina: Preco da gasolina em reais por litro (ex: 5.49)
        km_l_alcool: Consumo do veiculo com alcool em km/litro (ex: 8.8)
        preco_alcool: Preco do alcool em reais por litro (ex: 3.79)
        valor_abastecimento: Valor em reais para abastecer (ex: 100)
    """

    # Litros comprados
    litros_gasolina = valor_abastecimento / preco_gasolina
    litros_alcool = valor_abastecimento / preco_alcool

    # Autonomia (km que roda)
    km_gasolina = litros_gasolina * km_l_gasolina
    km_alcool = litros_alcool * km_l_alcool

    # Qual rende mais
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
        "resumo": f"Com R$ {valor_abastecimento:.2f}, voce roda {km_gasolina:.1f} km com gasolina ou {km_alcool:.1f} km com alcool. {melhor} rende {diferenca_km:.1f} km a mais."
    }


@mcp.tool()
def dicas_economia() -> dict:
    """Retorna dicas para economizar combustivel e informacoes uteis.

    Use this when user asks for tips on saving fuel or fuel economy advice."""

    return {
        "regra_de_ouro": "O alcool compensa quando seu preco for ate 70% do preco da gasolina (considerando consumo medio)",
        "como_calcular": "Divida o preco do alcool pelo preco da gasolina. Se der menos que 0.70, compensa alcool.",
        "exemplo": {
            "gasolina": 5.99,
            "alcool": 3.89,
            "calculo": "3.89 / 5.99 = 0.65 (65%)",
            "resultado": "Compensa ALCOOL pois 65% < 70%"
        },
        "dicas": [
            {
                "titulo": "Conheca seu carro",
                "descricao": "Cada veiculo tem consumo diferente. Anote a quilometragem e litros abastecidos para calcular seu consumo real."
            },
            {
                "titulo": "Pneus calibrados",
                "descricao": "Pneus murchos aumentam o consumo em ate 10%. Calibre semanalmente."
            },
            {
                "titulo": "Direcao suave",
                "descricao": "Aceleracoes e freadas bruscas aumentam o consumo em ate 20%."
            },
            {
                "titulo": "Ar-condicionado",
                "descricao": "O AC pode aumentar o consumo em 10-20%. Use com moderacao."
            },
            {
                "titulo": "Peso extra",
                "descricao": "Cada 50kg extras aumentam o consumo em cerca de 2%."
            },
            {
                "titulo": "Manutencao em dia",
                "descricao": "Filtros sujos, velas gastas e oleo vencido prejudicam a eficiencia."
            }
        ],
        "consumo_medio_referencia": {
            "carro_popular": {"gasolina": "12-14 km/L", "alcool": "8-10 km/L"},
            "sedan_medio": {"gasolina": "10-12 km/L", "alcool": "7-9 km/L"},
            "suv": {"gasolina": "8-10 km/L", "alcool": "6-8 km/L"}
        }
    }
