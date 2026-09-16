# 💰 Controle Financeiro Pessoal

Sistema web completo para gerenciar suas finanças pessoais, desenvolvido com **Python + Flask** no backend e **HTML + CSS + JavaScript** no frontend. Os dados são armazenados localmente em arquivos **JSON**, sem necessidade de banco de dados.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Executar](#-como-executar)
- [Como Usar](#-como-usar)
- [Explicação dos Arquivos](#-explicação-dos-arquivos)
- [API de Rotas](#-api-de-rotas)
- [Personalização](#-personalização)
- [Melhorias Futuras](#-melhorias-futuras)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Autor](#-autor)

---

## 🎯 Sobre o Projeto

O **Controle Financeiro Pessoal** é uma aplicação web simples e completa que permite:

- 📝 Registrar **receitas** e **despesas** do dia a dia
- 📊 Visualizar um **dashboard** com totais atualizados automaticamente
- 🏷️ Classificar movimentações por **categorias**
- 💼 Cadastrar **renda mensal** e **benefícios** (VR, VT, VA, etc.)
- 📅 Saber **quantos dias faltam** para o próximo recebimento
- 📈 Comparar **renda prevista** com **despesas reais**
- 🔔 Receber **alerta visual** quando o saldo ficar negativo
- 🔎 **Pesquisar** e **filtrar** por descrição e intervalo de datas
- 📥 **Exportar** todas as movimentações para **CSV**

Ideal para quem está aprendendo Flask e quer um projeto **prático, comentado e didático**.

---

## ✨ Funcionalidades

### 💸 Movimentações Financeiras
- [x] Adicionar **receitas** e **despesas**
- [x] Campos: **descrição**, **valor**, **tipo**, **data**, **hora** e **categoria**
- [x] Campo extra para especificar quando a categoria for **"Outros"**
- [x] Excluir movimentações com confirmação
- [x] Validação: sem campos vazios nem valores negativos/zero

### 📊 Dashboard
- [x] Card com **total de receitas**
- [x] Card com **total de despesas**
- [x] Card com **saldo atual** (verde se positivo, laranja se negativo)

### 💼 Renda & Benefícios
- [x] Cadastro de **renda mensal** e **dia do recebimento**
- [x] Cadastro de múltiplos **benefícios** (nome + valor + dia)
- [x] Cálculo automático do **total mensal previsto**
- [x] **Contador regressivo** de dias até o próximo recebimento
- [x] **Gráfico comparativo** renda prevista × despesas reais

### 🔔 Alerta de Saldo Negativo
- [x] Banner animado no topo quando o saldo fica negativo
- [x] Alerta visual reforçado com ícone pulsante

### 🔍 Filtros e Pesquisa
- [x] Pesquisa por **descrição**
- [x] Filtro por **intervalo de datas**
- [x] Exportação para **CSV** (compatível com Excel)

### 🎨 Interface
- [x] Tema **escuro** moderno
- [x] Totalmente **responsivo** (desktop, tablet e celular)
- [x] Gráfico de barras **Despesas por Categoria**

---

## 🛠 Tecnologias Utilizadas

| Camada       | Tecnologia                             |
|--------------|----------------------------------------|
| **Backend**  | Python 3.8+ / Flask                    |
| **Frontend** | HTML5, CSS3, JavaScript (puro)         |
| **Template** | Jinja2 (motor de templates do Flask)   |
| **Dados**    | JSON (arquivos locais)                 |
| **Estilo**   | CSS Grid, Flexbox, tema escuro         |

---

## 📂 Estrutura do Projeto
