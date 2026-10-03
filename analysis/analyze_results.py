import pandas as pd


# Load experiment results
df = pd.read_csv("analysis/results.csv")


print("\n======================================")
print("TRAFFIC SIGNAL RESULTS")
print("======================================\n")


# Calculate average performance
summary = (
    df.groupby("controller")
    .agg({
        "vehicles_spawned": "mean",
        "vehicles_passed": "mean",
        "average_waiting_time": "mean",
        "average_queue": "mean",
        "maximum_queue": "mean"
    })
    .round(2)
)


print(summary)


print("\n======================================")
print("DETAILED RESULTS")
print("======================================\n")

for controller in df["controller"].unique():

    controller_data = df[
        df["controller"] == controller
    ]

    print(f"\n{controller}")
    print("-" * 40)

    print(
        "Average Waiting Time:",
        round(
            controller_data[
                "average_waiting_time"
            ].mean(),
            2
        )
    )

    print(
        "Average Queue:",
        round(
            controller_data[
                "average_queue"
            ].mean(),
            2
        )
    )

    print(
        "Maximum Queue:",
        round(
            controller_data[
                "maximum_queue"
            ].mean(),
            2
        )
    )

    print(
        "Vehicles Passed:",
        round(
            controller_data[
                "vehicles_passed"
            ].mean(),
            2
        )
    )