# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import threading
import cv2
import os
import io
# import PIL.Image as Image
from PIL import Image, ImageTk, ImageFile
import numpy as np
import tkinter as tk
from array import array

from bluetooth import *

ImageFile.LOAD_TRUNCATED_IMAGES = True


def creation_canvas():
    global window
    window = tk.Tk()
    global canvas
    canvas = tk.Canvas(window, width=1920, height=1080)
    canvas.pack()
    window.mainloop()


def afficher_image(data, img_tmp):
    if 'xff\xd8\xff\xe0\x00\x10JFIF' in str(data) and len(img_tmp) != 0:
        print("Paquet reçu : [%s]" % data)
        print(len(img_tmp))

        for i in range(0, len(img_tmp)):
            str_img = img_tmp[i]
            if i == 0:
                img_byte = str_img
            else:
                # img_byte.extend(str_img)
                img_byte += str_img
            # if i != len(img_tmp) - 1:
            #    str_img = str_img[:-2]

            # if i != 0:
            #    img_tmp[i] = str_img[3:]
            # print("Le byte " + str(i) + " est " + str(str_img))
        # img_byte = ''.join(str(img_tmp))
        # img_byte = img_byte+"'"
        # print(img_byte)
        img_tmp = []
        image = Image.open(io.BytesIO(img_byte))
        # image = image.resize((1920, 1920))
        # image = image.rotate(90)
        # image = image.resize((1920, 1000))
        # image = image.resize(image.size / 2)
        # im_np = np.asarray(image)
        # out.write(im_np)
        # out.release()
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        # canvas.mainloop().
        # image.show()
    img_tmp.append(data)
    # print(type(data))


server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "52be30ba-5471-420c-b666-c42069fd4578"  # mettre le même sur la partie android

advertise_service(server_sock, "Serveur_de_reception",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
                  )

print("En attente de connection au RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Connection acceptée avec ", client_info)
img_tmp = []
# out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, (1920, 1080))
x = threading.Thread(target=creation_canvas)
x.start()
print(len(img_tmp))
try:
    while True:

        data = client_sock.recv(10240000)
        if len(data) == 0: break
        #y = threading.Thread(target=afficher_image, args=(data,))
        if 'x10JFIF' in str(data) and len(img_tmp) != 0:
            print("Paquet reçu : [%s]" % data)
            print(len(img_tmp))

            for i in range(0, len(img_tmp)):
                str_img = img_tmp[i]
                if i == 0:
                    img_byte = str_img
                else:
                    # img_byte.extend(str_img)
                    img_byte += str_img
                # if i != len(img_tmp) - 1:
                #    str_img = str_img[:-2]

                # if i != 0:
                #    img_tmp[i] = str_img[3:]
                # print("Le byte " + str(i) + " est " + str(str_img))
            # img_byte = ''.join(str(img_tmp))
            # img_byte = img_byte+"'"
            # print(img_byte)
            img_tmp = []
            image = Image.open(io.BytesIO(img_byte))
            # image = image.resize((1920, 1920))
            # image = image.rotate(90)
            # image = image.resize((1920, 1000))
            # image = image.resize(image.size / 2)
            # im_np = np.asarray(image)
            # out.write(im_np)
            # out.release()
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            # canvas.mainloop().
            # image.show()
        img_tmp.append(data)
        # print(type(data))
except IOError:
    pass
    print("error")

print("Connexion à l'appareil perdue")

client_sock.close()
server_sock.close()
print("Terminé")
