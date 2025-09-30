import os 

def create_directory(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Directory '{folder_name}' created successfully.")
    else:
        print(f"Directory '{folder_name}' already exists.")

create_directory("Scraping")

# Buat
def create_new_file(path):
    f = open(path, "w")
    f.write("")
    f.close()

create_new_file("new_file.txt")

#Isi
def write_to_file(path, data):
    with open(path, "a") as f:
        f.write(data)

write_to_file("new_file.txt", "\nHello, Sekai!")

# Baca
def read_file(path):
    with open(path, "r") as f:
        for line in f.readlines():
            print(line)
        # print(f.read())

read_file("new_file.txt")

#File ada/tdk
def does_file_exist(path):
    return os.path.exists(path)

print(does_file_exist("new_file.txt"))

#Hapus Isi
def clean_file(path):
    with open(path, "w") as f:
        f.write("")

clean_file("new_file.txt")

#Hapus file
def delete_file(path):
    os.remove(path)

delete_file("new_file.txt")
