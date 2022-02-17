import os

def savefig(plt, uuid, filename):
    """Take a matplotlib plot and save it to the project's /plots directory."""

    dir = os.getenv('ROOT')

    plt.savefig(f'{dir}/static/{uuid}/plots/{filename}.png')

    return

def savecsv(df, uuid, filename):
    """Take a dataframe and save it to the project's /csv directory."""

    dir = os.getenv('ROOT')

    df.to_csv(f'{dir}/static/{uuid}/csv/{filename}.csv')

    return