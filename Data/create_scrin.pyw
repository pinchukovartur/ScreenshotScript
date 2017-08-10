
try:
    import time
    import os
    import datetime
    import PIL.ImageGrab  # install lib
    import pycron  # install lib
    import xml.etree.ElementTree as ET
    import sys
    from requests import post  # install lib
    import subprocess
    import tempfile


    def run_screenshot_script():
        # get temp folder
        dirpath = tempfile.gettempdir()
        dirpath = dirpath + "/SCREENSHOTMONITOR/"
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        # check config file
        f_start = open(dirpath + "f_start.txt", "a")
        f_start.write(str(os.path.abspath(__file__).replace("\create_scrin.pyw","")) + "\config.xml")
        f_start.write("start work\n")
        f_start.write("time start work - " + str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + "\n")
        f_start.write("PID - ")
        f_start.write(str(os.getpid()) + "\n")
        if os.path.isfile(str(os.path.abspath(__file__).replace("\create_scrin.pyw","")) + "\config.xml") is False:
            f_start.write("config not found\n")
            time.sleep(5)
            exit(1)

        # get config parameters
        set_parameters = get_config()
        if len(set_parameters) == 0:
            f_start.write("config empty\n")
            exit(1)

        f_start.write("wait cron time...\n")
        f_start.close()

        while True:
            if pycron.is_now(set_parameters["cron"]):
                # create screenshot file
                f_work = open(dirpath + "f_work.txt", "a")
                f_work.write("\ncreate screen\n")
                img = PIL.ImageGrab.grab()
                img.save(dirpath + "tmp.jpg")
                img.close()

                if os.path.isfile(dirpath + "tmp.jpg"):
                    f_work.write("create post\n")
                    image = open(dirpath + "tmp.jpg", 'rb')
                    files = {'file': image}
                    values = {"token": set_parameters["token"],
                              "id": set_parameters["id"],
                              "time": datetime.datetime.now().strftime("%d-%m-%Y %H_%M_%S")}
                    p = post(set_parameters["url"], files=files, data=values)
                    f_work.write("Status code - ")
                    f_work.write(str(p.status_code))
                    image.close()

                    time.sleep(3)
                    f_work.write("\ndelete tpm.jpg\n")
                    os.remove(dirpath + "tmp.jpg")
                    f_work.write("sleep...\n")
                f_work.close()
                time.sleep(57)



    def get_config():
        try:
            # pars file config
            tree = ET.parse(str(os.path.abspath(__file__).replace("\create_scrin.pyw","")) + "\config.xml")
            root = tree.getroot()
            # get slack param
            for repository in root:
                if repository.tag == "screenshot":
                    slack_dict = dict()
                    for attribute in repository:
                        slack_dict[attribute.tag] = attribute.text
                    return slack_dict
        except ET.ParseError as error:
            f_err = open("ERROR.txt", "a")
            f_err.write("ERROR!!! " + str(error) + "\n check config file")
            f_err.close()
            exit(1)


    run_screenshot_script()

except Exception as e:
    f_err = open("ERROR.txt", "a")
    f_err.write(str(e))
    f_err.close()
    exit(1)