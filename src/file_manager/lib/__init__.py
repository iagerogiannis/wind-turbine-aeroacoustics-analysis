import os
import shutil


def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def write_file(filename, data_):
    with open(filename, 'w') as f_:
        f_.write(str(data_))


def read_value_from_file(directory_, filename):
    f_ = open("{}\\{}".format(directory_, filename), "r")
    return float(f_.read())
