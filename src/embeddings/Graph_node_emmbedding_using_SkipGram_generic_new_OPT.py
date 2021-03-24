import silence_tensorflow.auto

from ensmallen_graph import EnsmallenGraph
import sys

from embiggen import Node2VecSequence

import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.distribute import MirroredStrategy
from tensorflow.keras.optimizers import Nadam
from embiggen import SkipGram

import pandas as pd
import numpy as np

if len(sys.argv) < 3:
   sys.exit()
edge_file = sys.argv[1]
node_file = sys.argv[2]
out_prefix = sys.argv[3]


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

degrees = graph.degrees()
np.savetxt(f"{out_prefix}_degrees.tsv", degrees, delimiter="\t", fmt="%i")
nodes = graph.get_node_names()
np.savetxt(f"{out_prefix}_nodes.tsv", nodes, delimiter="\t", fmt="%s")


walk_length=30
batch_size=2**8
iterations=200
window_size=10
p=1.0
q=1.0
embedding_size=64
negative_samples=60
patience=5
delta=0.0001
epochs=1000
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
model.save_weights(f"{model.name}_weights_{out_prefix}.h5")

embeddings = pd.DataFrame(model.embedding, index=graph.get_node_names())
embeddings.to_csv(f"{model.name}_embedding_{out_prefix}.npy", header=True)

nodes = graph.get_node_names()
np.savetxt(f"{out_prefix}_nodes_after.tsv", nodes, delimiter="\t", fmt="%s")
