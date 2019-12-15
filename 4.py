import tensorflow as tf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file")
parser.add_argument("--debug", action='store_true')
args = parser.parse_args()

dataset = tf.data.TextLineDataset(args.file)

@tf.function
def get_bytes(x):
    l = tf.strings.length(x)
    b = tf.strings.substr(x, tf.range(l), tf.cast(tf.ones(l), tf.int32))    
    return b

dataset = dataset.map(lambda x: tf.map_fn(get_bytes, tf.strings.split(x, "-")))
#dataset = dataset.map(lambda x: tf.strings.split(x, "-"))
    
#dataset = dataset.map(lambda x: get_bytes(x))#unicode_script(x))tf.cast(tf.strings.to_number(x),tf.int32))

@tf.function
def add_one_number(num, idx, incr=1, propagate=False):
    carry = False
    if num[idx] < 9:
        num = tf.tensor_scatter_nd_add(num, [[idx]], [1])        
    else:
        num = tf.tensor_scatter_nd_update(num, [[idx]], [0])
        carry = True
    if propagate and not carry:
        indices = tf.stack([tf.range(idx+1, num.shape[0])], axis=1)
        num = tf.tensor_scatter_nd_update(num, indices, tf.ones(num.shape[0]-idx-1)*num[idx])
    return num, carry

@tf.function
def add_vector(num, incr=1):
    index = tf.shape(num)[0]-1
    num2, carry = add_one_number(num, index, incr)
    index = index - 1  
    while index >= 0 and carry:
        num2, carry = add_one_number(num2, index, incr, propagate=True)
        index = index - 1
    return num2

@tf.function
def two_same(number):
    proc = tf.squeeze(tf.nn.conv1d(tf.reshape(number, [1, number.shape[0], 1]),
                            tf.reshape(tf.constant([0.5, 0.5]), [2,1,1]),
                            1, "VALID"))
    return tf.reduce_any(tf.math.equal(number[:-1], proc))

@tf.function
def exactly_two_same(number):
    y, idx, cnts = tf.unique_with_counts(number)
    return tf.reduce_any(cnts==2)

@tf.function
def verify_number(num, end):
    radixes = tf.map_fn(lambda x: tf.math.pow(10.0, x), tf.cast(tf.range(num.shape[0]-1, -1, delta=-1), tf.float32))
    valid_numbers_part_1 = 0
    valid_numbers_part_2 = 0
    while tf.tensordot(num, radixes, 1) < tf.tensordot(end, radixes, 1):
        decr = tf.math.is_non_decreasing(num)
        if not decr:
            num = add_vector(num)
            continue
        two_same_numbers = two_same(num)
        if not two_same_numbers:
            num = add_vector(num)
            continue
        valid_numbers_part_1 += 1
        ex_two_same = exactly_two_same(num)
        if not ex_two_same:
            num = add_vector(num)
            continue
        valid_numbers_part_2 += 1
        #print(tf.tensordot(num, radixes, 1))
        num = add_vector(num)
    return valid_numbers_part_1, valid_numbers_part_2    

for d in dataset:
    start = d[0]
    end = d[1]
    #print(start, end)
    start_whole = tf.strings.to_number(start, out_type=tf.float32)
    end_whole = tf.strings.to_number(end, out_type=tf.float32)
    #print(start_whole)
    res, res2 = verify_number(start_whole, end_whole)
    print(res.numpy())
    print(res2.numpy())