import silence_tensorflow.auto

from ensmallen_graph import EnsmallenGraph

graph = EnsmallenGraph.from_unsorted_csv(
    edge_path="/global/scratch/marcin/N2V/embiggen/notebooks/IMGVR/IMGVR_sample_KGX_edges.tsv",
    node_path="/global/scratch/marcin/N2V/embiggen/notebooks/IMGVR/IMGVR_sample_KGX_nodes.tsv",
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
print(degrees)
file1 = open("IMGVR_sample_ensmallen_degrees.txt","a") 
np.save(file1, degrees)
file1.close() 

nodes = graph.nodes()
file2 = open("IMGVR_sample_ensmallen_nodes.txt","a") 
file2.write(nodes)
file2.close() 


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
epochs=1000
learning_rate=0.1


from embiggen import Node2VecSequence

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
model.save_weights(f"{model.name}_weights_IMGVR_sample.h5")

import numpy as np

np.save(f"{model.name}_embedding_IMGVR_sample.npy", model.embedding)


#from plot_keras_history import plot_history

#plot_history(history)
