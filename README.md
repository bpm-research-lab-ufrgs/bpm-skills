# BPM Skills

**Research project on BPM skills analysis and competence modeling.**

Este repositório contém os artefatos de pesquisa desenvolvidos no âmbito do **BPM Research Lab – UFRGS**.

---

## 🇧🇷 Português

### 📌 Contexto de Pesquisa
Este repositório contém um projeto de **pesquisa acadêmica em andamento**, desenvolvido no **BPM Research Lab** da **Universidade Federal do Rio Grande do Sul (UFRGS)**.

* **Pesquisador:** Guilherme Rego Rockembach
* **Orientadora:** Profa. Dra. Lucineia Heloisa Thom
* **Laboratório:** [BPM Research Lab – UFRGS](https://www.instagram.com/bpm_research_lab_ufrgs/)

A pesquisa investiga a **construção sistemática de competências e objetivos de aprendizagem em BPM**, integrando:
* Literatura de referência em BPM;
* Similaridade semântica baseada em *embeddings*;
* Taxonomias educacionais (Bloom e Dimensões do Conhecimento);
* Modelos de linguagem de grande escala (LLMs).

### 📋 Visão Geral
Este projeto implementa um *pipeline* que transforma índices de múltiplos livros de BPM (Excel) em um conjunto estruturado de competências e objetivos de aprendizagem. O processo utiliza *sentence-embeddings* e LLMs para mapeamento semântico, classificação, geração e desduplicação.

### 📂 Estrutura de Diretórios

```text
BPM_Skills/
│
├── data/
│   ├── bpm_skills_pipeline/            # BPM pipeline execution data (input → output)
│   └── Baselines_Cross-Domain-Gen/     # Baseline experiments and generalization results
│
├── src/
│   ├── bpm_books_merger.py
│   ├── sections_to_competence_mapper.py
│   ├── content_knowledge_dimension_classifier.py
│   ├── merge_contents_and_competences.py
│   ├── competence_bloom_classifier.py
│   ├── skills_generator.py
│   └── skills_deduplicator.py
│
├── config/
│   └── config.json         # Centralized configuration (models, thresholds)
│
├── requirements.txt
├── README.md
└── LICENSE
```
### ⚙️ Ordem de Execução (Obrigatória)
A ordem de execução é crítica, pois os passos seguintes consomem os resultados dos anteriores. Execute os scripts (localizados em `src/`) nesta sequência:

1.  **Mesclar livros (`bpm_books_merger.py`):** Unifica as planilhas dos livros e remove duplicatas de seções.
2.  **Mapear seções para competências (`sections_to_competence_mapper.py`):** Atribui cada seção mesclada a rótulos de competência.
3.  **Classificar dimensão do conhecimento (`content_knowledge_dimension_classifier.py`):** Infere a dimensão (Factual, Conceitual, Procedimental, Metacognitivo).
4.  **Mesclar conteúdos e classificações (`merge_contents_and_competences.py`):** Prepara o dataset consolidado.
5.  **Classificar nível Bloom (`competence_bloom_classifier.py`):** Infere o nível cognitivo (Lembrar, Compreender, Aplicar, etc.).
6.  **Gerar habilidades (`skills_generator.py`):** Usa LLM + embeddings para gerar objetivos de aprendizagem.
7.  **Desduplicar habilidades (`skills_deduplicator.py`):** Agrupa e remove habilidades duplicadas geradas por diferentes modelos.

### 🚀 Instalação e Execução (Colab ou Local)

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    python -m spacy download pt_core_news_sm
    python -m spacy download en_core_web_sm
    ```
2.  **Configuração de LLM:**
    O projeto utiliza modelos como `Meta-Llama-3.1-8B-Instruct`. É necessário um token do Hugging Face.
3.  **Execução:**
    Siga a ordem numérica listada acima, executando os scripts dentro da pasta `src/`. Exemplo:
    ```bash
    python src/bpm_books_merger.py
    ```

### ⚖️ Dados e Ética
Este projeto segue as diretrizes do laboratório:
* Scripts e datasets destinados exclusivamente para **uso educacional e de pesquisa**.
* Redistribuição ou uso comercial não permitidos sem autorização prévia.
* Ao utilizar este código, cite o **BPM Research Lab – UFRGS**.

---

## 🇺🇸 English

### 📌 Research Context
This repository contains an **ongoing academic research project** developed at the **BPM Research Lab** of the **Federal University of Rio Grande do Sul (UFRGS)**.

* **Researcher:** Guilherme Rego Rockembach
* **Supervisor:** Prof. Dr. Lucineia Heloisa Thom
* **Lab:** [BPM Research Lab – UFRGS](https://www.instagram.com/bpm_research_lab_ufrgs/)

The research investigates the **systematic construction of BPM competencies and learning objectives**, integrating:
* BPM reference literature;
* Embedding-based semantic similarity;
* Educational taxonomies (Bloom);
* Knowledge dimensions;
* Large Language Models (LLMs).

### 📋 Overview
This repository contains a sequence of scripts that transform multiple BPM book table-of-contents (Excel) files into a structured set of competencies and learning objectives, using sentence-embeddings and LLMs for semantic mapping, classification, generation, and deduplication. Designed for execution in Google Colab (GPU recommended) or local Python environments.

### 📂 Directory Structure

```text
BPM_Skills/
│
├── data/
│   ├── bpm_skills_pipeline/            # BPM pipeline execution data (input → output)
│   └── Baselines_Cross-Domain-Gen/     # Baseline experiments and generalization results
│
├── src/
│   ├── bpm_books_merger.py
│   ├── sections_to_competence_mapper.py
│   ├── content_knowledge_dimension_classifier.py
│   ├── merge_contents_and_competences.py
│   ├── competence_bloom_classifier.py
│   ├── skills_generator.py
│   └── skills_deduplicator.py
│
├── config/
│   └── config.json         # Centralized configuration (models, thresholds)
│
├── requirements.txt
├── README.md
└── LICENSE
```
### ⚙️ Execution Order (Required)
**Run the scripts in this exact order** (order matters because later steps consume outputs of previous ones):

1.  **`bpm_books_merger.py`**: Merge all input book spreadsheets and deduplicate sections.
2.  **`sections_to_competence_mapper.py`**: Assign each merged section (`group_name`) to competency labels.
3.  **`content_knowledge_dimension_classifier.py`**: Infer knowledge dimension (Factual / Conceptual / Procedural / Metacognitive).
4.  **`merge_contents_and_competences.py`**: Join contents with the competence assignment.
5.  **`competence_bloom_classifier.py`**: Infer Bloom taxonomy level for each competence.
6.  **`skills_generator.py`**: Use LLM + embeddings to generate learning objectives per competence.
7.  **`skills_deduplicator.py`**: Cluster & deduplicate skills ensuring minimum counts per model.

### 🚀 Quick Start (Colab/Local)

1.  **Install requirements:**
    ```bash
    pip install -r requirements.txt
    python -m spacy download pt_core_news_sm
    python -m spacy download en_core_web_sm
    ```
2.  **Hugging Face & LLM Notes:**
    * Scripts use models such as `meta-llama/Meta-Llama-3.1-8B-Instruct`.
    * Requires a Hugging Face token (`notebook_login()` in Colab).
    * Use quantization (`bitsandbytes`) if needed for GPU memory constraints.
3.  **Execution:**
    Run scripts from the root directory referencing the `src` folder:
    ```bash
    python src/bpm_books_merger.py
    ```

### 📄 Inputs & Outputs
* **Key Inputs (in `data/`):** `Final_BPM_Books_Definitivo.xlsx`, Book Excel files (`Livro_*.xlsx`).
* **Key Outputs (in `results/`):** `objetivos_de_aprendizagem_final.xlsx`, `habilidades_unicas_por_competencia.xlsx`.

### ⚖️ License and Responsibility
All scripts and datasets are intended exclusively for **educational and research use**. Redistribution, commercial use, or derivative works are **not allowed** without prior authorization.

If you use this code or its outputs, please cite or acknowledge the **BPM Research Lab – UFRGS**.

* **Contact:** Guilherme Rego Rockembach
* **Instagram:** [@bpm_research_lab_ufrgs](https://www.instagram.com/bpm_research_lab_ufrgs/)

---
*BPM Research Lab – UFRGS*
