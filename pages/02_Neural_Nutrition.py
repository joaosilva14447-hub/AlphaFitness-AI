import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. Configuração Master Alpha
st.set_page_config(page_title="Neural Nutrition | Alpha Fitness", layout="wide")

AQUA, BLUE = "#00FBFF", "#3D5AFE"

st.markdown(f"""
<style>
    .main {{ background-color: #0F0F0F; }}
    div[data-testid='stMetric'] {{ background-color: #161616; padding: 20px; border-radius: 5px; border: 1px solid #333; }}
    h1 {{ font-family: serif; color: {BLUE}; text-align: center; }}
</style>
""", unsafe_allow_html=True)

# 2. Sincronização de Dados
weight = st.session_state.get('user_weight', 80.0)
goal = st.session_state.get('user_goal', 'Maintenance')

st.markdown(f"<h1>✦ 𝓝𝓮𝓾𝓻𝓪𝓵 𝓝𝓾𝓽𝓻𝓲𝓽𝓲𝓸𝓷 𝓐𝓻𝓬𝓱𝓲𝓽𝓮𝓬𝓽 ✦</h1>", unsafe_allow_html=True)
st.write("---")

# 3. Hidratação Estratégica
water_target = (weight * 35 / 1000) + (0.5 if goal == "Bulking" else 0.7 if goal == "Cutting" else 0.0)

c1, c2, c3 = st.columns(3)
c1.metric("ESTRATÉGIA", goal.upper())
c2.metric("ALVO DE HIDRATAÇÃO", f"{water_target:.1f} L/Dia")
c3.info(f"💡 Dica: Dividir o consumo de água em 500ml a cada 2-3 horas.")

# 4. Engenharia de Macros
if goal == "Bulking": base_cals = 2900
elif goal == "Cutting": base_cals = 2000
else: base_cals = 2500

p_total = weight * 2.2
f_total = weight * 0.8
c_total = (base_cals - (p_total * 4) - (f_total * 9)) / 4

with st.sidebar:
    st.header("✦ Protocolo")
    num_meals = st.slider("Refeições Diárias", 3, 6, 4)

p_meal, c_meal, f_meal = p_total/num_meals, c_total/num_meals, f_total/num_meals

# 5. Database de Densidade Alpha (Ajustada para Volume Realista)
db = {
    "P": {"Frango": 31, "Vaca": 28, "Peixe": 24, "Whey": 80, "Ovos (un)": 6, "Claras (ml)": 11, "Iogurte": 10},
    "C": {"Arroz": 28, "Batata Doce": 20, "Aveia": 60, "Massa": 25, "Fruta Mix": 15, "Pão": 45, "Creme Arroz": 80},
    "F": {"Azeite (ml)": 90, "Abacate": 15, "Manteiga Amendoim": 50, "Frutos Secos": 50}
}

# 6. Matriz de Refeições Únicas (3 opções por cada uma das 6 janelas)
master_menu = {
    1: [ # Pequeno Almoço
        {"name": "Opção A: Alpha Pancakes", "p": "Claras (ml)", "c": "Aveia", "f": "Manteiga Amendoim"},
        {"name": "Opção B: Omelete de Elite", "p": "Ovos (un)", "c": "Pão", "f": "Abacate"},
        {"name": "Opção C: Yogurt Power", "p": "Iogurte", "c": "Fruta Mix", "f": "Frutos Secos"}
    ],
    2: [ # Lanche Manhã
        {"name": "Opção A: Protein Shake", "p": "Whey", "c": "Fruta Mix", "f": "Frutos Secos"},
        {"name": "Opção B: Yogurt & Nuts", "p": "Iogurte", "c": "Aveia", "f": "Frutos Secos"},
        {"name": "Opção C: Alpha Bar (Caseira)", "p": "Whey", "c": "Aveia", "f": "Manteiga Amendoim"}
    ],
    3: [ # Almoço
        {"name": "Opção A: Classic Gains", "p": "Frango", "c": "Arroz", "f": "Azeite (ml)"},
        {"name": "Opção B: Beef Performance", "p": "Vaca", "c": "Batata Doce", "f": "Azeite (ml)"},
        {"name": "Opção C: Marine Recovery", "p": "Peixe", "c": "Massa", "f": "Azeite (ml)"}
    ],
    4: [ # Lanche Tarde
        {"name": "Opção A: Toast Proteico", "p": "Frango", "c": "Pão", "f": "Abacate"},
        {"name": "Opção B: Anabolic Smoothie", "p": "Whey", "c": "Fruta Mix", "f": "Manteiga Amendoim"},
        {"name": "Opção C: Rice Cream", "p": "Whey", "c": "Creme Arroz", "f": "Frutos Secos"}
    ],
    5: [ # Jantar
        {"name": "Opção A: Light Chicken", "p": "Frango", "c": "Batata Doce", "f": "Azeite (ml)"},
        {"name": "Opção B: Lean Fish", "p": "Peixe", "c": "Arroz", "f": "Abacate"},
        {"name": "Opção C: Beef & Pasta", "p": "Vaca", "c": "Massa", "f": "Azeite (ml)"}
    ],
    6: [ # Ceia
        {"name": "Opção A: Night Shake", "p": "Whey", "c": "Fruta Mix", "f": "Manteiga Amendoim"},
        {"name": "Opção B: Greek Night", "p": "Iogurte", "c": "Aveia", "f": "Frutos Secos"},
        {"name": "Opção C: Zero-Stress Snack", "p": "Ovos (un)", "c": "Fruta Mix", "f": "Abacate"}
    ]
}

