from stable_baselines3 import PPO

from environment.traffic_env import TrafficEnv


# ==========================================
# CREATE ENVIRONMENT
# ==========================================

env = TrafficEnv()


# ==========================================
# CREATE PPO MODEL
# ==========================================

model = PPO(
    "MlpPolicy",
    env,

    verbose=1,

    learning_rate=0.0003,

    n_steps=2048,

    batch_size=64,

    gamma=0.99,

    gae_lambda=0.95,

    ent_coef=0.01,

    seed=42
)


# ==========================================
# TRAIN MODEL
# ==========================================

print()
print("================================")
print("Starting Improved PPO Training")
print("================================")
print()

model.learn(
    total_timesteps=200_000
)


# ==========================================
# SAVE MODEL
# ==========================================

model.save(
    "models/traffic_ppo"
)


print()
print("================================")
print("Training Completed!")
print("================================")
print()

print(
    "Model saved to: models/traffic_ppo"
)

print()