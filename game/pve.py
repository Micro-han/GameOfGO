import h5py
from dlgo.agent.naive import RandomBot
from dlgo.agent.predict import load_prediction_agent
from dlgo.httpfrontend import get_web_app
import tensorflow as tf
import webbrowser


def runitapp(graph):
    model_file = h5py.File("./agents/betago.hdf5", "r")
    bot_from_file = load_prediction_agent(model_file)
    web_app = get_web_app({'predict': bot_from_file}, graph)
    webbrowser.open("http://127.0.0.1:5000/static/play_predict_19.html")
    web_app.run()


global graph
if __name__ == '__main__':
    graph = tf.get_default_graph()
    runitapp(graph)