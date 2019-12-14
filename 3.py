import tensorflow as tf
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--file")
parser.add_argument("--debug", action='store_true')
args = parser.parse_args()

dataset = tf.data.TextLineDataset(args.file)
dataset = dataset.map(lambda x: tf.strings.split(x, ","))
dataset = dataset.map(lambda x: [tf.strings.substr(x, 0, 1), tf.cast(tf.strings.to_number(tf.strings.substr(x, 1, tf.strings.length(x)[0])),tf.int32)])

@tf.function
def draw(wiring_map_orig, directions, amount, current_pos_x=None, current_pos_y=None):
    wiring_map = tf.identity(wiring_map_orig)
    index = 0    
    cumsum = 1
    if current_pos_x is None:
        current_pos_x = tf.cast(tf.floor(tf.divide(tf.shape(wiring_map)[0], 2)), tf.int32)
    if current_pos_y is None:
        current_pos_y = tf.identity(current_pos_x)
    end_pos_x = tf.identity(current_pos_x)
    end_pos_y = tf.identity(current_pos_y)    
    while index < tf.size(directions):   
        update_indices = tf.constant(0)     
        if args.debug:
            print(directions[index], amount[index])
        if directions[index] == 'R':
            end_pos_x = tf.add(current_pos_x, amount[index])
            update_indices = tf.stack([tf.range(current_pos_x, end_pos_x), tf.multiply(tf.cast(tf.ones(amount[index]), tf.int32), current_pos_y)], axis=1)
        elif directions[index] == 'L':
            end_pos_x = tf.subtract(current_pos_x, amount[index])
            update_indices = tf.stack([tf.range(current_pos_x, end_pos_x, delta=-1), tf.multiply(tf.cast(tf.ones(amount[index]), tf.int32), current_pos_y)], axis=1)
        elif directions[index] == 'U':
            end_pos_y = tf.subtract(current_pos_y, amount[index])
            update_indices = tf.stack([tf.multiply(tf.cast(tf.ones(amount[index]), tf.int32), current_pos_x), tf.range(current_pos_y, end_pos_y, delta=-1)], axis=1)
        elif directions[index] == 'D':
            end_pos_y = tf.add(current_pos_y, amount[index])
            update_indices = tf.stack([tf.multiply(tf.cast(tf.ones(amount[index]), tf.int32), current_pos_x), tf.range(current_pos_y, end_pos_y)], axis=1)
        up = tf.ones(amount[index]) * tf.cast(tf.range(cumsum, cumsum+amount[index]), tf.float32)
        cumsum += amount[index]
        wiring_map = tf.tensor_scatter_nd_update(wiring_map, update_indices, up)
        current_pos_x = tf.identity(end_pos_x)
        current_pos_y = tf.identity(end_pos_y)
        index = tf.add(index, 1)
    wiring_map = tf.tensor_scatter_nd_add(wiring_map, [[current_pos_x, current_pos_y]], [cumsum])
    return wiring_map
    
