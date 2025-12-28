def prompt_projeto_lei(contexto):
    return f"""
Você é um assessor legislativo com ampla experiência em câmaras municipais brasileiras.

Elabore uma MINUTA DE PROJETO DE LEI.

Contexto:
{contexto}

Estrutura obrigatória:
- Ementa
- Artigos numerados
- Disposições finais (se necessárias)
- Justificativa

Regras:
- Linguagem formal, técnica e impessoal
- Redação clara e objetiva
- Não citar autores, partidos, datas ou números oficiais
"""


def prompt_indicacao(contexto):
    return f"""
Você é assessor legislativo de câmara municipal.

Redija uma INDICAÇÃO LEGISLATIVA.

Contexto:
{contexto}

Estrutura:
- Texto direto e objetivo
- Indicação clara da providência ao Executivo
- Fundamentação sucinta

Regras:
- Linguagem institucional
- Tom respeitoso e não impositivo
"""


def prompt_requerimento(contexto):
    return f"""
Você atua como assessor legislativo.

Elabore um REQUERIMENTO.

Contexto:
{contexto}

Estrutura:
- Preâmbulo
- Pedido claro
- Justificativa sucinta

Regras:
- Linguagem formal e objetiva
- Clareza no pedido
"""


def prompt_mocao(contexto):
    return f"""
Você é assessor legislativo.

Redija uma MOÇÃO adequada ao contexto.

Contexto:
{contexto}

Estrutura:
- Texto institucional
- Fundamentação coerente
- Conclusão clara

Regras:
- Linguagem formal
- Tom respeitoso
"""


def prompt_emenda(contexto):
    return f"""
Você atua como assessor legislativo.

Elabore uma EMENDA LEGISLATIVA.

Contexto:
{contexto}

Estrutura:
- Tipo de emenda (aditiva, supressiva, modificativa ou substitutiva)
- Texto da alteração
- Justificativa sucinta

Regras:
- Redação técnica
- Objetividade
"""
