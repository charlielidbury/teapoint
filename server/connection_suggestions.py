from ast import keyword


def get_mutuals(target_uid, connection_graph):
    # tally of 2nd degree connections and their 
    # connection path strength
    mutuals_score = dict()
    
    # tracks the actual mutual connection
    mutuals = dict()
    
    first_degree_connections = connection_graph[target_uid]
    for fst_connection_uid, fst_connection_strength in first_degree_connections.items():
        second_degree_connections = connection_graph.get(fst_connection_uid, {})
        for snd_connection_uid, snd_connection_strength in second_degree_connections.items():
            # we don't want to suggest people who are already connections
            if snd_connection_uid in first_degree_connections or snd_connection_uid == target_uid:
                continue
                
            # we calculate the overall connection strength for that path as the product of both
            # the middle connection's strengths
            overall_connection_strength = fst_connection_strength * snd_connection_strength
            mutuals_score[snd_connection_uid] = mutuals_score.get(snd_connection_uid, 0) + overall_connection_strength
            mutuals[snd_connection_uid] = mutuals.get(snd_connection_uid, []) + [fst_connection_uid]
    
    return dict(sorted(mutuals_score.items(), key=lambda x: x[1], reverse=True)), mutuals


def get_similar_interest(target_uid, ranked_keywords, already_connected=[]):
    similarities = dict()
    target_keywords = ranked_keywords[target_uid]
    matched_keywords = dict()
    for friend_uid, friend_keywords in ranked_keywords.items():
      if friend_uid == target_uid or friend_uid in already_connected:
        continue
      similarities[target_uid], matches = get_keyword_similarity(target_keywords, friend_keywords)
      matched_keywords[friend_uid] = matches
    return similarities, matched_keywords


# takes two lists of keywords both ordered from rank 1 to rank n
# returns similarity based on spearmans rank
def get_keyword_similarity(keywords1, keywords2):
    keywords1_weight = { kw: (1/(rank + 2)) for rank, kw in enumerate(keywords1) }
    keywords2_weight = { kw: (1/(rank + 2)) for rank, kw in enumerate(keywords2) }

    score = 0

    matched_keywords = []
    
    for kw, kw1_weight in keywords1_weight.items():
        kw2_weight = keywords2_weight.get(kw, 0)
        score += kw1_weight * kw2_weight
        if kw2_weight > 0:
            matched_keywords.append(kw)
    
    return score, matched_keywords