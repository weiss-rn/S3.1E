import os
class fungsi:
    @staticmethod
    def create_directory(directory):
        if not os.path.exists(directory):
            os.mkdir(directory)

    @staticmethod
    def write_to_file(path, data):
        with open(path,'a', encoding='utf-8') as file:
            file.write(data + '\n')

    @staticmethod
    def read_data(path, limit):
        with open(path,'rt', encoding='utf-8') as file:
            count = 0
            for line in file:
                if count == limit:
                    break
                if line == "\n":
                    continue
                else:
                    count += 1
                    print(line.replace("\n",""))
                    

    @staticmethod
    def does_file_exist(path):
        return os.path.isfile(path)

    @staticmethod
    def remove_file(path):
        if fungsi.does_file_exist(path):
            os.remove(path)
        else:
            print("file tidak ada")