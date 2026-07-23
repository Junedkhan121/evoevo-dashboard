import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="EvoEvo Live Dashboard",
    layout="wide"
)

# =========================
# THEME
# =========================

st.markdown("""
<style>

:root {
    --gold: #F5A623;
    --gold-dark: #B8790F;
    --bg: #0B0B0F;
    --panel: #171923;
    --border: #2A2A33;
}

.stApp {
    background-color: var(--bg);
    color: #FFFFFF;
}

h1, h2, h3 {
    color: var(--gold);
}

/* ---- Metric cards ---- */
[data-testid="metric-container"] {
    background-color: var(--panel);
    border: 1px solid var(--gold);
    border-radius: 12px;
    padding: 15px;
}

[data-testid="stMetricValue"] {
    color: var(--gold);
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background-color: var(--panel);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] h1 {
    color: var(--gold);
}

/* ---- Sidebar nav buttons ---- */
[data-testid="stSidebar"] button {
    width: 100%;
    text-align: left;
    border-radius: 8px;
    margin-bottom: 4px;
    font-weight: 500;
    transition: background-color 0.15s ease, color 0.15s ease;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
    background-color: var(--gold);
    color: var(--bg);
    border: none;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-primary"]:hover {
    background-color: var(--gold-dark);
    color: #FFFFFF;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
    background-color: transparent;
    color: #FFFFFF;
    border: 1px solid var(--border);
}

[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
    border-color: var(--gold);
    color: var(--gold);
}

/* ---- Regular action buttons (e.g. "Load Agents") ---- */
.main [data-testid="stBaseButton-secondary"] {
    background-color: var(--panel);
    color: var(--gold);
    border: 1px solid var(--gold);
}

.main [data-testid="stBaseButton-secondary"]:hover {
    background-color: var(--gold);
    color: var(--bg);
}

/* ---- Tables ---- */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 8px;
}

/* ---- Expander ---- */
[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# API
# =========================

CHAIN_IDS = {
    "0G": 16661,
    "BSC": 56
}

@st.cache_data(ttl=300)
def get_overview():

    url = (
        "https://api.evoevo.ai/v1/platform/home/overview"
        "?chain_id=16661"
    )

    return requests.get(
        url,
        timeout=20
    ).json()

@st.cache_data(ttl=300)
def fetch_agents_for_chain(wallet, chain_id):

    url = (
        "https://api.evoevo.ai/v1/agents"
        f"?wallet_address={wallet}"
        f"&chain_id={chain_id}"
    )

    try:
        result = requests.get(url, timeout=20).json()
    except Exception:
        return []

    if not isinstance(result, list):
        return []

    return result

def fetch_agents_all_chains(wallet):

    combined = []

    for chain_name, chain_id in CHAIN_IDS.items():

        chain_agents = fetch_agents_for_chain(wallet, chain_id)

        for a in chain_agents:
            a["chain"] = chain_name
            combined.append(a)

    return combined

# =========================
# DATA
# =========================

data = get_overview()

overview = data["overview"]

# =========================
# SIDEBAR NAVIGATION
# =========================

PAGES = [
    "Overview",
    "Agent Leaderboard",
    "Agent Analytics",
    "Network Intelligence",
    "Agent Profile Explorer",
    "Agent Comparison",
    "Domain Intelligence",
    "Agent Ranking Engine",
    "Agent Hall of Fame",
    "Agent Config Intelligence",
    "Network Growth Simulator"
]

if "page" not in st.session_state:
    st.session_state.page = PAGES[0]

st.sidebar.title("EvoEvo")

for p in PAGES:
    if st.sidebar.button(
        p,
        key=f"nav_{p}",
        use_container_width=True,
        type="primary" if st.session_state.page == p else "secondary"
    ):
        st.session_state.page = p
        st.rerun()

page = st.session_state.page 


# =====================================
# PAGE 1 - OVERVIEW
# =====================================

if page == "Overview":

    st.title("EvoEvo Live Intelligence Dashboard(0G+BSC)")

    # =========================
    # KPI CARDS
    # =========================

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Total Agents",
        f"{overview['total_agents']:,}"
    )

    c2.metric(
        "Total Predictions",
        f"{overview['agent_opinions']:,}"
    )

    c3.metric(
        "Memories",
        f"{overview['memory_count']:,}"
    )

    c4.metric(
        "Markets",
        f"{overview['total_markets']:,}"
    )

    c5,c6,c7,c8 = st.columns(4)

    c5.metric(
        "Completed Topics",
        f"{overview['completed_topics']:,}"
    )

    c6.metric(
        "LLM Tokens",
        f"{overview['llm_total_tokens']:,}"
    )

    # =========================
    # TABLE
    # =========================

    st.subheader("Platform Metrics")

    df = pd.DataFrame({
        "Metric":[
            "Total Agents",
            "Total Predictions",
            "Memories",
            "Markets",
            "Completed Topics",
            "LLM Tokens"
        ],
        "Value":[
            overview["total_agents"],
            overview["agent_opinions"],
            overview["memory_count"],
            overview["total_markets"],
            overview["completed_topics"],
            overview["llm_total_tokens"]
        ]
    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # RAW JSON
    # =========================

    with st.expander("View Raw API Response"):

        st.json(data)

# =====================================
# PAGE 2 - AGENT LEADERBOARD
# =====================================

elif page == "Agent Leaderboard":

    st.title("Agent Leaderboard")

    wallet = st.text_input(
        "Wallet Address",
        value=""
    )

    if st.button("Load Agents"):

        agents = fetch_agents_all_chains(wallet)

        rows = []

        for a in agents:

            rows.append({
                "Name": a.get("name"),
                "Chain": a.get("chain"),
                "Level": a.get("level"),
                "XP": a.get("xp"),
                "Win Rate %": round(
                    a.get("win_rate", 0) * 100,
                    2
                ),
                "Predictions": a.get("total_predictions"),
                "Wins": a.get("total_wins"),
                "Rating Points": a.get("rating_points"),
                "Memories": a.get("memory_count"),
                "Win Streak": a.get("current_win_streak"),
                "Potential Return %": round(
                    a.get("potential_return_pct", 0),
                    2
                ),
                "Domain": ",".join(
                    a.get("domain_focus", [])
                ),
                "Risk": a.get("risk_preference"),
                "Style": a.get("style")
            })

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Top Agent")

        if len(df) > 0:

            top = df.sort_values(
                "Rating Points",
                ascending=False
            ).iloc[0]

            c1,c2,c3,c4 = st.columns(4)

            c1.metric(
                "Name",
                top["Name"]
            )

            c2.metric(
                "Level",
                top["Level"]
            )

            c3.metric(
                "Win Rate",
                f"{top['Win Rate %']}%"
            )

            c4.metric(
                "Rating",
                top["Rating Points"]
            )
# =====================================
# PAGE 3 - AGENT ANALYTICS
# =====================================

elif page == "Agent Analytics":

    st.title("Agent Analytics")

    wallet = st.text_input(
        "Wallet Address",
        value="",
        key="analytics_wallet"
    )

    agents = fetch_agents_all_chains(wallet)

    rows = []

    for a in agents:

        rows.append({
            "Name": a.get("name"),
            "Chain": a.get("chain"),
            "Level": a.get("level"),
            "XP": a.get("xp"),
            "Win Rate": round(
                a.get("win_rate", 0) * 100,
                2
            ),
            "Rating": a.get("rating_points"),
            "Memories": a.get("memory_count"),
            "Predictions": a.get("total_predictions"),
            "Win Streak": a.get("current_win_streak"),
            "Domain": ",".join(
                a.get("domain_focus", [])
            ),
            "Risk": a.get("risk_preference"),
            "Style": a.get("style")
        })

    df = pd.DataFrame(rows)

    if len(df) == 0:

        st.warning("No agents found")

    else:

        st.subheader("Win Rate Distribution")

        st.bar_chart(
            df.set_index("Name")["Win Rate"]
        )

        st.subheader("Level Distribution")

        st.bar_chart(
            df.set_index("Name")["Level"]
        )

        st.subheader("Rating Distribution")

        st.bar_chart(
            df.set_index("Name")["Rating"]
        )

        st.subheader("Memory Distribution")

        st.bar_chart(
            df.set_index("Name")["Memories"]
        )

        st.subheader("Predictions Distribution")

        st.bar_chart(
            df.set_index("Name")["Predictions"]
        )

        st.subheader("Agent Dataset")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
# =====================================
# PAGE 4 - NETWORK INTELLIGENCE
# =====================================

elif page == "Network Intelligence":

    st.title("Network Intelligence")

    overview = get_overview()["overview"]

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Agents",
        f"{overview['total_agents']:,}"
    )

    c2.metric(
        "Total Predictions",
        f"{overview['agent_opinions']:,}"
    )

    c3.metric(
        "Memories",
        f"{overview['memory_count']:,}"
    )

    c4.metric(
        "Markets",
        f"{overview['total_markets']:,}"
    )

    metrics_df = pd.DataFrame({
        "Metric":[
            "Agents",
            "Total Predictions",
            "Memories",
            "Markets",
            "Completed Topics",
            "Predictions"
        ],
        "Value":[
            overview["total_agents"],
            overview["agent_opinions"],
            overview["memory_count"],
            overview["total_markets"],
            overview["completed_topics"],
            overview["predictions_completed"]
        ]
    })

    st.subheader("Network Scale")

    st.bar_chart(
        metrics_df.set_index("Metric")
    )

    st.subheader("Raw Metrics")

    st.dataframe(
        metrics_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Network Ratios")

    ratio_df = pd.DataFrame({
        "Metric":[
            "predictions per Agent",
            "Memories per Agent",
            "Predictions per Market"
        ],
        "Value":[
            round(
                overview["agent_opinions"] /
                overview["total_agents"],
                2
            ),
            round(
                overview["memory_count"] /
                overview["total_agents"],
                2
            ),
            round(
                overview["predictions_completed"] /
                overview["total_markets"],
                2
            )
        ]
    })

    st.dataframe(
        ratio_df,
        use_container_width=True,
        hide_index=True
    )

# =====================================
# PAGE 6 - AGENT PROFILE EXPLORER
# =====================================

elif page == "Agent Profile Explorer":

    st.title("Agent Profile Explorer")

    wallet = st.text_input(
        "Wallet Address",
        value=""
    )

    if st.button("Load Profile"):

        agents = fetch_agents_all_chains(wallet)

        if len(agents) == 0:

            st.warning("No agents found")

        else:

            for agent in agents:

                st.markdown("---")

                st.subheader(agent["name"])

                c1,c2,c3,c4 = st.columns(4)

                c1.metric(
                    "Level",
                    agent["level"]
                )

                c2.metric(
                    "XP",
                    agent["xp"]
                )

                c3.metric(
                    "Win Rate",
                    f"{round(agent['win_rate']*100,2)}%"
                )

                c4.metric(
                    "Rating",
                    agent["rating_points"]
                )

                c5,c6,c7,c8 = st.columns(4)

                c5.metric(
                    "Predictions",
                    agent["total_predictions"]
                )

                c6.metric(
                    "Wins",
                    agent["total_wins"]
                )

                c7.metric(
                    "Memories",
                    agent["memory_count"]
                )

                c8.metric(
                    "Win Streak",
                    agent["current_win_streak"]
                )

                st.markdown("### Agent Details")

                details = pd.DataFrame({
                    "Field":[
                        "Agent ID",
                        "Chain",
                        "Domain",
                        "Style",
                        "Risk",
                        "MBTI",
                        "Model",
                        "Status",
                        "Potential Return %",
                        "LLM Tokens"
                    ],
                    "Value":[
                        agent["id"],
                        agent.get("chain"),
                        ",".join(agent["domain_focus"]),
                        agent["style"],
                        agent["risk_preference"],
                        agent["mbti"],
                        agent["llm_model"],
                        agent["status"],
                        round(agent["potential_return_pct"],2),
                        agent["llm_total_tokens"]
                    ]
                })

                st.dataframe(
                    details,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("### Onchain Identity")

                if "onchain_identity" in agent:

                    st.json(
                        agent["onchain_identity"]
                    )

                st.markdown("### Prompt")

                st.code(
                    agent["prompt"]
                )
# =====================================
# PAGE 7 - AGENT COMPARISON
# =====================================

elif page == "Agent Comparison":

    st.title("Agent Comparison")

    wallet = st.text_input(
        "Wallet Address",
        value=""
    )

    agents = fetch_agents_all_chains(wallet)

    if len(agents) < 2:

        st.warning(
            "Need at least 2 agents in this wallet."
        )

    else:

        names = [
            a["name"]
            for a in agents
        ]

        col1,col2 = st.columns(2)

        with col1:

            left_name = st.selectbox(
                "Agent 1",
                names,
                key="left"
            )

        with col2:

            right_name = st.selectbox(
                "Agent 2",
                names,
                key="right"
            )

        left = next(
            a for a in agents
            if a["name"] == left_name
        )

        right = next(
            a for a in agents
            if a["name"] == right_name
        )

        st.markdown("---")

        c1,c2 = st.columns(2)

        with c1:

            st.subheader(left["name"])

            st.metric(
                "Level",
                left["level"]
            )

            st.metric(
                "XP",
                left["xp"]
            )

            st.metric(
                "Win Rate",
                f"{round(left['win_rate']*100,2)}%"
            )

            st.metric(
                "Rating",
                left["rating_points"]
            )

            st.metric(
                "Memories",
                left["memory_count"]
            )

            st.metric(
                "Predictions",
                left["total_predictions"]
            )

            st.metric(
                "Win Streak",
                left["current_win_streak"]
            )

            st.metric(
                "Potential Return %",
                round(
                    left["potential_return_pct"],
                    2
                )
            )

        with c2:

            st.subheader(right["name"])

            st.metric(
                "Level",
                right["level"]
            )

            st.metric(
                "XP",
                right["xp"]
            )

            st.metric(
                "Win Rate",
                f"{round(right['win_rate']*100,2)}%"
            )

            st.metric(
                "Rating",
                right["rating_points"]
            )

            st.metric(
                "Memories",
                right["memory_count"]
            )

            st.metric(
                "Predictions",
                right["total_predictions"]
            )

            st.metric(
                "Win Streak",
                right["current_win_streak"]
            )

            st.metric(
                "Potential Return %",
                round(
                    right["potential_return_pct"],
                    2
                )
            )

        st.markdown("### Comparison Table")

        comparison = pd.DataFrame({
            "Metric":[
                "Chain",
                "Level",
                "XP",
                "Win Rate",
                "Rating",
                "Memories",
                "Predictions",
                "Win Streak",
                "Potential Return %"
            ],
            left["name"]:[
                left.get("chain"),
                left["level"],
                left["xp"],
                round(left["win_rate"]*100,2),
                left["rating_points"],
                left["memory_count"],
                left["total_predictions"],
                left["current_win_streak"],
                round(left["potential_return_pct"],2)
            ],
            right["name"]:[
                right.get("chain"),
                right["level"],
                right["xp"],
                round(right["win_rate"]*100,2),
                right["rating_points"],
                right["memory_count"],
                right["total_predictions"],
                right["current_win_streak"],
                round(right["potential_return_pct"],2)
            ]
        })

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )
# =====================================
# PAGE 8 - DOMAIN INTELLIGENCE
# =====================================

elif page == "Domain Intelligence":

    st.title("Domain Intelligence")

    wallet = st.text_input(
        "Wallet Address",
        value="",
        key="domain_wallet"
    )

    agents = fetch_agents_all_chains(wallet)

    rows = []

    for a in agents:

        domains = a.get(
            "domain_focus",
            []
        )

        for domain in domains:

            rows.append({
                "Domain": domain,
                "Name": a["name"],
                "Chain": a.get("chain"),
                "Level": a["level"],
                "Win Rate": round(
                    a["win_rate"] * 100,
                    2
                ),
                "Rating": a["rating_points"],
                "Memories": a["memory_count"],
                "Predictions": a["total_predictions"]
            })

    df = pd.DataFrame(rows)

    if len(df) == 0:

        st.warning(
            "No domain data found"
        )

    else:

        st.subheader(
            "Domain Distribution"
        )

        domain_count = (
            df.groupby("Domain")
            .size()
            .reset_index(name="Agents")
        )

        st.bar_chart(
            domain_count.set_index(
                "Domain"
            )
        )

        st.subheader(
            "Average Win Rate by Domain"
        )

        win_df = (
            df.groupby("Domain")[
                "Win Rate"
            ]
            .mean()
            .reset_index()
        )

        st.bar_chart(
            win_df.set_index(
                "Domain"
            )
        )

        st.subheader(
            "Average Rating by Domain"
        )

        rating_df = (
            df.groupby("Domain")[
                "Rating"
            ]
            .mean()
            .reset_index()
        )

        st.bar_chart(
            rating_df.set_index(
                "Domain"
            )
        )

        st.subheader(
            "Average Level by Domain"
        )

        level_df = (
            df.groupby("Domain")[
                "Level"
            ]
            .mean()
            .reset_index()
        )

        st.bar_chart(
            level_df.set_index(
                "Domain"
            )
        )

        st.subheader(
            "Top Agents Per Domain"
        )

        top_agents = (
            df.sort_values(
                "Rating",
                ascending=False
            )
        )

        st.dataframe(
            top_agents,
            use_container_width=True,
            hide_index=True
        )
# =====================================
# PAGE 9 - AGENT RANKING ENGINE
# =====================================

elif page == "Agent Ranking Engine":

    st.title("Agent Ranking Engine")

    st.caption(
        "Custom ranking system built on top of EvoEvo data"
    )

    wallet = st.text_input(
        "Wallet Address",
        value="",
        key="ranking_wallet"
    )

    agents = fetch_agents_all_chains(wallet)

    rows = []

    for a in agents:

        rows.append({
            "Name": a["name"],
            "Chain": a.get("chain"),
            "Level": a["level"],
            "Win Rate": round(
                a["win_rate"] * 100,
                2
            ),
            "Rating": a["rating_points"],
            "Memories": a["memory_count"],
            "Win Streak": a["current_win_streak"]
        })

    df = pd.DataFrame(rows)

    if len(df) == 0:

        st.warning("No agents found")

    else:

        # Normalize

        df["WR_N"] = (
            df["Win Rate"] /
            df["Win Rate"].max()
        )

        df["RT_N"] = (
            df["Rating"] /
            df["Rating"].max()
        )

        df["LV_N"] = (
            df["Level"] /
            df["Level"].max()
        )

        df["MM_N"] = (
            df["Memories"] /
            df["Memories"].max()
        )

        df["WS_N"] = (
            df["Win Streak"] /
            max(
                df["Win Streak"].max(),
                1
            )
        )

        # NeoScore

        df["NeoScore"] = (

            df["WR_N"] * 40 +

            df["RT_N"] * 25 +

            df["LV_N"] * 15 +

            df["MM_N"] * 10 +

            df["WS_N"] * 10

        )

        df["NeoScore"] = (
            df["NeoScore"]
            .round(2)
        )

        df = df.sort_values(
            "NeoScore",
            ascending=False
        )

        df.insert(
            0,
            "Rank",
            range(
                1,
                len(df) + 1
            )
        )

        st.subheader(
            "Custom Agent Rankings"
        )

        st.dataframe(
            df[
                [
                    "Rank",
                    "Name",
                    "NeoScore",
                    "Win Rate",
                    "Rating",
                    "Level",
                    "Memories",
                    "Win Streak"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.subheader(
            "Top 10 Agents"
        )

        st.bar_chart(
            df.head(10)
            .set_index("Name")
            [["NeoScore"]]
        )

        st.subheader(
            "Ranking Formula"
        )

        st.code(
            """
NeoScore =
40% Win Rate
25% Rating
15% Level
10% Memories
10% Win Streak
            """
        )
# =====================================
# PAGE 10 - AGENT HALL OF FAME
# =====================================

elif page == "Agent Hall of Fame":

    st.title("Agent Hall of Fame")

    wallet = st.text_input(
        "Wallet Address",
        value="",
        key="hof_wallet"
    )

    agents = fetch_agents_all_chains(wallet)

    rows = []

    for a in agents:

        rows.append({
            "Name": a["name"],
            "Chain": a.get("chain"),
            "Level": a["level"],
            "Win Rate": round(
                a["win_rate"] * 100,
                2
            ),
            "Rating": a["rating_points"],
            "Memories": a["memory_count"],
            "Win Streak": a["current_win_streak"],
            "Predictions": a["total_predictions"]
        })

    df = pd.DataFrame(rows)

    if len(df) == 0:

        st.warning("No agents found")

    else:

        best_wr = df.loc[
            df["Win Rate"].idxmax()
        ]

        best_level = df.loc[
            df["Level"].idxmax()
        ]

        best_rating = df.loc[
            df["Rating"].idxmax()
        ]

        best_memory = df.loc[
            df["Memories"].idxmax()
        ]

        best_streak = df.loc[
            df["Win Streak"].idxmax()
        ]

        best_predictions = df.loc[
            df["Predictions"].idxmax()
        ]

        st.subheader("Award Winners")

        c1,c2,c3 = st.columns(3)

        c1.metric(
            "Highest Win Rate",
            best_wr["Name"],
            f"{best_wr['Win Rate']}%"
        )

        c2.metric(
            "Highest Level",
            best_level["Name"],
            f"Level {best_level['Level']}"
        )

        c3.metric(
            "Highest Rating",
            best_rating["Name"],
            best_rating["Rating"]
        )

        c4,c5,c6 = st.columns(3)

        c4.metric(
            "Most Memories",
            best_memory["Name"],
            best_memory["Memories"]
        )

        c5.metric(
            "Longest Win Streak",
            best_streak["Name"],
            best_streak["Win Streak"]
        )

        c6.metric(
            "Most Predictions",
            best_predictions["Name"],
            best_predictions["Predictions"]
        )

        st.markdown("---")

        st.subheader("Full Hall of Fame")

        awards = pd.DataFrame({

            "Award":[
                "Highest Win Rate",
                "Highest Level",
                "Highest Rating",
                "Most Memories",
                "Longest Win Streak",
                "Most Predictions"
            ],

            "Winner":[
                best_wr["Name"],
                best_level["Name"],
                best_rating["Name"],
                best_memory["Name"],
                best_streak["Name"],
                best_predictions["Name"]
            ]

        })

        st.dataframe(
            awards,
            use_container_width=True,
            hide_index=True
        )

# =====================================
# PAGE 5 - AGENT CONFIG INTELLIGENCE
# =====================================

elif page == "Agent Config Intelligence":

    st.title("Agent Config Intelligence")

    config_url = (
        "https://api.evoevo.ai/v1/agents/configs"
    )

    config = requests.get(
        config_url
    ).json()

    # =====================
    # DOMAINS
    # =====================

    st.subheader("Available Domains")

    domains = pd.DataFrame(
        config["domains"]
    )

    st.dataframe(
        domains,
        use_container_width=True,
        hide_index=True
    )

    # =====================
    # RISK PROFILES
    # =====================

    st.subheader("Risk Preferences")

    risk = pd.DataFrame(
        config["risk_preferences"]
    )

    st.dataframe(
        risk,
        use_container_width=True,
        hide_index=True
    )

    # =====================
    # MODELS
    # =====================

    st.subheader("Available Models")

    models = pd.DataFrame(
        config["models"]
    )

    st.dataframe(
        models,
        use_container_width=True,
        hide_index=True
    )

    # =====================
    # STYLES
    # =====================

    st.subheader("Agent Styles")

    styles = pd.DataFrame(
        config["styles"]
    )

    st.dataframe(
        styles,
        use_container_width=True,
        hide_index=True
    )

    # =====================
    # AVATARS
    # =====================

    st.subheader("Avatar Presets")

    avatars = pd.DataFrame(
        config["avatar_presets"]
    )

    st.metric(
        "Total Avatars",
        len(avatars)
    )

    st.dataframe(
        avatars[
            ["id","label"]
        ],
        use_container_width=True,
        hide_index=True
    )

    # =====================
    # SYSTEM DEFAULTS
    # =====================

    st.subheader("System Defaults")

    defaults = pd.DataFrame(
        [
            {
                "Setting": k,
                "Value": v
            }
            for k,v in config["defaults"].items()
        ]
    )

    st.dataframe(
        defaults,
        use_container_width=True,
        hide_index=True
    )
# =====================================
# PAGE 12 - NETWORK GROWTH SIMULATOR
# =====================================

elif page == "Network Growth Simulator":

    st.title("Network Growth Simulator")

    overview = get_overview()["overview"]

    agents = overview["total_agents"]
    opinions = overview["agent_opinions"]
    memories = overview["memory_count"]

    growth = st.slider(
        "Monthly Growth %",
        1,
        100,
        20
    )

    months = [1,3,6,12]

    rows = []

    for m in months:

        factor = (
            (1 + growth/100)
            ** m
        )

        rows.append({

            "Months": m,

            "Projected Agents":
            int(agents * factor),

            "Projected Opinions":
            int(opinions * factor),

            "Projected Memories":
            int(memories * factor)

        })

    sim_df = pd.DataFrame(rows)

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "Current Agents",
        f"{agents:,}"
    )

    c2.metric(
        "Total Predictions",
        f"{opinions:,}"
    )

    c3.metric(
        "Current Memories",
        f"{memories:,}"
    )

    st.subheader(
        "Growth Projection"
    )

    st.dataframe(
        sim_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "Projected Agent Growth"
    )

    st.line_chart(
        sim_df.set_index(
            "Months"
        )[
            "Projected Agents"
        ]
    )

    st.subheader(
        "Projected Memory Growth"
    )

    st.line_chart(
        sim_df.set_index(
            "Months"
        )[
            "Projected Memories"
        ]
    )
