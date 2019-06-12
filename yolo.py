import time

import numpy as np
import argparse
import cv2 as cv
from urllib.request import urlopen
import socket

import ctypes





from yolo_utils import infer_image, show_image

FLAGS = []
sizes = [0.75, 0, 1.75, 1]

class boxInfo:
    def __init__(self, classID, x, y, a, b):
        self.classID = classID
        self.x = x
        self.y = y
        # a es el desplazamiento del punto x para formar la caja
        # b es el desplazamiento del punto y para formar la caja

        self.a = a
        self.b = b
        #print("---Clase " + str(classids[box]) + " detectada---")
        # cx y cx establecen el punto central de la caja

        self.cx = x + (a / 2)
        self.cy = y + (b / 2)
        #print ("Esquinas de la caja: [" + str(x) + "," + str(y) + "] ; [" + str(x + a) + "," + str(y + b) + "]")
        #print("Puntos central es: " + str(self.cx) + "," + str(self.cy))

        # tennisball= 0, robot = 2, marca = 3
        # classids determina que clase fue
        # detectada en cada elemento de boxes
        # El promedio de porcentaje de pantalla que cubre el target repartido en x y y

        self.escalaCuadrado = (float(a) / width + float(b) / height) / 2
        #print ("Escala en pantalla: " + str(self.escalaCuadrado))
        #la distancia se traduce en unidades de 2.35 cuartas
        self.distancia = -np.math.log((self.escalaCuadrado / sizes[classID]) ** 2.35, 10)
        #print("Distancia: " + str(self.distancia))





def send(character):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('192.168.43.59', 9000))
            s.sendall(character.encode() + b"\r\n")
            s.close()
    except Exception as e:
        print(e.args)
try:
    HOST = input("ip del telefono: ")  # The server's hostname or IP address
    PORT = int(input("puerto del telefono: "))        # The port used by the server
    print(HOST + ":" + str(PORT))
except:
    print ("no valid socket provided")


def desicion(listaBoxes, ancho, alto):

    tennisball = " "
    robot = " "
    marca = " "
    mitad = ancho / 2

    if(len(listaBoxes)==0):
        print("No encontró nada")
        print("Izquierda")
        send('l')
    # -----------------------------------------------------------------
    else:
        for info in listaBoxes:
            if info.classID == 0:
                tennisball = info

            elif info.classID == 2:

                robot = info
            elif info.classID == 3:

                marca = info

        # -------------------------------------------------------------------------------------
        if tennisball != " ":
            print(tennisball.distancia)

            if robot == " ":
                print("Bola, sin robot")



                if tennisball.distancia > 0.8:
                    print("Debe acercase más")
                    #send('m')
                    Direccion(tennisball, mitad, ancho)
                    # -----------------------------------------------------------------
                    if marca != " ":
                        if marca.distancia > 0.8:
                            Direccion(tennisball, mitad, ancho)
                    else:
                        print("Bola, sin robot, con marca, buscar la marca")
                else:
                    Direccion(tennisball, mitad, ancho)
                    print("Debe moverse al frente")
                  #  send('u')


            # -----------------------------------------------------------------
            elif robot != " ":

                if robot.distancia < 1.0 and tennisball.distancia < 0.3:
                    Direccion(robot, mitad, ancho)
                    print("Debe alejarse o rodearlo, lleva la bola")

                if marca != " ":
                    Direccion(marca, mitad, ancho)
                    print("Bola, con marca, con robot")

                else:
                    #Direccion(marca, mitad, ancho)
                    print("Bola, con robot")

        # -----------------------------------------------------------------
        else:
            if robot != " ":
                print("Sin bola, con robot")

                if robot.distancia < 1.0:
                    print("hacer para atrás")
                    #Direccion(marca, mitad, ancho)

    print("-------------------------------------------------------------------")

timer = 0
def Direccion (objeto, mitad, ancho):
    if objeto.cx < (mitad - (ancho * 0.1)):
        send('f')
        time.sleep(timer)
        print("izquierda")
        send('l')
        time.sleep(timer)


    elif objeto.cx > (mitad + (ancho * 0.1)):
        send('f')
        time.sleep(timer)
        print("derecha")
        send('r')
        time.sleep(timer)

    else:
        send('m')
        time.sleep(timer)
        print("Centro")
        send('u')
        time.sleep(timer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model-path',
                        type=str,
                        default='./yolov3-coco/',
                        help='The directory where the model weights and \
			  configuration files are.')

    parser.add_argument('-w', '--weights',
                        type=str,
                        default='./yolov3-coco/yolov3.weights',
                        help='Path to the file which contains the weights \
			 	for YOLOv3.')

    parser.add_argument('-cfg', '--config',
                        type=str,
                        default='./yolov3-coco/yolov3.cfg',
                        help='Path to the configuration file for the YOLOv3 model.')

    parser.add_argument('-vo', '--video-output-path',
                        type=str,
                        default='./output.avi',
                        help='The path of the output video file')

    parser.add_argument('-l', '--labels',
                        type=str,
                        default='./yolov3-coco/coco-labels',
                        help='Path to the file having the \
					labels in a new-line seperated way.')

    parser.add_argument('-c', '--confidence',
                        type=float,
                        default=0.25,
                        help='The model will reject boundaries which has a \
				probabiity less than the confidence value. \
				default: 0.5')

    parser.add_argument('-th', '--threshold',
                        type=float,
                        default=0.3,
                        help='The threshold to use when applying the \
				Non-Max Suppresion')

    parser.add_argument('--download-model',
                        type=bool,
                        default=False,
                        help='Set to True, if the model weights and configurations \
				are not present on your local machine.')

    parser.add_argument('-t', '--show-time',
                        type=bool,
                        default=False,
                        help='Show the time taken to infer each image.')

    FLAGS, unparsed = parser.parse_known_args()

    # Get the labels
    labels = open(FLAGS.labels).read().strip().split('\n')

    # Intializing colors to represent each label uniquely
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')

    # Load the weights and configutation to form the pretrained YOLOv3 model
    net = cv.dnn.readNetFromDarknet(FLAGS.config, FLAGS.weights)

    # Get the output layer names of the model
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Infer real-time on webcam
    url = 'http://' + input("ip:puerto de la cámara: ")+'///shot.jpg?rnd=846518'
    count = 0

    while True:
        try:
            imgResp = urlopen(url)
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            img = cv.imdecode(imgNp, -1)
        except Exception as e:
            print(e.args)
            continue

        # _, frame = vid.read()
        height, width = img.shape[:2]
        if count == 0:
            img, boxes, confidences, classids, idxs = infer_image(net, layer_names, height, width, img, colors, labels, FLAGS)
            count += 1
        else:
            img, boxes, confidences, classids, idxs = infer_image(net, layer_names, height, width, img, colors, labels,
                                                                  FLAGS,
                                                                  boxes, confidences, classids, idxs, infer=False)
            count = (count + 1) % 6
        boxInfos = []
        for box in range(0, len(boxes)):
            boxInfos.append(boxInfo(classids[box], boxes[box][0],boxes[box][1],boxes[box][2],boxes[box][3]))

            # print(str(classids[box]) + ": " + str(a) + " + " + str(b) + " = " + str(squareSize))
        print("deicidir")
        desicion(boxInfos, width, height)
        cv.imshow('Object Detection with OpenCV', img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # cap.release()
    cv.destroyAllWindows()
