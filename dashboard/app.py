import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Traffic Signal Optimization",
    page_icon="🚦",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("🚦 AI Traffic Signal Optimization")

st.markdown(
    """
    ### Reinforcement Learning Based Traffic Signal Control

    This dashboard compares three traffic signal
    control strategies across multiple traffic scenarios:

    **Fixed-Time | Adaptive | RL-PPO**
    """
)


# ==========================================
# LOAD RESULTS
# ==========================================

@st.cache_data
def load_results():

    df = pd.read_csv(
        "analysis/results.csv"
    )

    return df


df = load_results()


# ==========================================
# CONTROLLER NAMES
# ==========================================

controllers = [
    "Fixed-Time",
    "Adaptive",
    "RL-PPO"
]


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Dashboard Controls")

selected_controllers = st.sidebar.multiselect(
    "Select Controllers",
    controllers,
    default=controllers
)

selected_seeds = st.sidebar.multiselect(
    "Select Seeds",
    sorted(df["seed"].unique()),
    default=sorted(df["seed"].unique())
)


# ==========================================
# FILTER DATA
# ==========================================

filtered_df = df[
    df["controller"].isin(selected_controllers)
    &
    df["seed"].isin(selected_seeds)
]


# ==========================================
# KPI DATA
# ==========================================

summary = (
    filtered_df
    .groupby("controller")
    .agg(
        average_waiting_time=(
            "average_waiting_time",
            "mean"
        ),

        average_queue=(
            "average_queue",
            "mean"
        ),

        maximum_queue=(
            "maximum_queue",
            "mean"
        ),

        vehicles_passed=(
            "vehicles_passed",
            "mean"
        ),

        vehicles_spawned=(
            "vehicles_spawned",
            "mean"
        ),

        total_reward=(
            "total_reward",
            "mean"
        )
    )
    .reset_index()
)


# ==========================================
# KPI SECTION
# ==========================================

st.subheader("📊 Performance Summary")


if len(summary) > 0:

    columns = st.columns(len(summary))

    for column, (_, row) in zip(
        columns,
        summary.iterrows()
    ):

        with column:

            st.markdown(
                f"### {row['controller']}"
            )

            st.metric(
                "Waiting Time",
                f"{row['average_waiting_time']:.2f} sec"
            )

            st.metric(
                "Average Queue",
                f"{row['average_queue']:.2f}"
            )

            st.metric(
                "Vehicles Passed",
                f"{row['vehicles_passed']:.1f}"
            )


# ==========================================
# SEPARATOR
# ==========================================

st.divider()


# ==========================================
# WAITING TIME
# ==========================================

st.subheader("⏱️ Average Waiting Time")

waiting_data = (
    filtered_df
    .groupby("controller")[
        "average_waiting_time"
    ]
    .mean()
)


fig, ax = plt.subplots()

waiting_data.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel(
    "Waiting Time (seconds)"
)

ax.set_xlabel(
    "Controller"
)

ax.set_title(
    "Average Waiting Time by Controller"
)

ax.tick_params(
    axis="x",
    rotation=0
)

st.pyplot(fig)

plt.close(fig)


# ==========================================
# QUEUE LENGTH
# ==========================================

st.subheader("🚗 Average Queue Length")

queue_data = (
    filtered_df
    .groupby("controller")[
        "average_queue"
    ]
    .mean()
)


fig, ax = plt.subplots()

queue_data.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel(
    "Average Queue (vehicles)"
)

ax.set_xlabel(
    "Controller"
)

ax.set_title(
    "Average Queue Length by Controller"
)

ax.tick_params(
    axis="x",
    rotation=0
)

st.pyplot(fig)

plt.close(fig)


# ==========================================
# MAXIMUM QUEUE
# ==========================================

st.subheader("🚧 Maximum Queue")

max_queue_data = (
    filtered_df
    .groupby("controller")[
        "maximum_queue"
    ]
    .mean()
)


fig, ax = plt.subplots()

max_queue_data.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel(
    "Maximum Queue (vehicles)"
)

ax.set_xlabel(
    "Controller"
)

ax.set_title(
    "Average Maximum Queue"
)

ax.tick_params(
    axis="x",
    rotation=0
)

st.pyplot(fig)

plt.close(fig)


# ==========================================
# VEHICLES PASSED
# ==========================================

st.subheader("🚙 Vehicles Passed")

passed_data = (
    filtered_df
    .groupby("controller")[
        "vehicles_passed"
    ]
    .mean()
)


fig, ax = plt.subplots()

passed_data.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel(
    "Vehicles Passed"
)

ax.set_xlabel(
    "Controller"
)

ax.set_title(
    "Average Vehicles Passed"
)

ax.tick_params(
    axis="x",
    rotation=0
)

st.pyplot(fig)

plt.close(fig)


# ==========================================
# TRAFFIC VOLUME
# ==========================================

st.subheader("📈 Traffic Volume")

volume_data = (
    filtered_df
    .groupby("controller")[
        "vehicles_spawned"
    ]
    .mean()
)


fig, ax = plt.subplots()

volume_data.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel(
    "Vehicles Spawned"
)

ax.set_xlabel(
    "Controller"
)

ax.set_title(
    "Average Traffic Volume"
)

ax.tick_params(
    axis="x",
    rotation=0
)

st.pyplot(fig)

plt.close(fig)


# ==========================================
# RL REWARD
# ==========================================

st.subheader("🧠 RL-PPO Training Reward")

rl_data = filtered_df[
    filtered_df["controller"] == "RL-PPO"
]


if not rl_data.empty:

    reward_data = (
        rl_data
        .groupby("seed")[
            "total_reward"
        ]
        .mean()
    )

    fig, ax = plt.subplots()

    reward_data.plot(
        kind="bar",
        ax=ax
    )

    ax.set_ylabel(
        "Total Reward"
    )

    ax.set_xlabel(
        "Random Seed"
    )

    ax.set_title(
        "RL-PPO Reward Across Traffic Scenarios"
    )

    ax.tick_params(
        axis="x",
        rotation=0
    )

    st.pyplot(fig)

    plt.close(fig)


# ==========================================
# DETAILED RESULTS
# ==========================================

st.divider()

st.subheader("📋 Detailed Results")

display_df = filtered_df.copy()

display_df["average_waiting_time"] = (
    display_df["average_waiting_time"]
    .round(2)
)

display_df["average_queue"] = (
    display_df["average_queue"]
    .round(2)
)

display_df["maximum_queue"] = (
    display_df["maximum_queue"]
    .round(2)
)

display_df["total_reward"] = (
    display_df["total_reward"]
    .round(2)
)

st.dataframe(
    display_df,
    use_container_width=True
)


# ==========================================
# FINAL SUMMARY
# ==========================================

st.divider()

st.subheader("🔎 Experiment Summary")

st.markdown(
    """
    The experiment evaluates traffic signal control
    across **10 different random traffic scenarios**.

    The RL-PPO agent uses reinforcement learning to
    decide when to keep or switch the traffic signal.

    The comparison includes:

    - Fixed-Time control
    - Adaptive rule-based control
    - PPO reinforcement learning
    - Average waiting time
    - Queue length
    - Maximum queue
    - Vehicles passed
    - Traffic volume
    - RL reward
    """
)