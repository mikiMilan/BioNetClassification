import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Lambda
from tensorflow.keras.models import Model
from tensorflow.keras.losses import mse
from tensorflow.keras import backend as K
import numpy as np

# Učitavanje podataka
(x_train, _), (x_test, _) = ...

# Normalizacija i pretvaranje podataka u float32 format
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

# Definicija parametara modela
input_shape = (28, 28, 1)
latent_dim = 2  # Dimenzija latentnog prostora

# Definicija VAE arhitekture
inputs = Input(shape=input_shape)
x = tf.keras.layers.Conv2D(32, 3, activation='relu', strides=2, padding='same')(inputs)
x = tf.keras.layers.Conv2D(64, 3, activation='relu', strides=2, padding='same')(x)
x = tf.keras.layers.Flatten()(x)
x = tf.keras.layers.Dense(16, activation='relu')(x)

# Parametri latentnog prostora
z_mean = Dense(latent_dim)(x)
z_log_var = Dense(latent_dim)(x)

# Funkcija za uzorkovanje iz latentnog prostora
def sampling(args):
    z_mean, z_log_var = args
    epsilon = K.random_normal(shape=(K.shape(z_mean)[0], latent_dim))
    return z_mean + K.exp(0.5 * z_log_var) * epsilon

# Uzorkovanje iz latentnog prostora
z = Lambda(sampling)([z_mean, z_log_var])

# Decoder model
decoder_input = Input(K.int_shape(z)[1:])
x = Dense(7 * 7 * 64, activation='relu')(decoder_input)
x = tf.keras.layers.Reshape((7, 7, 64))(x)
x = tf.keras.layers.Conv2DTranspose(64, 3, activation='relu', strides=2, padding='same')(x)
x = tf.keras.layers.Conv2DTranspose(32, 3, activation='relu', strides=2, padding='same')(x)
outputs = tf.keras.layers.Conv2DTranspose(1, 3, activation='sigmoid', padding='same')(x)

# Definicija decoder modela
decoder = Model(decoder_input, outputs)

# Definicija VAE modela
outputs = decoder(z)
vae = Model(inputs, outputs)

# Definicija VAE loss funkcije
reconstruction_loss = mse(K.flatten(inputs), K.flatten(outputs))
reconstruction_loss *= input_shape[0] * input_shape[1]
kl_loss = 1 + z_log_var - K.square(z_mean) - K.exp(z_log_var)
kl_loss = K.sum(kl_loss, axis=-1)
kl_loss *= -0.5
vae_loss = K.mean(reconstruction_loss + kl_loss)
vae.add_loss(vae_loss)

# Kompilacija modela
vae.compile(optimizer='adam')

# Treniranje modela
vae.fit(x_train, epochs=10, batch_size=128, validation_data=(x_test, None))
