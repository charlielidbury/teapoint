def get_mutuals(target_uid, connection_graph):
    # tally of 2nd degree connections and their 
    # connection path strength
    mutuals = dict()
    
    
    first_degree_connections = connection_graph[target_uid]
    for fst_connection_uid, fst_connection_strength in first_degree_connections.items():
        second_degree_connections = connection_graph[fst_connection_uid]
        for snd_connection_uid, snd_connection_strength in second_degree_connections.items():
            # we don't want to suggest people who are already connections
            if snd_connection_uid in first_degree_connections or snd_connection_uid == target_uid:
                continue
                
            # we calculate the overall connection strength for that path as the product of both
            # the middle connection's strengths
            overall_connection_strength = fst_connection_strength * snd_connection_strength
            mutuals[snd_connection_uid] = mutuals.get(snd_connection_uid, 0) + overall_connection_strength
    
    return dict(sorted(mutuals.items(), key=lambda x: x[1], reverse=True))