max_val = 0
min_L = 0
max_R = 0
min_U = 0
max_D = 0
horizontal_size = 0
vertical_size = 0
for d, l in dataset:
    R_indices = tf.where(d=='R')
    L_indices = tf.where(d=='L')
    D_indices = tf.where(d=='D')
    U_indices = tf.where(d=='U')
    LR_updated = tf.tensor_scatter_nd_update(l, L_indices,  tf.squeeze(tf.multiply(tf.gather(l, L_indices),-1), axis=1))
    LR_updated = tf.tensor_scatter_nd_update(LR_updated, D_indices, tf.squeeze(tf.cast(tf.zeros(tf.shape((D_indices))), tf.int32), axis=1))
    LR_updated = tf.tensor_scatter_nd_update(LR_updated, U_indices, tf.squeeze(tf.cast(tf.zeros(tf.shape((U_indices))), tf.int32), axis=1))
    UD_updated = tf.tensor_scatter_nd_update(l, U_indices,  tf.squeeze(tf.multiply(tf.gather(l, U_indices),-1), axis=1))
    UD_updated = tf.tensor_scatter_nd_update(UD_updated, L_indices, tf.squeeze(tf.cast(tf.zeros(tf.shape((L_indices))), tf.int32), axis=1))
    UD_updated = tf.tensor_scatter_nd_update(UD_updated, R_indices, tf.squeeze(tf.cast(tf.zeros(tf.shape((R_indices))), tf.int32), axis=1))
    LR_updated = tf.math.cumsum(LR_updated)
    UD_updated = tf.math.cumsum(UD_updated)
    min_L_n = tf.abs(tf.minimum(0, tf.reduce_min(LR_updated)))
    max_R_n = tf.maximum(tf.reduce_max(LR_updated), 0)
    min_U_n = tf.abs(tf.minimum(0, tf.reduce_min(UD_updated)))
    max_D_n = tf.maximum(0, tf.reduce_max(UD_updated))
    max_D = tf.maximum(max_D, max_D_n)
    max_R = tf.maximum(max_R, max_R_n)    
    min_L = tf.maximum(min_L, min_L_n)
    min_U = tf.maximum(min_U, min_U_n)
    horizontal_size = tf.maximum(horizontal_size, min_L + max_R + 2)
    vertical_size = tf.maximum(vertical_size, max_D + min_U + 2)

@tf.function
def round_for_conv(s):
    return (s + 1) + tf.math.mod(s + 1, 3)

wiring_map = tf.zeros((round_for_conv(horizontal_size), round_for_conv(vertical_size)), tf.float32)

orig_wiring_map = tf.identity( wiring_map ) #tf.zeros((round_for_conv(horizontal_size), round_for_conv(vertical_size)), tf.float32)

for dt, lt in dataset:
    wiring_map_temp = draw(orig_wiring_map, dt, lt, min_L+1, min_U+1)  
    if args.debug:
        print(wiring_map_temp)
    wiring_map_crs = tf.multiply(wiring_map, -1 * wiring_map_temp)    
    wiring_map = tf.add(wiring_map, wiring_map_temp)
    wiring_map = tf.add(wiring_map, wiring_map_crs)

if args.debug:
    print(wiring_map)

shape = tf.shape(wiring_map)
if args.debug:
    print(shape, file=sys.stderr)

wiring_map = tf.tensor_scatter_nd_update(wiring_map, [[min_L+1, min_U+1]], [0])

# sadly useless :-(
#processed = tf.squeeze(tf.nn.conv2d(tf.reshape(wiring_map, [1, shape[0], shape[1], 1]),
#                                    tf.reshape(tf.constant([[0, 0.125, 0],[0.125, 0.25, 0.125],[0, 0.125, 0]]), [3,3,1,1]),
#                                    strides=[1,1], padding="SAME"))


#tf.print(tensor, output_stream=sys.stderr)
#tf.io.write_file("wiring.txt", tf.io.serialize_tensor(wiring_map))
#tf.io.write_file("processed.txt", tf.io.serialize_tensor(processed))
crossings = tf.where(wiring_map<-1)

if args.debug:
    tf.print(wiring_map, summarize=-1, output_stream=sys.stdout)
    print(crossings, file=sys.stderr)

min_distances = tf.map_fn(lambda x: tf.math.abs(x[0] - tf.cast(min_L+1, tf.int64)) + tf.math.abs(x[1] - tf.cast(min_U+1, tf.int64)), crossings)

@tf.function
def min_in_surroundings(loc, w_map):
    return tf.minimum(w_map[loc[0]-1, loc[1]] + w_map[loc[0], loc[1]+1],  w_map[loc[0]+1, loc[1]] + w_map[loc[0], loc[1]-1])

min_time_lag = tf.map_fn(lambda x: min_in_surroundings(x, wiring_map), crossings, dtype=tf.float32)

print(tf.reduce_min(min_distances).numpy(), file=sys.stderr)
print(tf.reduce_min(min_time_lag).numpy(), file=sys.stderr)