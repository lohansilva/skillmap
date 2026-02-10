import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- Configuration & Styling ---
st.set_page_config(page_title="Competency Map Dashboard", layout="wide")

# Custom Light Mode Theme Application
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #FFFFFF;
        color: #212529;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #EAEDED;
        border-right: 1px solid #DEE2E6;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #0D1B2A !important;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-top: 0px;
    }
    
    /* Metrics/Cards */
    div.css-1r6slb0, div.css-12w0qpk { 
        background-color: #FFFFFF;
        border: 1px solid #DEE2E6;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Custom classes for Gap Analysis */
    .gap-card {
        background-color: #FFFFFF;
        border-left: 4px solid #922B21; /* Darker Muted Red */
        border-top: 1px solid #E9ECEF;
        border-right: 1px solid #E9ECEF;
        border-bottom: 1px solid #E9ECEF;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .gap-tech {
        font-weight: 600;
        color: #212529;
        font-size: 1.05em;
    }
    .gap-score {
        float: right;
        color: #922B21;
        font-weight: bold;
    }
    
    /* General text adjustments */
    p, label {
        color: #495057;
    }



</style>
""", unsafe_allow_html=True)

# --- Data Loading (Sheet2 Only) ---
@st.cache_data
def get_data():
    try:
        # Load Sheet2 directly
        # Expected structure: Category, Skill, Member1, Member2...
        df_raw = pd.read_excel("resources/skills.xlsx", sheet_name="Sheet2")
        
        # Normalize headers
        # We enforce the first two columns to be 'Category' and 'Tech' to avoid naming issues
        # and match the internal logic of the app.
        if len(df_raw.columns) > 2:
            df_raw.columns.values[0] = "Category"
            df_raw.columns.values[1] = "Tech"
            
            # Identify member columns (all columns from index 2 onwards)
            member_cols = df_raw.columns[2:].tolist()
            
            # Unpivot (Melt) to create the long format: Category, Tech, Member, Score
            # This format is required for the individual dashboard views
            df_long = df_raw.melt(
                id_vars=["Category", "Tech"], 
                value_vars=member_cols, 
                var_name="Member", 
                value_name="Score"
            )
            
            # Ensure Score is numeric
            df_long["Score"] = pd.to_numeric(df_long["Score"], errors='coerce').fillna(0)
            
            return df_long
        else:
            st.error("Sheet2 structure invalid. Expected at least 3 columns (Category, Skill, Members...).")
            return pd.DataFrame()

    except FileNotFoundError:
        st.error("File 'resources/skills.xlsx' not found.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = get_data()

if df.empty:
    st.stop()

# --- Sidebar ---
st.sidebar.title("Settings")
selected_member = st.sidebar.selectbox("Select Team Member", df["Member"].unique())

# Filter Data (Member View)
member_data = df[df["Member"] == selected_member].copy()

# --- Sidebar Insights ---
if not member_data.empty:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Profile Summary")
    
    # 1. Overall Average
    avg_score = member_data['Score'].mean()
    st.sidebar.metric("Overall Average", f"{avg_score:.2f}")
    
    # 2. Top Category
    cat_scores = member_data.groupby("Category")["Score"].mean()
    if not cat_scores.empty:
        best_cat = cat_scores.idxmax()
        best_cat_score = cat_scores.max()
        st.sidebar.markdown(f"**Top Strength:**")
        st.sidebar.markdown(f"{best_cat} ({best_cat_score:.1f})")
        
    # 3. Level Distribution
    st.sidebar.markdown("---")
    st.sidebar.subheader("Level Distribution")
    
    expert_count = len(member_data[member_data['Score'] == 5])
    competent_count = len(member_data[member_data['Score'].between(3, 4)])
    apprentice_count = len(member_data[member_data['Score'].between(0, 2)])
    
    
    st.sidebar.markdown(f"**Expert (5):** {expert_count}")
    st.sidebar.markdown(f"**Competent (3-4):** {competent_count}")
    st.sidebar.markdown(f"**Apprentice (0-2):** {apprentice_count}")

# --- Main Layout ---
st.title(f"Competency Map: {selected_member}")
st.markdown("### Technical Proficiency Overview")

col_summary, col_gap = st.columns([2, 1])

# --- Executive Summary Chart (Grouped Bar) ---
with col_summary:
    st.markdown("### Average Score by Category")
    # Aggregate score by Category
    summary_df = member_data.groupby("Category")["Score"].mean().reset_index()
    
    fig_summary = go.Figure()
    fig_summary.add_trace(go.Bar(
        x=summary_df['Category'],
        y=summary_df['Score'],
        name=selected_member,
        marker_color='#566573', # Neutral Grey/Blue
        text=summary_df['Score'].apply(lambda x: f"{x:.1f}"),
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Average Score: %{y:.2f}<extra></extra>'
    ))
    
    fig_summary.update_layout(
        # title removed to align with markdown header
        yaxis=dict(
            visible=True,
            range=[0, 5.5],
            gridcolor='#E9ECEF',
            linecolor='#E9ECEF',
            title='Score',
            title_font=dict(size=12, color='#6C757D')
        ),
        xaxis=dict(
            linecolor='#E9ECEF',
            tickfont=dict(color='#212529')
        ),
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font=dict(color='#212529'),
        margin=dict(l=40, r=40, t=40, b=20),
        showlegend=False
    )
    
    st.plotly_chart(fig_summary, use_container_width=True)

# --- Gap Analysis (Levels 0-2) ---
with col_gap:
    st.markdown("### Gap Analysis (Score <= 2)")
    
    gaps = member_data[member_data["Score"] <= 2]
    
    if gaps.empty:
        st.success("No critical skill gaps found for this selection!")
    else:
        # Limit to 5 cards
        for idx, row in gaps.head(5).iterrows():
            st.markdown(f"""
            <div class="gap-card">
                <div class="gap-tech">{row['Tech']} <span style='font-size:0.8em; color:#6C757D'>({row['Category']})</span></div>
                <div class="gap-score">Level {row['Score']}</div>
                <div style="clear:both;"></div>
            </div>
            """, unsafe_allow_html=True)
            
        if len(gaps) > 5:
             st.markdown(f"<div style='font-size: 0.8em; color: #6C757D; text-align: center; margin-top: 5px;'>+ {len(gaps) - 5} more...</div>", unsafe_allow_html=True)

# --- Detailed Skills Bar Chart ---
st.markdown("### Skill Detail Breakdown")

def get_color(score):
    if score >= 4: return '#2E4053' # Dark Slate
    elif score == 3: return '#7F8C8D' # Concrete Grey
    else: return '#922B21' # Dark Red

member_data['Color'] = member_data['Score'].apply(get_color)
member_data = member_data.sort_values(by="Score", ascending=True)

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    y=member_data['Tech'],
    x=member_data['Score'],
    orientation='h',
    marker=dict(color=member_data['Color']),
    text=member_data['Score'],
    textposition='auto',
    customdata=member_data['Category'],  # Add Category data
    hovertemplate='<b>%{y}</b><br>Category: %{customdata}<br>Score: %{x}<extra></extra>'
))

fig_bar.update_layout(
    xaxis=dict(
        range=[0, 5.5],
        gridcolor='#E9ECEF',
        title="Proficiency Level (0-5)",
        tickfont=dict(color='#6C757D'),
        title_font=dict(color='#6C757D')
    ),
    yaxis=dict(
        tickfont=dict(color='#212529'),
        automargin=True
    ),
    paper_bgcolor='#FFFFFF',
    plot_bgcolor='#FFFFFF',
    font=dict(color='#212529'),
    height=400 + (len(member_data) * 15),
    margin=dict(l=20, r=20, t=20, b=20),
)

st.plotly_chart(fig_bar, use_container_width=True)

