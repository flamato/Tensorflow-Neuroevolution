import tensorflow as tf
from absl import logging
from collections import deque

import neuroevolution as ne


def test_direct_encoding():
    logging.set_verbosity(logging.DEBUG)
    logging.info("Using TF Version {}".format(tf.__version__))
    assert tf.__version__[0] == '2'  # Assert that TF 2.x is used

    config = ne.load_config('./test_config.cfg')

    encoding = ne.encodings.DirectEncoding(config)

    activation_default = tf.keras.activations.deserialize("tanh")
    activation_out = tf.keras.activations.deserialize("sigmoid")

    genotype = deque([
        encoding.create_gene_connection(1, 4),
        encoding.create_gene_connection(1, 5),
        encoding.create_gene_connection(2, 6),
        encoding.create_gene_connection(3, 4),
        encoding.create_gene_connection(3, 5),
        encoding.create_gene_connection(4, 6),
        encoding.create_gene_connection(5, 6),
        encoding.create_gene_node(4, activation_default),
        encoding.create_gene_node(5, activation_default),
        encoding.create_gene_node(6, activation_out)
    ])

    encoding.create_genome(genotype, trainable=False)


if __name__ == '__main__':
    test_direct_encoding()
