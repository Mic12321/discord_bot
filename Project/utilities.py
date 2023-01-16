import os



def extension_exists(extension_name):
    for Filename in os.listdir("./extensions"):
        if ((Filename.endswith(".py")) and (Filename[:-3]==extension_name)):
            return True

    return False


def data_exists(file_name, target_a):

    target=str(target_a)
    file=open(file_name, "r")
    content = file.readlines()
    file.close()
    for line_content in content:
        if(line_content[-1] == '\n'):
            line_content = line_content[:-1]

        if (line_content == target):
            return True
        
    return False


def append_content(file_name, content):
    file=open(file_name, "a")
    file.write(f"\n{content}")
    file.close()

def write_content(file_name, content):
    file=open(file_name, "w")
    file.write(content)
    file.close()


def remove_content(file_name, target):
    file=open(file_name, "r")

    content=file.readlines()

    count=0
    file_w=open(file_name, "w")
    for index, line_content in enumerate(content):
        if(line_content[-1] == '\n'):
            line_content = line_content[:-1]

        if (line_content != target):
            if (count!=0):
                file_w.write("\n")
            file_w.write(f"{line_content}")
            count+=1

    file.close()