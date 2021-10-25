from __future__ import absolute_import
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Conv2D, ZeroPadding2D


# 围棋深度学习网络
# 七层神经网络
def layers(input_shape):
    return [
        # 填0 64个输出过滤器 卷积核为7*7
        ZeroPadding2D((3, 3), input_shape=input_shape, data_format='channels_first'),
        Conv2D(64, (7, 7), padding='valid', data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(64, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(64, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(48, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(48, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(32, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(32, (5, 5), data_format='channels_first'),
        Activation('relu'),

        Flatten(),
        Dense(1024),
        Activation('relu'),
    ]
