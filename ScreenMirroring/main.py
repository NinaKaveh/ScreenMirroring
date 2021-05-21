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
from tkinter import messagebox
from bluetooth import *

ImageFile.LOAD_TRUNCATED_IMAGES = True

global photo


def fenetre_principale():
    global main_w
    main_w = tk.Tk()
    main_w.title("ScreenMirroring Application")
    main_w.configure(bg="white")
    #image_presentation = Image.open("C:\\Users\\vicle\\Pictures\\screen_mirror_icon.png")
    image_presentation = Image.open("screen_mirror_icon.png")
    couverture = ImageTk.PhotoImage(image_presentation)
    couverture_label = tk.Label(main_w, image=couverture)
    couverture_label.pack(side="top", fill="both", expand="yes")
    global message_label
    message_label = tk.Label(main_w, text="Appuyez sur Connexion pour lancer la synchronisation")
    message_label.pack(side="top", fill="both", expand="yes")
    bouton_stop = tk.Button(main_w, text="Déconnexion", bg="#ff8080", command=deconnexion)
    bouton_stop.pack(side="bottom")
    bouton_connexion = tk.Button(main_w, text="  Connexion  ", bg="#87b5ff", command=lancement_socket)
    bouton_connexion.pack(side="bottom")

    main_w.protocol("WM_DELETE_WINDOW", quit_program)
    main_w.mainloop()


def creation_canvas():
    global window
    window = tk.Toplevel()
    window.title("Android Screen")
    # global canvas
    # canvas = tk.Canvas(window, width=1920, height=1080)
    # canvas.pack()

    im = Image.open("screen_mirror_icon.png")
    couv = ImageTk.PhotoImage(im)
    global panel
    panel = tk.Label(window, image=couv)
    panel.pack(side="bottom", fill="both", expand="yes")
    window.protocol("WM_DELETE_WINDOW", closing_image)
    #window.loop()

def closing_image():
    if messagebox.askokcancel("Deconnexion", "Voulez-vous vous déconnecter ?"):
        deconnexion()

def quit_program():
    if messagebox.askokcancel("Quitter", "Voulez-vous quitter ?"):
        main_w.destroy()
        exit()

def lancement_socket():
    global all
    all = threading.Thread(target=reception)
    all.daemon = True
    all.start()


y = threading.Thread(target=fenetre_principale)
#y.daemon = True
y.start()


def reception():
    global server_sock
    global client_sock
    global client_info
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

    message_label.config(text="En attente de connection au RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()
    message_connexion = "Connexion acceptée avec " + client_info[0]

    message_label.config(text=message_connexion)
    img_tmp = []
    nb_images = 0
    indice_stop = 0
    global x
    x = threading.Thread(target=creation_canvas)
    x.daemon = True
    x.start()

    try:
        while True:

            # data = client_sock.recv(102400000)
            data = client_sock.recv(1999999999)
            if len(data) == 0: break
            # print("Paquet reçu : [%s]" % data)
            # y = threading.Thread(target=afficher_image, args=(data,))
            if 'START' in str(data):
                img_tmp = []
                nb_images += 1
                data = data[5:]
                indice_stop = 0
            if 'STOP' in str(data):
                data = data[:-4]
                indice_stop = 1
                print(nb_images)
            img_tmp.append(data)
            if indice_stop == 1:
                for i in range(0, len(img_tmp)):
                    str_img = img_tmp[i]
                    if i == 0:
                        img_byte = str_img
                    else:
                        img_byte += str_img

                img_tmp = []
                image = Image.open(io.BytesIO(img_byte))
                image = image.resize((1920, 1920))
                image = image.rotate(90)
                image = image.resize((1920, 1000))

                photo = ImageTk.PhotoImage(image)
                # canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                panel.configure(image=photo)
                panel.image = photo
                client_sock.send('OK')

                # canvas.mainloop().
                # image.show()

            # print(type(data))
    except IOError:
        pass

    deconnexion()


def deconnexion():
    try:
        client_sock.close()
        server_sock.close()
        window.destroy()
    except NameError:
        pass
    message_label.config(text="Déconnecté de l'appareil Android")


