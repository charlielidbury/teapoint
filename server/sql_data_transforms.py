# takes in a list of rows of sql messages, returns a graph
from re import M


def create_connections_graph(messages):
    graph = dict()
    
    for message in messages:
        sender = message["sender"]
        receiver = message["receiver"]
        if not graph.get(sender):
            graph[sender] = dict()
        graph[sender][receiver] = graph[sender].get(receiver, 0) + 1
    
    # represent weights as a percentage of total messages sent
    for sender, connections in graph.items():
        total_messages = sum(list(connections.values()))
        for connection, messages in graph[sender].items():
            graph[sender][connection] = messages / total_messages

    return graph
