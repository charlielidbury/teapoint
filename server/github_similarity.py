from datetime import datetime
from github import Github
from collections import Counter

import os
import math

from functools import lru_cache

from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("GITHUB_CLIENT_ID")
client_secret = os.getenv("GITHUB_CLIENT_SECRET")

g = Github(client_id, client_secret)

MIN_THRESHOLD = 0.05

def language_breakdown(repos):
    return [Counter(r.get_languages()) for r in repos]

def language_sums(repos):
    return sum(language_breakdown(repos), Counter())

def normalised_values(lsum):
    total = sum(lsum.values())

    for c in lsum:
        lsum[c] /= total

    return lsum

@lru_cache(maxsize=None)
def get_user_languages(username):
    user = g.get_user(username)
    repos_single = language_sums(user.get_repos())

    # Weight repos:starred 4:1
    repos = Counter({k: v * 4 for k, v in repos_single.items()})
    starred = language_sums(user.get_starred())

    weighted = normalised_values(repos + starred)
    pruned = {l: w for l, w in weighted.items() if w >= MIN_THRESHOLD}
    
    return normalised_values(pruned)

def squared_sum_sqrt(v):
    return math.sqrt(sum(x * x for x in v))

# Cosine similarity
def compute_similarity(first, second):
    (i1, i2) = (first, second) if len(first) > len(second) else (second, first)

    v1 = list(i1.values())
    v2 = [i2[k] if k in i2 else 0 for k in i1.keys()]

    n = sum(a * b for a, b in zip(v1, v2))
    d = squared_sum_sqrt(v1) * squared_sum_sqrt(v2)

    return 0 if d == 0 else n / d


def similarity(first, second):
    first_langs = get_user_languages(first)
    second_langs = get_user_languages(second)
    intersection = set(first_langs.keys()) & set(second_langs.keys())
    return (list(intersection), compute_similarity(first_langs, second_langs))
    