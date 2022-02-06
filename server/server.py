import json
import connection_suggestions
import keyword_extraction
import sql_database
import sql_data_transforms
import slack_extract
import pickle
import github_similarity
from flask import Flask, jsonify

app = Flask(__name__)

last_pull_time = 0

@app.route("/home")
def hello_world():
    return "ok!"


@app.route("/pull_messages")
def pull_messages():
    global last_pull_time
    last_pull_time, updates = slack_extract.upload_conversations(last_pull_time)
    
    for [time, sender, receiver, body, keywords] in updates:
        sql_database.execute(f""" # probably correct
            INSERT INTO message(sent, sender, receiver, content, keywords)
            VALUES ({time, sender, receiver, body, pickle.dumps(keywords) })
        """)

# recc_mutual
@app.route("/find_mutuals")
def find_mutuals():
    # read data from DB
    messages = sql_database.get_messages()

    # construct connections graph
    connection_graph = sql_data_transforms.create_connections_graph(messages)

    # run mutual finder algorithm
    for message in messages:
        uid = message["sender"]
        suggs = connection_suggestions.get_mutuals(uid, connection_graph)
        # update db
        for tid, certainty in suggs.items():
            sql_database.db.execute(f"""
                INSERT INTO recc_mutual(user, target, certainty)
                VALUES ({uid}, {tid}, {certainty})
            """)
    
    return
    return jsonify({
        "success": True
    })

# recc_interests
@app.route("/find_common_interests")
def find_common_interests():
    # read data from DB
    messages = sql_database.get_messages()
    # get keywords
    ranked_keywords = keyword_extraction.get_ranked_keywords(messages)
    # run mutual finder algorithm
    uids = set([m[3] for m in messages])

    for uid in uids:
        suggs = connection_suggestions.get_similar_interest(uid, ranked_keywords)
        for tid, certainty in suggs.items():
            sql_database.db.execute(f"""
                INSERT INTO recc_interests(user, target, certainty)
                VALUES ({uid}, {tid}, {certainty})
            """)
    
    return
    return jsonify({
        "success": True
    })

# recc_git
@app.route("/find_git_friends")
def find_git_friends():
    # load all github IDs
    github_ids = None

    similarities = dict()

    for gid1 in github_ids:
        similarities[gid1] = dict()
        for gid2 in github_ids:
            if gid1 != gid2:
                similarities[gid1][gid2] = github_similarity.compute_similarity(gid1, gid2)
        # THE 5 IN FOLLOWING LINE NEEDS TO BE REPLACED WITH SOMETHING

    # upload to database

    return jsonify({
        "success": True
    })

# Which languages
# Which mutual friends you have
# Shared interests
# { git: { user,  } }
@app.route("/get_reccomendations")
def get_reccomendations():
    uid = request.args.get("uid")

    recc_mutual = dict(list(sql_database.db.execute(f"""
        SELECT user.name, user.title, user.github, recc_mutual.con
        FROM recc_mutual
        JOIN user ON user.rowid = user
        WHERE user = {uid}
        ORDER BY certainty DESC
        LIMIT 1
    """))[0])

    recc_interests = dict(list(sql_database.db.execute(f"""
        SELECT user.name, user.title, user.github, recc_mutual.con
        FROM recc_interests
        JOIN user ON user.rowid = user
        WHERE user = {uid}
        ORDER BY certainty DESC
        LIMIT 1
    """))[0])

    recc_git = dict(list(sql_database.db.execute(f"""
        SELECT user.name, user.title, user.github, recc_mutual.con
        FROM recc_git
        JOIN user ON user.rowid = user
        WHERE user = {uid}
        ORDER BY certainty DESC
        LIMIT 1
    """))[0])

    return jsonify({
        "mutual": recc_mutual,
        "interests": recc_interests,
        "git": recc_git,
    })

if __name__ == "__main__":
    # app.run()
    find_mutuals()

