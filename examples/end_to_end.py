import h5py
import os
from dlgo.agent.naive import RandomBot
from dlgo.agent.predict import load_prediction_agent
from dlgo.httpfrontend import get_web_app

# 生成模型
# go_board_rows, go_board_cols = 19, 19
# nb_classes = go_board_rows * go_board_cols
# encoder = SevenPlaneEncoder((go_board_rows, go_board_cols))
# processor = GoDataProcessor(encoder=encoder.name())
#
# X, y = processor.load_go_data(num_samples=100)
# input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
# model = Sequential()
# network_layers = large.layers(input_shape)
# for layer in network_layers:
#     model.add(layer)
# model.add(Dense(nb_classes, activation='softmax'))
# model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
#
# model.fit(X, y, batch_size=128, epochs=20, verbose=1)
# deep_learning_bot = DeepLearningAgent(model, encoder)
# deep_learning_bot.serialize("../agents/deep_bot.h5")

random_agent = RandomBot()
file_name = os.path.dirname(__file__)
model_file = h5py.File(file_name + "/small_model_epoch_5.h5", "r")
bot_from_file = None

try:
    bot_from_file = load_prediction_agent(model_file)
    web_app = get_web_app({'predict': bot_from_file})
except Exception as ee:
    print("ee" + str(ee))
    web_app = get_web_app({'predict': random_agent})

web_app.run()