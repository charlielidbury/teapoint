# takes in a list of rows of sql messages, returns a graph
from re import M


def create_connections_graph(messages):
    graph = dict()
    messages = [SQLMessage(row) for row in messages]
    for message in messages:
        sender = message.sender
        receiver = message.reciever
        if not graph.get(sender):
            graph[sender] = dict()
        graph[sender][receiver] = graph[sender].get(receiver, 0) + 1
    return graph

class SQLMessage:
    def __init__(self, sql_row):
        self.time = sql_row[1]
        self.reciever = sql_row[2]
        self.sender = sql_row[3]
        self.content = sql_row[4]