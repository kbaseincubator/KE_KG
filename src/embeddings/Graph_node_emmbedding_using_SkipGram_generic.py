#!/usr/bin/env python

#import silence_tensorflow.auto
import tensorflow as tf
import sys
import numpy as np

from ensmallen_graph import EnsmallenGraph
from embiggen import Node2VecSequence

if len(sys.argv) < 3:
   sys.exit()
edge_file = sys.argv[1]
node_file = sys.argv[2]
out_name = sys.argv[3]

graph = EnsmallenGraph.from_unsorted_csv(
    edge_path=edge_file,
    node_path=node_file,
    sources_column="subject",
    destinations_column="object",
    nodes_column = 'id',
    #node_types_column = 'category',
    #default_node_type = 'biolink:NamedThing',
    directed=False
    #weights_column="weight"
)

#print(graph.report())
print(graph)


walk_length=100
batch_size=2**8
iterations=20
window_size=4
p=1.0
q=1.0
embedding_size=100
negative_samples=30
patience=5
delta=0.0001
epochs=100
learning_rate=0.1



graph_sequence = Node2VecSequence(
    graph,
    walk_length=walk_length,
    batch_size=batch_size,
    iterations=iterations,
    window_size=window_size,
    return_weight=1/p,
    explore_weight=1/q,
    support_mirror_strategy=True
)

#CREATING
from tensorflow.distribute import MirroredStrategy
from tensorflow.keras.optimizers import Nadam
from embiggen import SkipGram

strategy = MirroredStrategy()
with strategy.scope():
    model = SkipGram(
       vocabulary_size=graph.get_nodes_number(),
       embedding_size=embedding_size,
       window_size=window_size,
       negative_samples=negative_samples,
       optimizer=Nadam(learning_rate=learning_rate)
    )

print(model.summary())

#TUNING
from tensorflow.keras.callbacks import EarlyStopping

print("GPU")
print(tf.test.gpu_device_name())
history = model.fit(
    graph_sequence,
    steps_per_epoch=graph_sequence.steps_per_epoch,
    epochs=epochs,
    callbacks=[
        EarlyStopping(
            monitor="loss",
            min_delta=delta,
            patience=patience,
            restore_best_weights=True
        )
    ]
)

#SAVE
model.save_weights(f"{model.name}_{out_name}_weights.h5")


np.save(f"{model.name}_{out_name}_embedding.npy", model.embedding)


#from plot_keras_history import plot_history

#plot_history(history)
