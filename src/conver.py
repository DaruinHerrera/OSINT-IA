import tensorflow as tf
import numpy as np

# Cargar el modelo guardado
modelo = tf.keras.models.load_model("./models/modelo_conversion_celsius_a_fahrenheit.h5")

# Realizar una predicción

# import matplotlib.pyplot as plt
# plt.xlabel("# Epoca")
# plt.ylabel("Magnitud de pérdida")
# plt.plot(historial.history["loss"])

print("Hagamos una predicción!")
resultado = modelo.predict(np.array([10]))
print("El resultado es " + str(resultado) + " fahrenheit!")

# print("Variables internas del modelo")
# #print(capa.get_weights())
# print(oculta1.get_weights())
# print(oculta2.get_weights())
# print(salida.get_weights())