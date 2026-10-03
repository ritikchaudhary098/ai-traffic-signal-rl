from stable_baselines3 import PPO

from environment.traffic_env import TrafficEnv


# ==========================================
# LOAD TRAINED MODEL
# ==========================================

model = PPO.load("models/traffic_ppo")

env = TrafficEnv()


# ==========================================
# RESET ENVIRONMENT
# ==========================================

observation, _ = env.reset(seed=42)


# ==========================================
# VARIABLES
# ==========================================

total_reward = 0

action_counts = {
    0: 0,
    1: 0
}

successful_switches = 0


# ==========================================
# RUN RL AGENT
# ==========================================

for step in range(1000):

    action, _ = model.predict(
        observation,
        deterministic=True
    )

    action = int(action)

    action_counts[action] += 1

    observation, reward, terminated, truncated, info = env.step(action)

    total_reward += reward

    if info["switch_requested"]:
        successful_switches += 1

    if terminated or truncated:
        break


# ==========================================
# GET FINAL METRICS
# ==========================================

metrics = env.intersection.get_metrics()


# ==========================================
# PRINT RESULTS
# ==========================================

print()
print("==========================================")
print("        RL TRAFFIC SIGNAL RESULTS")
print("==========================================")

print()

print("Total Reward:", round(total_reward, 2))

print()

print("Actions:")
print("KEEP:", action_counts[0])
print("SWITCH:", action_counts[1])

print()

print("Successful Switches:", successful_switches)

print()

print("Traffic Metrics:")

print(
    "Vehicles Spawned:",
    metrics["vehicles_spawned"]
)

print(
    "Vehicles Passed:",
    metrics["vehicles_passed"]
)

print(
    "Average Waiting Time:",
    round(
        metrics["average_waiting_time"],
        2
    ),
    "seconds"
)

print(
    "Average Queue:",
    round(
        metrics["average_queue"],
        2
    ),
    "vehicles"
)

print(
    "Maximum Queue:",
    metrics["maximum_queue"]
)

print()

print("==========================================")