import os
import argparse
import sys
sys.path.insert(0, "utils")

import Const

def main():
    parser = argparse.ArgumentParser(description='Build training set.')

    parser.add_argument('-m', dest='maxsize', action="store_true", help='Build training set to max size.')
    parser.add_argument('--debug', action="store_true", help='Debug mode, show additional information')

    args = parser.parse_args()

    print("Build to max size: ", args.maxsize)

    with open(Const.TEST_LIST_FILE_PATH, 'w+') as train_file:
        print("Does training set exist: ", os.path.exists(Const.TRAINING_DATA_PATH))
        sample_list = []

        cnt = 0

        for x in os.walk(Const.TRAINING_DATA_PATH, topdown=False):
            if not args.maxsize and cnt == Const.TRAINING_DATA_MAX_SIZE:
                break

            sample = x[0].replace(Const.TRAINING_DATA_PATH + '/', '')
            
            if args.debug:
                print(sample)

            sample_list.append(sample)

            cnt += 1

        train_file.write('\n'.join(sample_list))
        print(f"Training set size: {cnt}")


if __name__ == '__main__':
    main()
