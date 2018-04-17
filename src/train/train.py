import keras


def start(model, data, batch_size, epochs):
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])
    history = model.fit(data.train.images, data.train.labels,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_data=(data.valid.images, data.valid.labels))

    score = model.evaluate(data.valid.images, data.valid.labels, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    print('Score: ', score)

    return model, history, score