# 7. Renderização com Validação de Volume
st.subheader("✦ Plano de Execução Nutricional")

cols = st.columns(2)
for i in range(1, num_meals + 1):
    with cols[(i-1) % 2]:
        with st.container(border=True):
            st.markdown(f"#### REFEIÇÃO {i}")
            
            # Seleção de Opção Única por Refeição
            options_list = [opt["name"] for opt in master_menu[i]]
            choice = st.selectbox("Selecione o Menu:", options_list, key=f"m4_choice_{i}")
            
            sel = next(opt for opt in master_menu[i] if opt["name"] == choice)
            
            # Cálculos de Quantidade com Proteção de Volume
            # Proteína
            if "un" in sel['p']: p_qty = f"{max(1, p_meal / db['P'][sel['p']]):.0f} unid"
            else: p_qty = f"{(p_meal / db['P'][sel['p']]) * 100:.0f}g/ml"
            
            # Carbo (Se o volume de fruta for > 200g, sugerimos misturar ou trocar por fonte densa)
            raw_c_qty = (c_meal / db['C'][sel['c']]) * 100
            if sel['c'] == "Fruta Mix" and raw_c_qty > 200:
                # Lógica de Volume Inteligente: 150g Fruta + Resto em Aveia/Creme Arroz
                c_display = f"150g de Fruta + {(c_meal - (150 * 0.15)) / 0.60:.0f}g de Aveia"
            else:
                c_display = f"{raw_c_qty:.0f}g"
            
            # Gordura
            if "ml" in sel['f']: f_display = f"{f_meal / (db['F'][sel['f']]/100):.0f}ml"
            else: f_display = f"{(f_meal / db['F'][sel['f']]) * 100:.0f}g"
            
            # UI do Card
            st.markdown(f"""
            <div style="background-color: #161616; padding: 15px; border-radius: 10px; border-left: 5px solid {AQUA};">
                <p style="margin:0;">🟢 <b>{p_display if 'p_display' in locals() else p_qty}</b> de {sel['p']}</p>
                <p style="margin:0;">🔵 <b>{c_display}</b> de {sel['c']}</p>
                <p style="margin:0;">⚪ <b>{f_display}</b> de {sel['f']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Target: {p_meal:.0f}P | {c_meal:.0f}C | {f_meal:.0f}F")

# 8. Gráfico de Distribuição
st.divider()
fig = go.Figure(data=[go.Pie(labels=['Proteína', 'Carbos', 'Gordura'], 
                             values=[p_total*4, c_total*4, f_total*9],
                             hole=.5, marker_colors=[AQUA, BLUE, "#FFFFFF"])])
fig.update_layout(template="plotly_dark", height=400, paper_bgcolor="#0F0F0F")
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.code(f"USER: {weight}KG | GOAL: {goal.upper()} | SYSTEM: OPERATIONAL", language="text")
