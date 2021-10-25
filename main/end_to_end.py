import h5py
from dlgo.agent.naive import RandomBot
from dlgo.agent.predict import load_prediction_agent
from dlgo.httpfrontend import get_web_app

from dlgo.networks import large
from dlgo.encoders.sevenplane import SevenPlaneEncoder
from dlgo.agent.predict import DeepLearningAgent
from keras.models import Sequential
from keras.layers import Dense
from dlgo.data.processor import GoDataProcessor
import tensorflow as tf


def main(graph):
    # 训练模型生成模型
    go_board_rows, go_board_cols = 19, 19
    nb_classes = go_board_rows * go_board_cols
    encoder = SevenPlaneEncoder((go_board_rows, go_board_cols))
    processor = GoDataProcessor(encoder=encoder.name())

    # 加载num_samples个棋谱的特征和标签
    X, y = processor.load_go_data(num_samples=1)
    input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
    model = Sequential()
    network_layers = large.layers(input_shape)
    for layer in network_layers:
        model.add(layer)
    model.add(Dense(nb_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

    model.fit(X, y, batch_size=128, epochs=20, verbose=1)
    deep_learning_bot = DeepLearningAgent(model, encoder)
    model_file = h5py.File("../agents/deep_bot.h5", "w")
    deep_learning_bot.serialize(model_file)

    random_agent = RandomBot()
    model_file = h5py.File("../agents/deep_bot.h5", "r")


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