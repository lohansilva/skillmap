import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- Configuration & Styling ---
st.set_page_config(page_title="Competency Map Dashboard", layout="wide")

# Custom Dark Mode Theme Application
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #E6EDF3 !important;
        font-weight: 600;
    }
    
    /* Metrics/Cards */
    div.css-1r6slb0, div.css-12w0qpk { 
        background-color: #21262D;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 15px;
    }

    /* Custom classes for Gap Analysis */
    .gap-card {
        background-color: #21262D;
        border-left: 4px solid #FF7F50; /* Coral */
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 4px;
    }
    .gap-tech {
        font-weight: bold;
        color: #E6EDF3;
    }
    .gap-score {
        float: right;
        color: #FF7F50;
    }

</style>
""", unsafe_allow_html=True)

# --- Mock Data Generation ---
# Team Members: 4 people
# Categories: RPA, Backend, Frontend, Cloud

@st.cache_data
def get_data():
    try:
        df = pd.read_excel("resources/skills.xlsx")
        
        # Rename columns to match internal logic
        # Excel: Colaborador, Categoria, Skill, Nível (0-5)
        # Internal: Member, Category, Tech, Score
        df = df.rename(columns={
            "Colaborador": "Member",
            "Categoria": "Category",
            "Competência": "Tech",
            "Nível (0-5)": "Score"
        })
        
        # Ensure Score is numeric
        df["Score"] = pd.to_numeric(df["Score"], errors='coerce').fillna(0)
        
        return df
    except FileNotFoundError:
        st.error("File 'resources/skills.xlsx' not found. Please ensure the file exists.")
        return pd.DataFrame(columns=["Member", "Category", "Tech", "Score"])
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=["Member", "Category", "Tech", "Score"])

df = get_data()

# --- Sidebar ---
st.sidebar.title("🛠️ Settings")
selected_member = st.sidebar.selectbox("Select Team Member", df["Member"].unique())

all_cats = df["Category"].unique()
selected_cats = st.sidebar.multiselect("Filter by Category", all_cats, default=all_cats)

# Filter Data
member_data = df[(df["Member"] == selected_member) & (df["Category"].isin(selected_cats))].copy()

# --- Main Layout ---
st.title(f"Competency Map: {selected_member}")
st.markdown("### Technical Proficiency Overview")

col_radar, col_gap = st.columns([2, 1])

# --- Radar Chart (Spider Chart) ---
with col_radar:
    # Aggregate score by Category for the Radar Chart
    radar_df = member_data.groupby("Category")["Score"].mean().reset_index()
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_df['Score'],
        theta=radar_df['Category'],
        fill='toself',
        name=selected_member,
        line_color='#50C878', # Emerald
        fillcolor='rgba(80, 200, 120, 0.3)'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                gridcolor='#30363D',
                linecolor='#30363D',
                tickfont=dict(color='#8B949E')
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E6EDF3'),
        margin=dict(l=40, r=40, t=20, b=20),
        showlegend=False
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

# --- Gap Analysis (Levels 0-1) ---
with col_gap:
    st.markdown("### 🚀 Gap Analysis")
    st.markdown("<div style='font-size: 0.9em; color: #8B949E; margin-bottom: 15px;'>Skills requiring attention (Score ≤ 1)</div>", unsafe_allow_html=True)
    
    gaps = member_data[member_data["Score"] <= 1]
    
    if gaps.empty:
        st.success("No critical skill gaps found for this selection!")
    else:
        for idx, row in gaps.iterrows():
            st.markdown(f"""
            <div class="gap-card">
                <div class="gap-tech">{row['Tech']} <span style='font-size:0.8em; color:#8B949E'>({row['Category']})</span></div>
                <div class="gap-score">Level {row['Score']}</div>
                <div style="clear:both;"></div>
            </div>
            """, unsafe_allow_html=True)

# --- Horizontal Bar Chart (Detailed Skills) ---
st.markdown("### 📊 Skill Detail Breakdown")

# Color mapping logic
def get_color(score):
    if score >= 4: return '#50C878'
    elif score == 3: return '#F1C40F'
    else: return '#FF7F50'

member_data['Color'] = member_data['Score'].apply(get_color)

# Sort by Score (Ascending) so that Higher scores appear at the Top of the chart
member_data = member_data.sort_values(by="Score", ascending=True)

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    y=member_data['Tech'],
    x=member_data['Score'],
    orientation='h',
    marker=dict(color=member_data['Color']),
    text=member_data['Score'],
    textposition='auto'
))

fig_bar.update_layout(
    xaxis=dict(
        range=[0, 5.5],
        gridcolor='#30363D',
        title="Proficiency Level (0-5)",
        tickfont=dict(color='#8B949E'),
        title_font=dict(color='#8B949E')
    ),
    yaxis=dict(
        tickfont=dict(color='#E6EDF3'),
        automargin=True
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#E6EDF3'),
    height=400 + (len(member_data) * 15), # Dynamic height
    margin=dict(l=20, r=20, t=20, b=20),
)

st.plotly_chart(fig_bar, use_container_width=True)
