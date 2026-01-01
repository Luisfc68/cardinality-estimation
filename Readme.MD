# Randomized Algorithms Assignment #3
## Participants
* Luis Fernando Chavez Quevedo
* Antonio Peso Vilella

## Instructions to execute the experiment
You can do 3 things with this project; generate a vocabulary for a synthetic stream, generate a synthetic stream using a
specific vocabulary, or estimate the cardinality of a stream using the different estimators included in the project. In
any case, the requirements are the following:
* Python >= 3.14.0
* pip >= 25.1.1

The following estimators are included:
* Hyper log log (with and without corrections)
* Recordinality

The common steps to run any of the three scenarios are the following:
1. Clone the project: `https://github.com/Luisfc68/cardinality-estimation.git`
2. Go inside the project: `cd cardinality-estimation`
3. Install the project: `pip3 install -e .`

### Generating a vocabulary
The purpose of this functionality is to generate the vocabulary that will be used as an input to generate the synthetic datastreams.
The command to be executed is 
```
python3 stream_generator.py --mode=vocabulary
```
The `stream_generator.py` file is used for the generation of both the stream and the vocabulary so that's why we need to specify the mode.
Inside the `stream_generator.py`, the following variables need to be modified as needed:
* `STREAM_DIR`: existing directory where the vocabulary file will be placed.
* `VOCABULARY_FILE`: the file to write the vocabulary. Should be inside `STREAM_DIR`.
* `VOCABULARY_SIZE`: the size of the vocabulary (number of distinct elements).

In this implementation the vocabulary consist in random numbers, however, this can be changed by words if needed.
Also, the format of the output file consist in one element per line. So the number of lines matches with the value provided in `VOCABULARY_SIZE`.

### Generating a synthetic stream
This functionality is used to create additional datasets besides the ones provided by default. The output file also consists of one element per line.
An existing vocabulary file is required in order to generate the synthetic stream. The stream is generated using a Zipfian distribution,
where the probability of each vocabulary element depends on its position (rank) in the vocabulary file.

The following variables should be configured as needed in the `stream_generator.py` file:
* `STREAM_DIR`: existing directory where the stream file will be placed.
* `VOCABULARY_FILE`: the existing input file to read the vocabulary. Should be inside `STREAM_DIR`.
* `STREAM_FILE`: the output file to write the stream. Should be inside `STREAM_DIR`.
* `STREAM_SIZE`: the size of the stream.
* `ALPHA`: the Zipfian distribution exponent, which controls the skewness of the probability distribution.

### Estimating set cardinality
This is the main functionality of this project. It consists on estimating the cardinality of the requested datasets with all the
estimators configured. The way it works is the following: in the `main.py` script there are two important variables; the first one is
the **datasets** array, and the second one is the **estimators** array. The datasets array consist on the **names without the extension** of
the datasets to estimate, these datasets should meet some assumptions:
1. The dataset exists in the `DATASET_DIR` directory.
2. There are two files in the `DATASET_DIR` for each dataset, <dataset>.txt with the dataset itself and <dataset>.dat 
with the vocabulary of the dataset. The reason for this is that <dataset>.txt will be used to estimate and <dataset>.dat
will be used to compare the estimation against the actual cardinality.
3. Both files should have one element per line (doesn't matter if the line has information about the element, like in some cases of the
vocabularies where the number of repetitions is also in the line).

Regarding the estimators array, it is an array of `Estimator` class instances, it can be configured any number of estimators with any
number of configurations, the only requirement is to have one instance per configuration. The values required to create one instance are
a name for the estimator and an estimation function (any of the ones listed at the beginning of this file).

There are some other configurations at the beginning of the `main.py` file like `ITERATIONS` to set the iterations to run per estimator
(the presented results will be the average of these iterations) or the particular configurations of each estimator.
The command to run the estimators is:
```
python main.py
```