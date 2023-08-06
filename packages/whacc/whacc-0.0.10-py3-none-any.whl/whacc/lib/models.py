import tensorflow as tf
from tensorflow import keras
from whacc.config import config


def scratch_model():
    """
    Create base model

    First, instantiate a MobileNet V2 model pre-loaded with weights trained on ImageNet. By specifying the include_top=False argument,
    you load a network that doesn't include the classification layers at the top, which is ideal for feature extraction

    Create the base model from the pre-trained model MobileNet V2
    """

    IMG_SIZE = 96  # All images will be resized to 96x96. This is the size of MobileNetV2 input sizes
    IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)

    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights='imagenet')

    base_model.trainable = False

    feature_batch = base_model.output
    print(feature_batch.shape)

    # Adding Classification head
    global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
    feature_batch_average = global_average_layer(feature_batch)
    print(feature_batch_average.shape)

    prediction_layer = tf.keras.layers.Dense(1, activation='sigmoid')
    prediction_batch = prediction_layer(feature_batch_average)
    print(prediction_batch.shape)

    # Model Stacking
    model = tf.keras.Sequential([
        base_model,
        global_average_layer,
        prediction_layer
    ])

    print(model.summary())

    # Compile model with specific metrics
    # Metrics below are for evaluating imbalanced datasets
    METRICS = [
        keras.metrics.TruePositives(name='tp'),
        keras.metrics.FalsePositives(name='fp'),
        keras.metrics.TrueNegatives(name='tn'),
        keras.metrics.FalseNegatives(name='fn'),
        keras.metrics.Precision(name='precision'),
        keras.metrics.Recall(name='recall'),
        keras.metrics.AUC(name='auc')
    ]

    base_learning_rate = 0.0001
    model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=base_learning_rate),
                  loss=tf.keras.losses.BinaryCrossentropy(),
                  metrics=METRICS)

    return model


def load_model():
    file_folder = 'model_v1.h5'
    model = tf.keras.models.load_model(config.TRAINED_MODEL_DIR / file_folder)
    return model


def load_model_checkpoint():
    model = scratch_model()

    model_checkpoints = config.TRAINED_MODEL_DIR
    latest = tf.train.latest_checkpoint(model_checkpoints)
    print(latest)
    model.load_weights(latest)

    return model
