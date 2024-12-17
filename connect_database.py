import json

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster


def criar_session():
    cloud_config = {"secure_connect_bundle": "secure-connect-xmercury.zip"}

    with open("xmercury-token.json") as f:
        secrets = json.load(f)

    CLIENT_ID = secrets["clientId"]
    CLIENT_SECRET = secrets["secret"]
    KEYSPACE = "xmercury"

    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    return session
