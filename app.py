# ============================================================
# app.py - Servidor Flask do Controle Financeiro (v3 FINAL)
# ============================================================
# Funcionalidades:
#   • Movimentações com descrição, valor, tipo, data, hora e categoria
#   • Campo extra "Especifique" quando categoria = Outros
#   • Renda mensal + dia de recebimento + benefícios
#   • Cálculo de dias até o próximo recebimento
#   • Gráfico comparativo renda prevista × despesas reais
#   • Alerta de saldo negativo
#   • Filtros, pesquisa e exportação CSV
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, send_file
import json
import os
import csv
import io
import calendar
from datetime import datetime, date

app = Flask(__name__)

ARQUIVO_DADOS = "dados.json"
ARQUIVO_PERFIL = "perfil.json"

CATEGORIAS = ["Alimentação", "Transporte", "Lazer", "Educação", "Saúde", "Outros"]


# ============================================================
# FUNÇÕES AUXILIARES — dados.json
# ============================================================
def carregar_dados():
    """Lê as movimentações do arquivo JSON."""
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def salvar_dados(movimentacoes):
    """Grava a lista de movimentações no JSON."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(movimentacoes, f, ensure_ascii=False, indent=4)


# ============================================================
# FUNÇÕES AUXILIARES — perfil.json
# ============================================================
def carregar_perfil():
    """Lê o perfil (renda + benefícios). Cria padrão se não existir."""
    padrao = {
        "renda_mensal": 0.0,
        "dia_recebimento": 1,
        "beneficios": []
    }
    if not os.path.exists(ARQUIVO_PERFIL):
        return padrao
    try:
        with open(ARQUIVO_PERFIL, "r", encoding="utf-8") as f:
            perfil = json.load(f)
            for chave, valor in padrao.items():
                perfil.setdefault(chave, valor)
            return perfil
    except (json.JSONDecodeError, FileNotFoundError):
        return padrao


def salvar_perfil(perfil):
    """Grava o perfil no arquivo JSON."""
    with open(ARQUIVO_PERFIL, "w", encoding="utf-8") as f:
        json.dump(perfil, f, ensure_ascii=False, indent=4)


# ============================================================
# FUNÇÃO AUXILIAR — próximo recebimento
# ============================================================
def calcular_proximo_recebimento(hoje, dia):
    """
    Retorna a próxima data em que o usuário vai receber.
    Trata meses curtos (ex: dia 31 em fevereiro → 28 ou 29).
    """
    ano, mes = hoje.year, hoje.month

    ultimo_dia_mes = calendar.monthrange(ano, mes)[1]
    dia_ajustado = min(dia, ultimo_dia_mes)

    if dia_ajustado >= hoje.day:
        return date(ano, mes, dia_ajustado)

    mes += 1
    if mes > 12:
        mes = 1
        ano += 1

    ultimo_dia_mes = calendar.monthrange(ano, mes)[1]
    return date(ano, mes, min(dia, ultimo_dia_mes))


# ============================================================
# ROTA PRINCIPAL
# ============================================================
@app.route("/")
def index():
    movimentacoes = carregar_dados()
    perfil = carregar_perfil()

    # ----- Filtros -----
    busca = request.args.get("busca", "").strip().lower()
    data_inicio = request.args.get("data_inicio", "")
    data_fim = request.args.get("data_fim", "")

    filtradas = []
    for m in movimentacoes:
        if busca and busca not in m["descricao"].lower():
            continue
        if data_inicio and m["data"] < data_inicio:
            continue
        if data_fim and m["data"] > data_fim:
            continue
        filtradas.append(m)

    # ----- Totais -----
    total_receitas = sum(m["valor"] for m in filtradas if m["tipo"] == "Receita")
    total_despesas = sum(m["valor"] for m in filtradas if m["tipo"] == "Despesa")
    saldo = total_receitas - total_despesas

    # ----- Totais por categoria -----
    categorias_totais = {cat: 0 for cat in CATEGORIAS}
    for m in filtradas:
        if m["tipo"] == "Despesa":
            categorias_totais[m.get("categoria", "Outros")] += m["valor"]

    # ----- Renda prevista -----
    total_beneficios = sum(b["valor"] for b in perfil["beneficios"])
    renda_total_prevista = perfil["renda_mensal"] + total_beneficios

    # ----- Dias até o próximo recebimento -----
    hoje = date.today()
    dia_rec = perfil.get("dia_recebimento", 1)
    proximo_recebimento = calcular_proximo_recebimento(hoje, dia_rec)
    dias_ate_receber = (proximo_recebimento - hoje).days

    # ----- Comparativo renda × despesas -----
    if renda_total_prevista > 0:
        percentual_despesas = round((total_despesas / renda_total_prevista) * 100, 1)
    else:
        percentual_despesas = 0.0

    sobra_prevista = renda_total_prevista - total_despesas

    return render_template(
        "index.html",
        movimentacoes=sorted(filtradas,
                             key=lambda x: (x["data"], x.get("hora", "")),
                             reverse=True),
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo,
        categorias=CATEGORIAS,
        categorias_totais=categorias_totais,
        busca=busca,
        data_inicio=data_inicio,
        data_fim=data_fim,
        perfil=perfil,
        total_beneficios=total_beneficios,
        renda_total_prevista=renda_total_prevista,
        proximo_recebimento=proximo_recebimento,
        dias_ate_receber=dias_ate_receber,
        percentual_despesas=percentual_despesas,
        sobra_prevista=sobra_prevista,
    )


# ============================================================
# ROTA — adicionar movimentação
# ============================================================
@app.route("/adicionar", methods=["POST"])
def adicionar():
    descricao = request.form.get("descricao", "").strip()
    valor_str = request.form.get("valor", "").strip()
    tipo = request.form.get("tipo", "").strip()
    data = request.form.get("data", "").strip()
    hora = request.form.get("hora", "").strip() or datetime.now().strftime("%H:%M")
    categoria = request.form.get("categoria", "Outros").strip()
    outros_desc = request.form.get("outros_desc", "").strip()

    if not descricao or not valor_str or not tipo or not data:
        return redirect(url_for("index", erro="Preencha todos os campos obrigatórios!"))

    try:
        valor = float(valor_str.replace(",", "."))
    except ValueError:
        return redirect(url_for("index", erro="Valor inválido!"))

    if valor <= 0:
        return redirect(url_for("index", erro="O valor deve ser maior que zero!"))

    if tipo not in ["Receita", "Despesa"]:
        return redirect(url_for("index", erro="Tipo inválido!"))

    if categoria == "Outros" and not outros_desc:
        return redirect(url_for("index",
                                erro="Especifique o que foi a movimentação 'Outros'!"))

    if categoria != "Outros":
        outros_desc = ""

    nova = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "descricao": descricao,
        "valor": round(valor, 2),
        "tipo": tipo,
        "data": data,
        "hora": hora,
        "categoria": categoria if categoria in CATEGORIAS else "Outros",
        "outros_desc": outros_desc,
    }

    movimentacoes = carregar_dados()
    movimentacoes.append(nova)
    salvar_dados(movimentacoes)
    return redirect(url_for("index"))


# ============================================================
# ROTA — salvar perfil (renda + benefícios)
# ============================================================
@app.route("/perfil", methods=["POST"])
def atualizar_perfil():
    renda_str = request.form.get("renda_mensal", "0").strip() or "0"
    dia_str = request.form.get("dia_recebimento", "1").strip() or "1"

    try:
        renda = float(renda_str.replace(",", "."))
        if renda < 0:
            renda = 0
    except ValueError:
        renda = 0.0

    try:
        dia = int(dia_str)
        if dia < 1 or dia > 31:
            dia = 1
    except ValueError:
        dia = 1

    nomes = request.form.getlist("beneficio_nome[]")
    valores = request.form.getlist("beneficio_valor[]")
    dias = request.form.getlist("beneficio_dia[]")

    beneficios = []
    for n, v, d in zip(nomes, valores, dias):
        n = n.strip()
        v = v.strip()
        d = d.strip()
        if not n or not v:
            continue
        try:
            valor_b = float(v.replace(",", "."))
            if valor_b < 0:
                continue
            dia_b = int(d) if d else 1
            if dia_b < 1 or dia_b > 31:
                dia_b = 1
            beneficios.append({"nome": n, "valor": round(valor_b, 2), "dia": dia_b})
        except ValueError:
            continue

    perfil = {
        "renda_mensal": round(renda, 2),
        "dia_recebimento": dia,
        "beneficios": beneficios,
    }
    salvar_perfil(perfil)
    return redirect(url_for("index"))


# ============================================================
# ROTA — excluir movimentação
# ============================================================
@app.route("/excluir/<id_mov>")
def excluir(id_mov):
    movimentacoes = carregar_dados()
    movimentacoes = [m for m in movimentacoes if m["id"] != id_mov]
    salvar_dados(movimentacoes)
    return redirect(url_for("index"))


# ============================================================
# ROTA — exportar CSV
# ============================================================
@app.route("/exportar")
def exportar():
    movimentacoes = carregar_dados()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")
    writer.writerow(["Data", "Hora", "Descrição", "Categoria",
                     "Detalhe (Outros)", "Tipo", "Valor"])
    for m in movimentacoes:
        writer.writerow([
            m["data"],
            m.get("hora", ""),
            m["descricao"],
            m.get("categoria", "Outros"),
            m.get("outros_desc", ""),
            m["tipo"],
            f'{m["valor"]:.2f}'
        ])

    output.seek(0)
    bytes_io = io.BytesIO(output.getvalue().encode("utf-8-sig"))
    return send_file(
        bytes_io,
        mimetype="text/csv",
        as_attachment=True,
        download_name="movimentacoes.csv",
    )


if __name__ == "__main__":
    app.run(debug=True) 