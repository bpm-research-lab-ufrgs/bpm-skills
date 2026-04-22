import pandas as pd

# 1. Carregar os dados
caminho_arquivo = 'logs_INF01216 - U (232)_20260323-1019.xlsx'

try:
    df = pd.read_excel(caminho_arquivo)
except ValueError:
    df = pd.read_csv(caminho_arquivo)

# 2. Classificação de Eventos
eventos_ativos = [
    'Um envio foi submetido.',
    'Um arquivo foi enviado.',
    'Submissão criada.',
    'Tentativa do questionário entregue',
    'Post criado',
    'Discussão criada'
]

eventos_excluidos = ['Usuário recebeu nota', 'Lista de usuários vistos', 'Perfil do usuário visto']

# 3. Dicionário de Mapeamento Múltiplo (ATUALIZADO CONFORME ESPECIALISTA NEUTRO)
def mapear_habilidades(contexto):
    contexto = str(contexto).lower()
    habilidades = []

    # Projeto Etapa 1 -> H1_C1, H5_C1
    if 'etapa 1' in contexto:
        habilidades.extend(['h1', 'h5'])

    # Projeto Etapa 2 -> H1_C1, H2_C1, H4_C1, H9_C1
    if 'etapa 2' in contexto:
        habilidades.extend(['h1', 'h2', 'h4', 'h9'])

    # Projeto Etapa 3 -> H2_C1, H3_C1, H4_C1, H6_C1, H7_C1, H8_C1, H9_C1
    if 'etapa 3' in contexto:
        habilidades.extend(['h2', 'h3', 'h4', 'h6', 'h7', 'h8', 'h9'])

    # Seminário -> H5_C1
    if 'seminário' in contexto:
        habilidades.extend(['h5'])

    # Exercício de Descrição (MOD_1) -> H5_C1
    if 'exercício de descrição' in contexto:
        habilidades.extend(['h5'])

    # Questionários (1 e 2) (MOD_3) -> H2_C1, H9_C1
    if 'questionário' in contexto:
        habilidades.extend(['h2', 'h9'])

    # Uso da Camunda (MOD_3) -> H1_C1, H2_C1, H9_C1
    if 'camunda' in contexto:
        habilidades.extend(['h1', 'h2', 'h9'])

    # Prática 5 (MOD_4) -> H5_C1
    if 'prática 5' in contexto:
        habilidades.extend(['h5'])

    # Prática 7 (MOD_4) -> H5_C1
    if 'prática 7' in contexto:
        habilidades.extend(['h5'])

    # Prática 8 (MOD_4) -> H2_C1, H3_C1, H4_C1, H6_C1, H7_C1, H8_C1, H9_C1
    if 'prática 8' in contexto:
        habilidades.extend(['h2', 'h3', 'h4', 'h6', 'h7', 'h8', 'h9'])

    # NOTA: Prática 1 (Tarefas 1 e 2) não recebem if, pois mapeiam para "nenhuma", 
    # logo a lista retornará vazia e será filtrada abaixo.

    # Retorna a lista removendo possíveis duplicatas
    return list(set(habilidades))

# Aplica a função 
df['Habilidades_Lista'] = df['Contexto do Evento'].apply(mapear_habilidades)

# Filtra o ruído e remove eventos que não mapearam para nenhuma habilidade (listas vazias)
df_util = df[(df['Habilidades_Lista'].str.len() > 0) & (~df['Nome do evento'].isin(eventos_excluidos))].copy()

# O PULO DO GATO: Transforma a lista em múltiplas linhas independentes
df_util = df_util.explode('Habilidades_Lista')
df_util = df_util.rename(columns={'Habilidades_Lista': 'Habilidade'})

# 4. Cria a coluna indicando o TIPO de rastro e agrega os dados
df_util['Tipo_Rastro'] = df_util['Nome do evento'].apply(lambda x: 'Ativo (Proficiência)' if x in eventos_ativos else 'Passivo (Engajamento)')

# Agrupando Ativos
df_ativos = df_util[df_util['Tipo_Rastro'] == 'Ativo (Proficiência)']
resumo_ativos = df_ativos.groupby('Habilidade').agg(
    Evidencias_Ativas=('Nome do evento', 'count'),
    Alunos_Ativos=('Nome completo', 'nunique')
).reset_index()

# Agrupando Passivos
df_passivos = df_util[df_util['Tipo_Rastro'] == 'Passivo (Engajamento)']
resumo_passivos = df_passivos.groupby('Habilidade').agg(
    Engajamento_Passivo=('Nome do evento', 'count'),
    Alunos_Passivos=('Nome completo', 'nunique')
).reset_index()

# Mesclando os dois resumos
resumo_final = pd.merge(resumo_ativos, resumo_passivos, on='Habilidade', how='outer').fillna(0)

# Convertendo para inteiros
colunas_int = ['Evidencias_Ativas', 'Alunos_Ativos', 'Engajamento_Passivo', 'Alunos_Passivos']
resumo_final[colunas_int] = resumo_final[colunas_int].astype(int)

# Ordenando
resumo_final = resumo_final.sort_values(by='Evidencias_Ativas', ascending=False)

# 5. Análise de Lacunas (Gaps)
todas_habilidades = {f'h{i}' for i in range(1, 11)}
habilidades_encontradas = set(resumo_final['Habilidade'].unique())
gaps = todas_habilidades - habilidades_encontradas

df_gaps = pd.DataFrame({'Habilidades_Sem_Cobertura': list(gaps)})
if df_gaps.empty:
    df_gaps = pd.DataFrame({'Habilidades_Sem_Cobertura': ['Nenhuma lacuna encontrada.']})

# 6. Exportação
nome_arquivo_saida = 'evidencias_framework_moodle_novo_mapeamento.xlsx'

with pd.ExcelWriter(nome_arquivo_saida, engine='openpyxl') as writer:
    resumo_final.to_excel(writer, sheet_name='Analise_Habilidades', index=False)
    df_gaps.to_excel(writer, sheet_name='Analise_Gaps', index=False)

print(f"Análise de mapeamento múltiplo concluída com sucesso!")
print(f"Resultados salvos em: {nome_arquivo_saida}")
print("\n=== PRÉVIA DOS RESULTADOS ===")
print(resumo_final.to_string(index=False))
