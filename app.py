import streamlit as st
import pandas as pd
import joblib
import os
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ACTIVISM // TERMINAL",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- GLOBAL STATE SYNCING ---
if "global_sector" not in st.session_state:
    st.session_state.global_sector = "Banking & Finance"

def sync_tab1():
    st.session_state.global_sector = st.session_state.tab1_sector

def sync_tab2():
    st.session_state.global_sector = st.session_state.tab2_sector

# --- 🎨 UNIVERSAL DARK GLASS BACKGROUND FUNCTION ---
@st.cache_data
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

def set_background(sector_name):
    if sector_name == "Banking & Finance":
        file_path = "banking background.jpeg"
    else:
        file_path = "mining background.jpeg"

    base64_img = get_base64_of_bin_file(file_path)

    if base64_img:
        css = f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(14, 17, 23, 0.40), rgba(14, 17, 23, 0.70)), url("data:image/jpeg;base64,{base64_img}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# --- 🎨 INVINCIBLE DARK THEME CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Removed the aggressive 'span' override so the dataframe isn't broken */
    .stApp, .stApp p, .stApp label, div[data-testid="stMetricValue"] { 
        font-family: 'Inter', sans-serif !important; 
        color: #E0E0E0 !important; 
    }
    h1, h2, h3, h4 { color: #FFFFFF !important; text-transform: uppercase; letter-spacing: 1px; }

    /* Input Boxes */
    .stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div { 
        background-color: rgba(20, 20, 25, 0.85) !important; 
        color: #FFFFFF !important; 
        border: 1px solid #48484A !important; 
        border-radius: 4px !important;
    }

    /* FIX: Force Floating Dropdown Menus to be Dark */
    div[data-baseweb="popover"] > div,
    ul[data-baseweb="menu"],
    li[role="option"] {
        background-color: #1A1C24 !important;
        color: #FFFFFF !important;
    }
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #0A84FF !important;
        color: #FFFFFF !important;
    }

    /* Frosted Glass Cards */
    .prognosis-card { 
        background: rgba(20, 20, 25, 0.65); 
        backdrop-filter: blur(12px); 
        padding: 20px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .risk-border { border-left: 6px solid #EF5350; }
    .safe-border { border-left: 6px solid #66BB6A; }

    .risk-title { color: #EF5350 !important; font-size: 1.1rem; font-weight: 700; margin: 0; }
    .safe-title { color: #66BB6A !important; font-size: 1.1rem; font-weight: 700; margin: 0; }
    .prob-score { color: #FFFFFF !important; font-size: 2.8rem; font-weight: 700; margin: 0; padding-top: 5px; }

    /* Diagnostic Log Styling */
    .factor-bad { color: #EF5350 !important; font-weight: 600; font-size: 0.95rem; margin-bottom: 6px; }
    .factor-good { color: #66BB6A !important; font-weight: 600; font-size: 0.95rem; margin-bottom: 6px; }

    button[kind="primary"] { background-color: #0A84FF; border-radius: 4px; color: white !important; text-transform: uppercase; font-weight: 700; border: none; }
</style>
""", unsafe_allow_html=True)

# --- INJECT BACKGROUND ONCE GLOBALLY ---
set_background(st.session_state.global_sector)

# --- 1. DATA LOADING ---
@st.cache_resource
def load_resources():
    if not os.path.exists('activism_model.pkl'): return None, None
    model = joblib.load('activism_model.pkl')
    if os.path.exists('Final_Dataset_Cleaned.csv'):
        df = pd.read_csv('Final_Dataset_Cleaned.csv')
        df['Sector'] = df.apply(lambda r: 'Banking & Finance' if 'Bank' in str(r['Ticker']) or r['Asset_Quality'] > 0 else 'Mining & Heavy Industry', axis=1)
    else: df = None
    return model, df

model, df_database = load_resources()
def to_dec(x): return x / 100.0

feature_cols = ['3Y_Stock_CAGR', 'Ann_Volatility', 'Promoter_Hold', 'Promoter_Pledge', 'Inst_Hold_Change', 'Board_Indep_Pct', 'Director_Tenure', 'CEO_Duality', 'Auditor_Quality', 'Auditor_Quit', 'Voting_Dissent', 'Whistleblower_Cnt', 'Profit_Growth', 'Governance_Ratio', 'Leverage_Risk', 'Liquidity', 'CEO_Pay_Gap', 'Div_Yield', 'Asset_Quality', 'Loan_Risk', 'Environ_Risk', 'Capex_Trap']

sec_list = ["Banking & Finance", "Mining & Heavy Industry"]
if df_database is not None: sec_list = sorted(df_database['Sector'].unique())

# --- 2. HEADER ---
st.markdown("## 📈 CORPORATE ACTIVISM DIAGNOSTIC TOOL")
st.caption("v5.3 |DARK GLASS UI")
st.markdown("---")

tab1, tab2 = st.tabs(["🏢 CORPORATE INTELLIGENCE", "⚡ SCENARIO ANALYSIS"])

# ==============================================================================
# TAB 1: CORPORATE INTELLIGENCE
# ==============================================================================
with tab1:
    if df_database is None: st.error(">> DATABASE_OFFLINE")
    else:
        c1, c2, c3 = st.columns(3)
        with c1: 
            selected_sector = st.selectbox(
                "1. SECTOR", 
                sec_list, 
                index=sec_list.index(st.session_state.global_sector),
                key="tab1_sector",
                on_change=sync_tab1
            )
        with c2: 
            filtered_tickers = sorted(df_database[df_database['Sector'] == selected_sector]['Ticker'].unique())
            ticker = st.selectbox("2. TICKER", filtered_tickers)
        with c3: 
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
                input_vec = pd.DataFrame([row[feature_cols]])
                prob = model.predict_proba(input_vec)[0][1]

                rc1, rc2 = st.columns([1, 1.5])
                with rc1:
                    if prob >= 0.50: 
                        st.markdown(f'<div class="prognosis-card risk-border"><p class="risk-title">PROGNOSIS: CRITICAL RISK</p><p class="prob-score">{prob:.1%}</p><p style="margin:0;">REVOLT PROBABILITY</p></div>', unsafe_allow_html=True)
                    else: 
                        st.markdown(f'<div class="prognosis-card safe-border"><p class="safe-title">PROGNOSIS: STABLE</p><p class="prob-score">{prob:.1%}</p><p style="margin:0;">REVOLT PROBABILITY</p></div>', unsafe_allow_html=True)
                with rc2:
                    st.markdown("#### 🔍 GOVERNANCE AUDIT LOG")
                    if row['Promoter_Pledge'] > 0.4: st.markdown(f"<div class='factor-bad'>[!] HIGH PLEDGE: {row['Promoter_Pledge']:.1%} encumbered.</div>", unsafe_allow_html=True)
                    if row['Auditor_Quit'] == 1: st.markdown("<div class='factor-bad'>[!] AUDITOR RESIGNATION: Major governance red flag.</div>", unsafe_allow_html=True)
                    if row['Voting_Dissent'] > 0.05: st.markdown(f"<div class='factor-bad'>[!] DISSENT: Voting opposition is high ({row['Voting_Dissent']:.1%}).</div>", unsafe_allow_html=True)
                    if row['Profit_Growth'] > 0.05: st.markdown(f"<div class='factor-good'>[OK] EARNINGS BUFFER: Profit growth ({row['Profit_Growth']:.1%}) offsets risk factors.</div>", unsafe_allow_html=True)
                    if row['Auditor_Quality'] == 1: st.markdown("<div class='factor-good'>[OK] AUDIT: Verified by Big 4 Firm.</div>", unsafe_allow_html=True)

                st.markdown("---")
                st.markdown(f"#### 🚦 5-YEAR MULTI-FACTOR RISK MATRIX: {ticker}")
                st.caption("Green = Safe/Healthy | Orange = Monitor | Red = Critical Risk Zone")

                hist_df = df_database[df_database['Ticker'] == ticker].sort_values('Year')
                heatmap_data = hist_df[['Year'] + feature_cols].set_index('Year').T

                pct_cols = ['3Y_Stock_CAGR', 'Ann_Volatility', 'Promoter_Hold', 'Promoter_Pledge', 'Inst_Hold_Change', 'Board_Indep_Pct', 'Voting_Dissent', 'Profit_Growth', 'Div_Yield', 'Asset_Quality', 'Loan_Risk']
                num_cols = [c for c in feature_cols if c not in pct_cols]

                good_is_high = ['3Y_Stock_CAGR', 'Profit_Growth', 'Div_Yield', 'Board_Indep_Pct', 'Promoter_Hold', 'Auditor_Quality', 'Loan_Risk', 'Governance_Ratio', 'Liquidity', 'Inst_Hold_Change']
                bad_is_high = [c for c in feature_cols if c not in good_is_high]

                # FIX: Explicitly style the dataframe headers to be dark with white text!
                styled_heatmap = heatmap_data.style\
                    .background_gradient(cmap='RdYlGn', axis=1, subset=(good_is_high, heatmap_data.columns))\
                    .background_gradient(cmap='RdYlGn_r', axis=1, subset=(bad_is_high, heatmap_data.columns))\
                    .format("{:.1%}", subset=(pct_cols, heatmap_data.columns))\
                    .format("{:.3f}", subset=(num_cols, heatmap_data.columns))\
                    .set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#1A1C24 !important'), ('color', '#FFFFFF !important')]},
                        {'selector': 'th.row_heading', 'props': [('background-color', '#1A1C24 !important'), ('color', '#FFFFFF !important')]},
                        {'selector': 'th.col_heading', 'props': [('background-color', '#1A1C24 !important'), ('color', '#FFFFFF !important')]}
                    ])

                # Convert the heatmap to raw HTML and inject it to bypass Streamlit's Light Mode canvas
                html_heatmap = styled_heatmap.to_html()


                st.dataframe(styled_heatmap, width="stretch", height=800)
        except Exception as e:
            st.error(f">> SYSTEM ERROR: {e}")

# ==============================================================================
# TAB 2: STRATEGY SIMULATOR 
# ==============================================================================
with tab2:
    st.markdown("### ⚡ FULL-FEATURE STRESS TEST")

    c1, c2 = st.columns(2)
    sim_name = c1.text_input("SCENARIO LABEL", "Simulation Case A")
    sim_sector = c2.selectbox(
        "INDUSTRY", 
        sec_list, 
        index=sec_list.index(st.session_state.global_sector),
        key="tab2_sector",
        on_change=sync_tab2
    )

    with st.form("sim_form"):
        st.markdown("#### 🔴 PRIMARY RISK LEVERS")
        l1, l2, l3, l4 = st.columns(4)
        v_pledge = l1.number_input("Promoter Pledge (%)", 0.0, 100.0, 90.0)
        v_dissent = l4.number_input("Voting Dissent (%)", 0.0, 100.0, 10.0)
        v_audit_quit = l3.selectbox("Auditor Quit?", (1, 0))

        v_gnpa, v_pcr, v_env, v_capex = 0.0, 0.70, 0, 0.0
        if sim_sector == "Banking & Finance":
            v_gnpa = l2.number_input("GNPA % (Asset Quality)", 0.0, 100.0, 30.0)
        else:
            v_env = l2.selectbox("Environmental Risk Flag", (0, 1))

        st.markdown("#### ⚙️ ALL REMAINING PARAMETERS (FOR PROFESSOR REVIEW)")
        e1, e2, e3, e4 = st.columns(4)
        v_hold = e1.number_input("Promoter Hold (%)", 0.0, 100.0, 50.0)
        v_profit = e2.number_input("Profit Growth (%)", -100.0, 500.0, 3.0)
        v_cagr = e3.number_input("3Y Stock CAGR (%)", -100.0, 100.0, 2.0)
        v_vol = e4.number_input("Ann. Volatility (%)", 0.0, 200.0, 30.0)

        e5, e6, e7, e8 = st.columns(4)
        v_indep = e5.number_input("Board Indep (%)", 0.0, 100.0, 50.0)
        v_tenure = e6.number_input("Director Tenure (Yrs)", 0.0, 20.0, 4.0)
        v_dual = e7.selectbox("CEO Duality (0=No, 1=Yes)", (1, 0))
        v_audit_q = e8.selectbox("Big 4 Auditor (1=Yes, 0=No)", (0, 1))

        e9, e10, e11, e12 = st.columns(4)
        v_inst = e9.number_input("Inst. Hold Change (%)", -50.0, 50.0, 10.0)
        v_whistle = e10.number_input("Whistleblower Cnt", 0, 50, 2)
        v_div = e11.number_input("Div. Yield (%)", 0.0, 20.0, 2.0)
        v_roa = e12.number_input("ROA (decimal)", value=0.005, format="%.3f")

        e13, e14, e15, e16 = st.columns(4)
        v_lev = e13.number_input("Leverage Ratio", value=3.0)
        v_liq = e14.number_input("Liquidity Ratio", value=1.2)
        v_pay = e15.number_input("CEO Pay Gap (x)", value=50.0)

        if sim_sector == "Banking & Finance":
            v_pcr = e16.number_input("PCR Ratio (decimal)", 0.0, 1.0, 0.70)
        else:
            v_capex = e16.number_input("Capex Trap Ratio", 0.0, 1.0, 0.0)

        submit = st.form_submit_button("RUN FULL SIMULATION", type="primary", width="stretch")

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
                if prob >= 0.50: 
                    st.markdown(f'<div class="prognosis-card risk-border"><p class="risk-title">PROGNOSIS: CRITICAL</p><p class="prob-score">{prob:.1%}</p><p style="margin:0;">REVOLT PROBABILITY</p></div>', unsafe_allow_html=True)
                else: 
                    st.markdown(f'<div class="prognosis-card safe-border"><p class="safe-title">PROGNOSIS: STABLE</p><p class="prob-score">{prob:.1%}</p><p style="margin:0;">REVOLT PROBABILITY</p></div>', unsafe_allow_html=True)
            with sc2:
                st.markdown("#### 🛰️ MULTI-FACTOR REASONING")
                if v_pledge > 40: st.markdown(f"<div class='factor-bad'>[!] OWNERSHIP: High Promoter Pledging ({v_pledge}%).</div>", unsafe_allow_html=True)
                if sim_sector == "Banking & Finance" and v_gnpa > 10: st.markdown(f"<div class='factor-bad'>[!] CREDIT: GNPA exceeds safety threshold ({v_gnpa}%).</div>", unsafe_allow_html=True)
                if sim_sector == "Mining & Heavy Industry" and v_env == 1: st.markdown(f"<div class='factor-bad'>[!] ESG: Major Environmental Risk detected.</div>", unsafe_allow_html=True)
                if v_audit_quit == 1: st.markdown("<div class='factor-bad'>[!] AUDIT: Auditor resignation is a critical red flag.</div>", unsafe_allow_html=True)
                if v_dissent > 5: st.markdown(f"<div class='factor-bad'>[!] DISSENT: Voting opposition is high ({v_dissent}%).</div>", unsafe_allow_html=True)

                if v_profit > 0: st.markdown(f"<div class='factor-good'>[OK] PROFIT: Positive growth ({v_profit}%) mitigates extreme risk.</div>", unsafe_allow_html=True)
                if v_cagr > 0: st.markdown(f"<div class='factor-good'>[OK] MARKET: Positive 3Y CAGR suggests surviving stock value.</div>", unsafe_allow_html=True)
                if 0.45 < prob < 0.65: st.info("💡 **Model Note:** The score is near 50-60% because severe structural risks are being partially offset by surviving business performance.")
