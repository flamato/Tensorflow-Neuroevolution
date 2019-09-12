import ast
import numpy as np
import tensorflow as tf
from absl import logging

from ..base_environment import BaseEnvironment


class XOREnvironment(BaseEnvironment):
    def __init__(self, config):
        self.x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        self.y = np.array([[0], [1], [1], [0]])

        self.loss_function = tf.keras.losses.BinaryCrossentropy()

        # Declare and read in config parameters for the XOR environment
        self.input_shape = None
        self.num_output = None
        self._read_config_parameters(config)

    def _read_config_parameters(self, config):
        section_name = 'XOR_ENVIRONMENT' if config.has_section('XOR_ENVIRONMENT') else 'ENVIRONMENT'
        self.input_shape = ast.literal_eval(config.get(section_name, 'input_shape', fallback='(2,)'))
        self.num_output = config.getint(section_name, 'num_output', fallback=1)

        logging.debug("XOR Environment read from config: input_shape = {}".format(self.input_shape))
        logging.debug("XOR Environment read from config: num_output = {}".format(self.num_output))

    def eval_genome_fitness(self, genome):
        # Calculate the genome fitness as the percentage of accuracy in its prediction, rounded to 3 decimal points
        model = genome.get_model()
        evaluated_fitness = float(100 * (1 - self.loss_function(self.y, model.predict(self.x))))
        return round(evaluated_fitness, 3)

    def replay_genome(self, genome):
        model = genome.get_model()
        logging.info("Replaying Genome {}...".format(genome.get_id()))
        logging.info("Solution Values:\n{}".format(self.y))
        logging.info("Predicted Values:\n{}".format(model.predict(self.x)))

    def get_input_shape(self):
        return self.input_shape

    def get_num_output(self):
        return self.num_output
