import tensorflow as tf


class DQNCore:
    def __init__(self, learning_rate, discount):
        self.discount = discount

        self.__input_count = 26
        self.__output_count = 49

        self.__define_model()
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                           loss=tf.losses.Huber(),
                           metrics=[tf.metrics.Accuracy()])
        self.model.summary()

    def __define_model(self):
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(units=32,
                                  activation=tf.keras.activations.relu,
                                  kernel_initializer=tf.keras.initializers.he_normal(),
                                  input_shape=(self.__input_count,)),
            tf.keras.layers.Dense(units=40,
                                  activation=tf.keras.activations.relu,
                                  kernel_initializer=tf.keras.initializers.he_normal()),
            tf.keras.layers.Dense(units=self.__output_count)
        ])

    def get_input_size(self):
        return self.__input_count

    def get_output_size(self):
        return self.__output_count

    def get_q_values(self, state):
        return self.model.predict(x=[state], batch_size=1)[0].tolist()

    def train(self, state, q_values):
        self.model.fit(x=[state, ], y=[q_values, ], epochs=1)

# todo: old_state_q_values[action] = reward + self.discount * np.amax(new_state_q_values)


class DQN:
    __network = DQNCore(learning_rate=0.01, discount=0.95)

    @staticmethod
    def get_q_values(state):
        return DQN.__network.get_q_values(state)

    @staticmethod
    def train(state, q_values):
        DQN.__network.train(state, q_values)

    @staticmethod
    def get_state_regular_len():
        return DQN.__network.get_input_size()

    @staticmethod
    def get_q_values_list_regular_len():
        return DQN.__network.get_output_size()
