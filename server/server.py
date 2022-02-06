import json
import connection_suggestions
import keyword_extraction
import sql_database
import sql_data_transforms
import slack_extract
import pickle
import github_similarity
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

last_pull_time = 0

@app.route("/home")
def hello_world():
    return "ok!"


@app.route("/pull_messages")
def pull_messages():
    global last_pull_time
    last_pull_time, updates = slack_extract.upload_conversations(last_pull_time)
    
    for [time, sender, receiver, body, keywords] in updates:
        s = f"""
            INSERT INTO message(sent, sender, receiver, content, keywords)
            VALUES (
                {time},
                (SELECT rowid FROM user WHERE slack = "{sender}"),
                (SELECT rowid FROM user WHERE slack = "{receiver}"),
                "{body}",
                ?
            )
        """

        sql_database.db.execute(s, [pickle.dumps(keywords)])
        sql_database.db.commit()

    return jsonify("success")

# recc_mutual
@app.route("/find_mutuals")
def find_mutuals():
    # read data from DB
    messages = sql_database.get_messages()

    # construct connections graph
    connection_graph = sql_data_transforms.create_connections_graph(messages)

    # run mutual finder algorithm
    uids = set([m[3] for m in messages])
    for uid in uids:
        # mutuals is a dictionary of k: v -> second_degree_connection_uid: [mutual_connection_uid]
        suggs, mutuals = connection_suggestions.get_mutuals(uid, connection_graph)
        # update db
        for tid, certainty in suggs.items():
            print(mutuals[tid], mutuals, tid)
            sql_database.db.execute(f"""
                INSERT INTO recc_mutual(user, target, certainty, con)
                VALUES ({uid}, {tid}, {certainty}, ?)
            """, [pickle.dumps(mutuals[tid])])
            sql_database.db.commit()
    
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
        # matched keywords is a dictionary of the form
        # k: v -> connection_uid: [matched_keywords]
        suggs, matched_keywords = connection_suggestions.get_similar_interest(uid, ranked_keywords)
        for tid, certainty in suggs.items():
            print(matched_keywords, tid)
            sql_database.db.execute(f"""
                INSERT INTO recc_interests(user, target, certainty)
                VALUES ({uid}, {tid}, {certainty}, ?)
            """, [pickle.dumps(matched_keywords[tid])])
            sql_database.db.commit()
    
    return jsonify({
        "success": True
    })

# recc_git
@app.route("/find_git_friends")
def find_git_friends():
    # load all github IDs
    github_ids = [a["github"] for a in sql_database.db.execute(f"""
        SELECT github FROM user
    """)]

    for gid1 in github_ids:
        for gid2 in github_ids:
            if gid1 != gid2:
                (languages, certainty) = github_similarity.similarity(gid1, gid2)
                sql_database.db.execute(f"""
                    INSERT INTO recc_git(user, target, certainty, con)
                    VALUES (
                        (SELECT rowid FROM user WHERE github = "{gid1}"),
                        (SELECT rowid FROM user WHERE github = "{gid2}"),
                        {certainty},
                        ?
                    )
                """, [pickle.dumps(languages)])
                sql_database.db.commit()
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
    uid = int(request.args.get("uid"))
    print("HELLO")
    recc_mutual = dict(list(sql_database.db.execute(f"""
        SELECT user.name, user.title, user.github, user.icon, recc_mutual.con
        FROM recc_mutual
        JOIN user ON user.rowid = user
        WHERE user = {uid}
        ORDER BY certainty DESC
        LIMIT 1
    """))[0])
    recc_mutual["con"] = [
        dict(list(sql_database.db.execute(f"SELECT name FROM user WHERE rowid = {a}"))[0])["name"]
        for a in pickle.loads(recc_mutual["con"])
    ]

    # recc_interests = dict(list(sql_database.db.execute(f"""
    #     SELECT user.name, user.title, user.github, user.icon, recc_interests.con
    #     FROM recc_interests
    #     JOIN user ON user.rowid = user
    #     WHERE user = {uid}
    #     ORDER BY certainty DESC
    #     LIMIT 1
    # """))[0])

    recc_git = dict(list(sql_database.db.execute(f"""
        SELECT user.name, user.title, user.github, user.icon, recc_git.con
        FROM recc_git
        JOIN user ON user.rowid = user
        WHERE user = {uid}
        ORDER BY certainty DESC
        LIMIT 1
    """))[0])
    recc_git["con"] = pickle.loads(recc_git["con"])

    print(recc_mutual, recc_git)

    return jsonify({
        "mutuals": recc_mutual,
        # "interests": recc_interests,
        "git": recc_git,
    })

if __name__ == "__main__":
    app.run(processes=1, threaded=False)

