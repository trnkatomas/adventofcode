import tensorflow as tf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file")
args = parser.parse_args()

dataset = tf.data.TextLineDataset(args.file)
dataset = dataset.map(lambda x: tf.strings.to_number(x, tf.float32))

@tf.function
def compute_fuel(x):
    fuel_mass = tf.math.subtract(tf.math.floor(tf.divide(x,3.0)), 2.0)
    fuel_mass_temp = tf.identity(fuel_mass)
    while fuel_mass_temp > 0.0:        
        fuel_mass_temp = tf.math.maximum(0.0, tf.math.subtract(tf.math.floor(tf.divide(fuel_mass_temp,3.0)), 2.0))        
        fuel_mass = tf.add(fuel_mass, fuel_mass_temp)
    return fuel_mass

print(compute_fuel(1969))

dataset_pre_line_transform_fuel_for_fuel = dataset.map(lambda x: compute_fuel(x))
print(dataset_pre_line_transform_fuel_for_fuel.reduce(0.0, lambda state, value: state + value).numpy())
