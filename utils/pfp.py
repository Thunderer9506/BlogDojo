import random

def generate_random_pfp(username):
    seeds = ["cat", "robot", "wizard", "ninja", "alien"]
    seed = random.choice(seeds) + username
    return f"https://api.dicebear.com/7.x/adventurer/svg?seed={seed}"