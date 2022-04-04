from io import BytesIO
import base64


def encode_plot(plt):
    print("encoding plot", flush=True)

    img = BytesIO()

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    plot_base64 = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_base64
