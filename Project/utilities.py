import os

def is_bot_admin(check_id):
    file=open("admin.txt", "r")
    content = file.readlines()
    file.close()
    for line_content in content:
        if (line_content==str(check_id)):
            return True
        
    return False


def extension_exists(extension_name):
    for Filename in os.listdir("./extensions"):
        if ((Filename.endswith(".py")) and (Filename[:-3]==extension_name)):
            return True

    return False