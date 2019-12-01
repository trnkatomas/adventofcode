import tensorflow as tf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file")
args = parser.parse_args()

dataset = tf.data.TextLineDataset(args.file)
dataset = dataset.map(lambda x: tf.strings.to_number(x, tf.float32))

dataset_pre_line_transform = dataset.map(lambda x: tf.math.subtract(tf.math.floor(tf.divide(x,3.0)), 2.0))

print(dataset_pre_line_transform.reduce(0.0, lambda state, value: state + value).numpy())
