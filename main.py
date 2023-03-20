from argparse import ArgumentParser
import app

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)

    args = parser.parse_args()
    path = args.input

    app.run(path)
