import matplotlib.pyplot as plt


def createPlot(title, label, save_dir, x, y):
    plt.plot(x)
    plt.plot(y)
    plt.title(title)
    plt.xlabel('epoch')
    plt.ylabel(label)
    plt.legend(['test', 'train'], loc='upper left')
    plt.savefig('{}/{}.png'.format(save_dir, title.replace(' ', '_')))
    plt.clf()
