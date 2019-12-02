import tensorflow as tf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file")
args = parser.parse_args()

dataset = tf.data.TextLineDataset(args.file)
dataset = dataset.map(lambda x: tf.strings.to_number(tf.strings.split(x, ","), tf.int32))

n_ops = tf.constant(2)

@tf.function
def process(x):
    index = 0 #tf.Variable(0)
    up = tf.constant(0)
    while index < tf.size(x):
        if x[index] == 99:
            break
        operands = tf.gather(x, x[index+1:index+1+n_ops])
        if x[index] == 1:
            up = tf.reduce_sum(operands)
        elif x[index] == 2:
            up = tf.reduce_prod(operands)
        x = tf.tensor_scatter_nd_update(x, [x[index+3:index+1+3]], [up])
        index = tf.add(index, 4)
    return x

for d in dataset:
    # fix according to assigment
    for noun in tf.range(100):
        for verb in tf.range(100):
            updated_d =  tf.tensor_scatter_nd_update(d, tf.constant([[1], [2]]), [noun, verb])
            if process(updated_d)[0].numpy() == 19690720:
                print(noun, verb)
                print(tf.add(tf.multiply(100, noun), verb).numpy())