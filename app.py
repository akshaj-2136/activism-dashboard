import streamlit as st
import pandas as pd
import joblib
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ACTIVISM // TERMINAL",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 🎨 BLOOMBERG TERMINAL AESTHETIC CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600&display=swap');
    .stApp { background-color: #0E1117; color: #E0E0E0; font-family: 'Inter', sans-serif; }
    .stMetricValue, .stNumberInput input { font-family: 'JetBrains Mono', monospace !important; }
    h1, h2, h3, h4 { color: #FFFFFF !important; text-transform: uppercase; letter-spacing: 1px; }
    .risk-terminal-card {
        background-color: #1a1a1a; border: 1px solid #FF3B30; border-left: 5px solid #FF3B30;
        padding: 15px; margin-bottom: 10px;
    }
    .risk-terminal-card h2 { color: #FF3B30 !important; font-size: 1.1rem; }
    .risk-terminal-card h1 { color: #FFFFFF !important; font-family: 'JetBrains Mono'; font-size: 2.5rem; margin: 0; }
    .safe-terminal-card {
        background-color: #1a1a1a; border: 1px solid #30D158; border-left: 5px solid #30D158;
        padding: 15px; margin-bottom: 10px;
    }
    .safe-terminal-card h2 { color: #30D158 !important; font-size: 1.1rem; }
    .safe-terminal-card h1 { color: #FFFFFF !important; font-family: 'JetBrains Mono'; font-size: 2.5rem; margin: 0; }
    .factor-bad { color: #FF453A; font-family: 'JetBrains Mono'; font-weight: bold; font-size: 0.85rem; margin-bottom: 5px; }
    .factor-good { color: #32D74B; font-family: 'JetBrains Mono'; font-weight: bold; font-size: 0.85rem; margin-bottom: 5px; }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #2C2C2E !important; color: #F2F2F7 !important; border: 1px solid #48484A !important; border-radius: 0px !important;
    }
    button[kind="primary"] {
        background-color: #0A84FF; border-radius: 0px; color: white; text-transform: uppercase; font-weight: 700; border: 1px solid #0058D0;
    }
    button[data-baseweb="tab"] { background: transparent; border: none; color: #636366; font-weight: 600; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #0A84FF; border-bottom: 2px solid #0A84FF; }
    .block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# --- 1. DATA LOADING ---
@st.cache_resource
def load_resources():
    if not os.path.exists('activism_model.pkl'): return None, None
    model = joblib.load('activism_model.pkl')
    if os.path.exists('Final_Dataset_Cleaned.csv'):
        df = pd.read_csv('Final_Dataset_Cleaned.csv')
        # Generate the Sector label so filtering works
        df['Sector'] = df.apply(lambda r: 'Banking & Finance' if 'Bank' in str(r['Ticker']) or r['Asset_Quality'] > 0 else 'Mining & Heavy Industry', axis=1)
    else: df = None
    return model, df

model, df_database = load_resources()
def to_dec(x): return x / 100.0

# --- 2. HEADER ---
st.markdown("## 📈 ACTIVISM // TERMINAL")
st.caption("v4.0 | FULLY DYNAMIC FILTERING & EXHAUSTIVE REASONING")
st.markdown("---")

tab1, tab2 = st.tabs(["🏢 CORPORATE INTELLIGENCE", "⚡ STRATEGY SIMULATOR"])

# ==============================================================================
# TAB 1: CORPORATE INTELLIGENCE
# ==============================================================================
with tab1:
    if df_database is None: st.error(">> DATABASE_OFFLINE")
    else:
        c1, c2, c3 = st.columns(3)
        with c1: 
            # DYNAMIC FILTER 1: Sector
            sectors = sorted(df_database['Sector'].unique())
            selected_sector = st.selectbox("1. SECTOR", sectors)
        with c2: 
            # DYNAMIC FILTER 2: Ticker (Depends on Sector)
            filtered_tickers = sorted(df_database[df_database['Sector'] == selected_sector]['Ticker'].unique())
            ticker = st.selectbox("2. TICKER", filtered_tickers)
        with c3: 
            # DYNAMIC FILTER 3: Year (Depends on Ticker)
            filtered_years = sorted(df_database[df_database['Ticker'] == ticker]['Year'].unique(), reverse=True)
            year = st.selectbox("3. YEAR", filtered_years)

        try:
            row = df_database[(df_database['Ticker'] == ticker) & (df_database['Year'] == year)].iloc[0]
            st.markdown("### FINANCIAL SNAPSHOT")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("PROMOTER HOLD", f"{row['Promoter_Hold']:.1%}")
            k2.metric("PROMOTER PLEDGE", f"{row['Promoter_Pledge']:.1%}")
            k3.metric("VOLATILITY", f"{row['Ann_Volatility']:.1%}")
            k4.metric("DISSENT", f"{row['Voting_Dissent']:.1%}")

            if st.button("RUN DIAGNOSTIC", type="primary"):
                feature_cols = ['3Y_Stock_CAGR', 'Ann_Volatility', 'Promoter_Hold', 'Promoter_Pledge', 'Inst_Hold_Change', 'Board_Indep_Pct', 'Director_Tenure', 'CEO_Duality', 'Auditor_Quality', 'Auditor_Quit', 'Voting_Dissent', 'Whistleblower_Cnt', 'Profit_Growth', 'Governance_Ratio', 'Leverage_Risk', 'Liquidity', 'CEO_Pay_Gap', 'Div_Yield', 'Asset_Quality', 'Loan_Risk', 'Environ_Risk', 'Capex_Trap']
                input_vec = pd.DataFrame([row[feature_cols]])
                prob = model.predict_proba(input_vec)[0][1]

                rc1, rc2 = st.columns([1, 1.5])
                with rc1:
                    if prob >= 0.50: st.markdown(f'<div class="risk-terminal-card"><h2>RISK: CRITICAL</h2><h1>{prob:.1%}</h1><p>REVOLT PROBABILITY</p></div>', unsafe_allow_html=True)
                    else: st.markdown(f'<div class="safe-terminal-card"><h2>RISK: STABLE</h2><h1>{prob:.1%}</h1><p>REVOLT PROBABILITY</p></div>', unsafe_allow_html=True)
                with rc2:
                    st.markdown("#### 🔍 GOVERNANCE AUDIT LOG")
                    if row['Promoter_Pledge'] > 0.4: st.markdown(f"<div class='factor-bad'>[!] HIGH PLEDGE: {row['Promoter_Pledge']:.1%} encumbered.</div>", unsafe_allow_html=True)
                    if row['Auditor_Quit'] == 1: st.markdown("<div class='factor-bad'>[!] AUDITOR RESIGNATION: Major governance red flag.</div>", unsafe_allow_html=True)
                    if row['Voting_Dissent'] > 0.05: st.markdown(f"<div class='factor-bad'>[!] DISSENT: Voting opposition is high ({row['Voting_Dissent']:.1%}).</div>", unsafe_allow_html=True)
                    if row['Profit_Growth'] > 0.05: st.markdown(f"<div class='factor-good'>[OK] EARNINGS BUFFER: Profit growth ({row['Profit_Growth']:.1%}) offsets risk factors.</div>", unsafe_allow_html=True)
                    if row['Auditor_Quality'] == 1: st.markdown("<div class='factor-good'>[OK] AUDIT: Verified by Big 4 Firm.</div>", unsafe_allow_html=True)
        except:
            st.error(">> DATA UNAVAILABLE")

# ==============================================================================
# TAB 2: STRATEGY SIMULATOR (ALL 22 EXPOSED & CLEANLY SEPARATED)
# ==============================================================================
with tab2:
    st.markdown("### ⚡ FULL-FEATURE STRESS TEST")
    with st.form("sim_form"):
        c1, c2 = st.columns(2)
        sim_name = c1.text_input("SCENARIO LABEL", "Simulation Case A")
        sim_sector = c2.selectbox("INDUSTRY", ("Banking & Finance", "Mining & Heavy Industry"))

        st.markdown("#### 1. OWNERSHIP & SHAREHOLDER VOICE")
        o1, o2, o3, o4 = st.columns(4)
        v_hold = o1.number_input("Promoter Hold (%)", 0.0, 100.0, 50.0)
        v_pledge = o2.number_input("Promoter Pledge (%)", 0.0, 100.0, 0.0)
        v_inst = o3.number_input("Inst. Hold Change (%)", -50.0, 50.0, 0.0)
        v_dissent = o4.number_input("Voting Dissent (%)", 0.0, 100.0, 1.0)

        st.markdown("#### 2. BOARD & AUDIT GOVERNANCE")
        b1, b2, b3, b4, b5, b6 = st.columns(6)
        v_indep = b1.number_input("Board Indep (%)", 0.0, 100.0, 50.0)
        v_tenure = b2.number_input("Director Tenure", 0.0, 20.0, 4.0)
        v_dual = b3.selectbox("CEO Duality", (0, 1))
        v_audit_q = b4.selectbox("Big 4 Auditor", (1, 0))
        v_audit_quit = b5.selectbox("Auditor Quit", (0, 1))
        v_whistle = b6.number_input("Whistleblower Cnt", 0, 50, 0)

        st.markdown("#### 3. PERFORMANCE & VALUATION")
        p1, p2, p3, p4 = st.columns(4)
        v_cagr = p1.number_input("3Y Stock CAGR (%)", -100.0, 200.0, 10.0)
        v_profit = p2.number_input("Profit Growth (%)", -100.0, 500.0, 5.0)
        v_vol = p3.number_input("Ann. Volatility (%)", 0.0, 200.0, 30.0)
        v_div = p4.number_input("Div. Yield (%)", 0.0, 20.0, 2.0)

        st.markdown("#### 4. CAPITAL & RISK STRUCTURE")
        r1, r2, r3, r4 = st.columns(4)
        v_roa = r1.number_input("ROA/ROCE (decimal)", value=0.02, format="%.3f")
        v_lev = r2.number_input("Leverage Ratio", value=1.5, format="%.2f")
        v_liq = r3.number_input("Liquidity Ratio", value=1.2, format="%.2f")
        v_pay = r4.number_input("CEO Pay Gap (x)", value=50.0)

        st.markdown(f"#### 5. {sim_sector.upper()} SPECIFICS")
        s1, s2 = st.columns(2)
        v_gnpa, v_pcr, v_env, v_capex = 0.0, 0.70, 0, 0.0

        # STRICT SECTOR LOGIC
        if sim_sector == "Banking & Finance":
            v_gnpa = s1.number_input("GNPA % (Asset Quality)", 0.0, 100.0, 2.0)
            v_pcr = s2.number_input("PCR Ratio (decimal)", 0.0, 1.0, 0.70, format="%.2f")
        else:
            v_env = s1.selectbox("Environmental Risk Flag", (0, 1))
            v_capex = s2.number_input("Capex Trap Ratio", 0.0, 1.0, 0.0, format="%.2f")

        submit = st.form_submit_button("RUN FULL SIMULATION", type="primary", use_container_width=True)
        if submit:
            input_dict = {
                '3Y_Stock_CAGR': to_dec(v_cagr), 'Ann_Volatility': to_dec(v_vol), 'Promoter_Hold': to_dec(v_hold),
                'Promoter_Pledge': to_dec(v_pledge), 'Inst_Hold_Change': to_dec(v_inst), 'Board_Indep_Pct': to_dec(v_indep),
                'Director_Tenure': v_tenure, 'CEO_Duality': v_dual, 'Auditor_Quality': v_audit_q,
                'Auditor_Quit': v_audit_quit, 'Voting_Dissent': to_dec(v_dissent), 'Whistleblower_Cnt': v_whistle,
                'Profit_Growth': to_dec(v_profit), 'Governance_Ratio': v_roa, 'Leverage_Risk': v_lev,
                'Liquidity': v_liq, 'CEO_Pay_Gap': v_pay, 'Div_Yield': to_dec(v_div),
                'Asset_Quality': to_dec(v_gnpa), 'Loan_Risk': v_pcr, 'Environ_Risk': v_env, 'Capex_Trap': v_capex
            }
            sim_df = pd.DataFrame([input_dict])
            prob = model.predict_proba(sim_df)[0][1]

            sc1, sc2 = st.columns([1, 1.5])
            with sc1:
                if prob >= 0.50: st.markdown(f'<div class="risk-terminal-card"><h2>PROGNOSIS: CRITICAL</h2><h1>{prob:.1%}</h1><p>REVOLT PROBABILITY</p></div>', unsafe_allow_html=True)
                else: st.markdown(f'<div class="safe-terminal-card"><h2>PROGNOSIS: STABLE</h2><h1>{prob:.1%}</h1><p>REVOLT PROBABILITY</p></div>', unsafe_allow_html=True)
            with sc2:
                st.markdown("#### 🛰️ MULTI-FACTOR REASONING")
                # Exhausive Reasoning Engine
                if v_pledge > 40: st.markdown(f"<div class='factor-bad'>[!] OWNERSHIP: High Promoter Pledging ({v_pledge}%).</div>", unsafe_allow_html=True)
                if sim_sector == "Banking & Finance" and v_gnpa > 10: st.markdown(f"<div class='factor-bad'>[!] CREDIT: GNPA exceeds safety threshold ({v_gnpa}%).</div>", unsafe_allow_html=True)
                if sim_sector == "Mining & Heavy Industry" and v_env == 1: st.markdown(f"<div class='factor-bad'>[!] ESG: Major Environmental Risk detected.</div>", unsafe_allow_html=True)
                if v_audit_quit == 1: st.markdown("<div class='factor-bad'>[!] AUDIT: Auditor resignation is a critical red flag.</div>", unsafe_allow_html=True)
                if v_dissent > 5: st.markdown(f"<div class='factor-bad'>[!] DISSENT: Voting opposition is high ({v_dissent}%).</div>", unsafe_allow_html=True)

                # Mitigating Factors
                if v_profit > 0: st.markdown(f"<div class='factor-good'>[OK] PROFIT: Positive growth ({v_profit}%) mitigates extreme risk.</div>", unsafe_allow_html=True)
                if v_cagr > 0: st.markdown(f"<div class='factor-good'>[OK] MARKET: Positive 3Y CAGR suggests surviving stock value.</div>", unsafe_allow_html=True)

                if 0.45 < prob < 0.65:
                    st.info("💡 **Model Note:** The score is near 50-60% because severe structural risks are being partially offset by surviving business performance.")
