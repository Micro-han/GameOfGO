import h5py
from dlgo.agent.naive import RandomBot
from dlgo.agent.predict import load_prediction_agent
from dlgo.httpfrontend import get_web_app

import tensorflow as tf


def main(graph):
    random_agent = RandomBot()
    model_file = h5py.File("../agents/betago.hdf5", "r")


    try:
        bot_from_file = load_prediction_agent(model_file)
        web_app = get_web_app({'predict': bot_from_file}, graph)
    except Exception as e:
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeee:" + str(e))
        web_app = get_web_app({'predict': random_agent})

    web_app.run()


global graph
if __name__ == '__main__':
    graph = tf.get_default_graph()
    main(graph)