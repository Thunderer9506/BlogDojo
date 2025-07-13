import random

def generate_random_pfp(username):
    seeds = ["cat", "robot", "wizard", "ninja", "alien"]
    seed = random.choice(seeds) + username
    return f"https://api.dicebear.com/7.x/adventurer/svg?seed={seed}"

print(generate_random_pfp("afa8c6ae-62ec-4577-9c0e-87dceae09a3c"))