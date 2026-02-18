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
    /* 1. GLOBAL TERMINAL THEME */
    .stApp {
        background-color: #0E1117; /* Deep Carbon Black */
        color: #E0E0E0;
    }

    /* 2. FONTS: Monospace for Data (Like a Terminal) */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stMetricValue, .stNumberInput input { font-family: 'JetBrains Mono', monospace !important; }

    /* 3. HEADERS (Bloomberg Orange & White) */
    h1, h2, h3 { color: #FFFFFF !important; text-transform: uppercase; letter-spacing: 1px; }
    .stCaption { color: #FF9F00 !important; font-family: 'JetBrains Mono'; }

    /* 4. CARDS: Sharp Edges, High Contrast */
    .risk-terminal-card {
        background-color: #1a1a1a;
        border: 1px solid #FF3B30; /* Neon Red */
        border-left: 5px solid #FF3B30;
        padding: 15px;
        margin-bottom: 10px;
    }
    .risk-terminal-card h2 { color: #FF3B30 !important; font-size: 1.2rem; margin-bottom: 5px; }
    .risk-terminal-card h1 { color: #FFFFFF !important; font-family: 'JetBrains Mono'; font-size: 2.5rem; margin: 0; }

    .safe-terminal-card {
        background-color: #1a1a1a;
        border: 1px solid #30D158; /* Neon Green */
        border-left: 5px solid #30D158;
        padding: 15px;
        margin-bottom: 10px;
    }
    .safe-terminal-card h2 { color: #30D158 !important; font-size: 1.2rem; margin-bottom: 5px; }
    .safe-terminal-card h1 { color: #FFFFFF !important; font-family: 'JetBrains Mono'; font-size: 2.5rem; margin: 0; }

    /* 5. DATA FACTOR LIST */
    .factor-bad { color: #FF453A; font-family: 'JetBrains Mono'; font-weight: bold; }
    .factor-good { color: #32D74B; font-family: 'JetBrains Mono'; font-weight: bold; }
    .factor-neutral { color: #8E8E93; font-family: 'JetBrains Mono'; }

    /* 6. INPUT FIELDS (Dark & Techy) */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #2C2C2E !important;
        color: #F2F2F7 !important;
        border: 1px solid #48484A !important;
        border-radius: 0px !important; /* Sharp corners like Bloomberg */
    }

    /* 7. BUTTONS (Terminal Blue) */
    button[kind="primary"] {
        background-color: #0A84FF;
        border-radius: 0px; /* Sharp corners */
        color: white;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
        border: 1px solid #0058D0;
    }
    button[kind="primary"]:hover { background-color: #0058D0; }

    /* 8. TABS (Minimalist) */
    button[data-baseweb="tab"] { background: transparent; border: none; color: #636366; font-weight: 600; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #0A84FF; border-bottom: 2px solid #0A84FF; }

    /* Hide default padding */
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
        def get_sector(row):
            if 'Bank' in str(row['Ticker']) or row['Asset_Quality'] > 0: return 'Banking & Finance'
            else: return 'Mining & Heavy Industry'
        df['Sector'] = df.apply(get_sector, axis=1)
    else:
        df = None
    return model, df

model, df_database = load_resources()

# --- 2. TERMINAL HEADER ---
c1, c2 = st.columns([0.4, 10])
with c1: st.markdown("## 📈") 
with c2: 
    st.markdown("## ACTIVISM // GOVERNANCE TERMINAL")
    st.caption("SYSTEM STATUS: ONLINE | MODEL: RANDOM FOREST v2.5")

st.markdown("---")

if model is None:
    st.error(">> SYSTEM ERROR: MODEL_FILE_MISSING. EXECUTE TRAINING SEQUENCE.")
    st.stop()

# --- 3. TABS ---
tab_trained, tab_custom = st.tabs(["🏢 CORPORATE INTELLIGENCE", "⚡ STRATEGY SIMULATOR"])

# ==============================================================================
# TAB 1: CORPORATE INTELLIGENCE (Historical Data)
# ==============================================================================
with tab_trained:

    if df_database is None:
        st.error(">> DATABASE_CONNECTION_FAILED")
    else:
        # 3 INPUTS: Industry -> Company -> Year
        c1, c2, c3 = st.columns(3)
        with c1: 
            selected_sector = st.selectbox("1. SECTOR", df_database['Sector'].unique())
        with c2: 
            filtered = df_database[df_database['Sector'] == selected_sector]['Ticker'].unique()
            selected_company = st.selectbox("2. TICKER / COMPANY", filtered)
        with c3:
            years = sorted(df_database[df_database['Ticker'] == selected_company]['Year'].unique(), reverse=True)
            selected_year = st.selectbox("3. FISCAL YEAR", years)

        # FETCH DATA
        try:
            row = df_database[(df_database['Ticker'] == selected_company) & (df_database['Year'] == selected_year)].iloc[0]

            st.markdown("### FINANCIAL SNAPSHOT")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("PROMOTER HOLDING", f"{row['Promoter_Hold']:.1%}")
            k2.metric("PROMOTER PLEDGE", f"{row['Promoter_Pledge']:.1%}")
            k3.metric("VOLATILITY", f"{row['Ann_Volatility']:.1%}")
            k4.metric("AUDITOR STATUS", "QUIT" if row['Auditor_Quit']==1 else "ACTIVE")

            st.markdown("---")

            if st.button("RUN DIAGNOSTIC", type="primary"):
                # Predict
                feature_cols = ['3Y_Stock_CAGR', 'Ann_Volatility', 'Promoter_Hold', 'Promoter_Pledge', 'Inst_Hold_Change', 'Board_Indep_Pct', 'Director_Tenure', 'CEO_Duality', 'Auditor_Quality', 'Auditor_Quit', 'Voting_Dissent', 'Whistleblower_Cnt', 'Profit_Growth', 'Governance_Ratio', 'Leverage_Risk', 'Liquidity', 'CEO_Pay_Gap', 'Div_Yield', 'Asset_Quality', 'Loan_Risk', 'Environ_Risk', 'Capex_Trap']
                input_vec = pd.DataFrame([row[feature_cols]])
                pred = model.predict(input_vec)[0]
                prob = model.predict_proba(input_vec)[0][1]

                col_res, col_log = st.columns([1, 1.5])

                with col_res:
                    if pred == 1:
                        st.markdown(f"""
                        <div class="risk-terminal-card">
                            <h2>RISK LEVEL: CRITICAL</h2>
                            <h1>{prob:.1%}</h1>
                            <p style="color:#aaa; font-size:0.8rem;">ACTIVISM PROBABILITY</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="safe-terminal-card">
                            <h2>RISK LEVEL: STABLE</h2>
                            <h1>{prob:.1%}</h1>
                            <p style="color:#aaa; font-size:0.8rem;">ACTIVISM PROBABILITY</p>
                        </div>
                        """, unsafe_allow_html=True)

                with col_log:
                    st.markdown("#### 🔍 CONTRIBUTING FACTORS")

                    # LOGIC FOR DISPLAYING FACTORS (Regardless of Risk/Safe)
                    factors = []

                    # 1. Pledge
                    if row['Promoter_Pledge'] > 0.5: factors.append(f"<div class='factor-bad'>[!] High Promoter Pledge ({row['Promoter_Pledge']:.1%})</div>")
                    else: factors.append(f"<div class='factor-good'>[OK] Low Pledge ({row['Promoter_Pledge']:.1%})</div>")

                    # 2. Asset Quality
                    if row['Asset_Quality'] > 0.05: factors.append(f"<div class='factor-bad'>[!] Asset Quality Stress (NPA {row['Asset_Quality']:.1%})</div>")
                    elif selected_sector == "Banking & Finance": factors.append(f"<div class='factor-good'>[OK] Asset Quality Stable</div>")

                    # 3. Auditor
                    if row['Auditor_Quit'] == 1: factors.append("<div class='factor-bad'>[!] Auditor Resignation Detected</div>")
                    elif row['Auditor_Quality'] == 1: factors.append("<div class='factor-good'>[OK] Big 4 Auditor Verified</div>")

                    # 4. Volatility
                    if row['Ann_Volatility'] > 0.5: factors.append(f"<div class='factor-bad'>[!] High Market Volatility ({row['Ann_Volatility']:.1%})</div>")

                    # Render Factors
                    for f in factors:
                        st.markdown(f, unsafe_allow_html=True)

        except:
            st.error(">> DATA_UNAVAILABLE_FOR_SELECTED_PERIOD")

# ==============================================================================
# TAB 2: STRATEGY SIMULATOR
# ==============================================================================
with tab_custom:
    st.markdown("### ⚡ SCENARIO BUILDER")

    with st.form("custom_form"):
        # 1. SETUP
        c1, c2 = st.columns(2)
        custom_name = c1.text_input("SCENARIO LABEL", value="Scenario Alpha")
        custom_sector = c2.selectbox("TARGET SECTOR", ("Banking & Finance", "Mining & Heavy Industry"))

        st.markdown("---")

        # 2. UNIVERSAL RATIOS
        st.markdown("#### 🌐 GOVERNANCE VECTORS")
        u1, u2, u3, u4 = st.columns(4)
        val_pledge = u1.number_input("Promoter Pledge %", value=0.0)
        val_hold = u2.number_input("Promoter Holding %", value=50.0)
        val_audit_quit = u3.selectbox("Auditor Quit?", ("No", "Yes"))
        val_vol = u4.number_input("Ann. Volatility %", value=20.0)

        # 3. SECTOR SPECIFICS
        st.markdown(f"#### 🏭 {custom_sector.upper()} METRICS")
        s1, s2, s3, s4 = st.columns(4)

        val_npa, val_env, val_capex_trap = 0.0, "No", 0.0
        val_leverage, val_liquidity, val_gov_ratio = 0.0, 0.0, 0.0
        val_profit = 10.0 # Default profit

        if custom_sector == "Banking & Finance":
            val_npa = s1.number_input("GNPA % (Asset Quality)", value=0.0)
            val_profit = s2.number_input("Profit Growth %", value=10.0)
            val_leverage = s3.number_input("Capital Adequacy", value=0.15)
            val_gov_ratio = s4.number_input("ROA", value=0.02)
            val_liquidity = 0.40
            val_env = "No"
        else: 
            val_env = s1.selectbox("Environmental Fines?", ("No", "Yes"))
            val_profit = s2.number_input("Profit Growth %", value=10.0)
            val_leverage = s3.number_input("Net Debt / EBITDA", value=1.5)
            val_gov_ratio = s4.number_input("ROCE", value=0.15)
            val_npa = 0.0
            val_liquidity = 1.5

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("EXECUTE SIMULATION", type="primary", use_container_width=True)

        if submitted:
            def clean_pct(x): return x / 100.0 if x > 5.0 else x 
            audit_quit_bin = 1 if val_audit_quit == "Yes" else 0
            env_bin = 1 if val_env == "Yes" else 0

            input_data = {
                '3Y_Stock_CAGR': 0.15, 'Ann_Volatility': clean_pct(val_vol), 
                'Promoter_Hold': clean_pct(val_hold), 'Promoter_Pledge': clean_pct(val_pledge), 
                'Inst_Hold_Change': 0.00, 'Board_Indep_Pct': 0.50, 'Director_Tenure': 4.0, 
                'CEO_Duality': 0, 'Auditor_Quality': 1, 'Auditor_Quit': audit_quit_bin, 
                'Voting_Dissent': 0.00, 'Whistleblower_Cnt': 0, 'Profit_Growth': clean_pct(val_profit), 
                'Governance_Ratio': val_gov_ratio, 'Leverage_Risk': val_leverage, 
                'Liquidity': val_liquidity, 'CEO_Pay_Gap': 50.0, 'Div_Yield': 0.01, 
                'Asset_Quality': clean_pct(val_npa), 'Loan_Risk': 0.70, 
                'Environ_Risk': env_bin, 'Capex_Trap': 0.0
            }

            input_df = pd.DataFrame([input_data])
            sim_pred = model.predict(input_df)[0]
            sim_prob = model.predict_proba(input_df)[0][1]

            st.markdown("---")
            st.markdown(f"### 📊 SIMULATION REPORT: {custom_name}")

            c_res1, c_res2 = st.columns([1, 1.5])
            with c_res1:
                if sim_pred == 1:
                    st.markdown(f"""
                    <div class="risk-terminal-card">
                        <h2>PROGNOSIS: CRITICAL</h2>
                        <h1>{sim_prob:.1%}</h1>
                        <p style="color:#aaa; font-size:0.8rem;">ACTIVISM PROBABILITY</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="safe-terminal-card">
                        <h2>PROGNOSIS: STABLE</h2>
                        <h1>{sim_prob:.1%}</h1>
                        <p style="color:#aaa; font-size:0.8rem;">ACTIVISM PROBABILITY</p>
                    </div>
                    """, unsafe_allow_html=True)
            with c_res2:
                st.markdown("#### 🔍 KEY DRIVERS")
                if sim_pred == 1:
                     if val_pledge > 50: st.markdown("<div class='factor-bad'>[!] High Promoter Pledge</div>", unsafe_allow_html=True)
                     if audit_quit_bin == 1: st.markdown("<div class='factor-bad'>[!] Auditor Resignation</div>", unsafe_allow_html=True)
                     if val_npa > 5: st.markdown("<div class='factor-bad'>[!] High Bad Loans (NPA)</div>", unsafe_allow_html=True)
                else:
                     st.markdown("<div class='factor-good'>[OK] Strong Fundamentals Detected</div>", unsafe_allow_html=True)
                     st.markdown("<div class='factor-good'>[OK] No Critical Governance Flags</div>", unsafe_allow_html=True)
