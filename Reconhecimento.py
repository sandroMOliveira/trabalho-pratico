#Fonte adaptado do seguinte site
#https://hackernoon.com/face-recognition-using-opencv-a-step-by-step-guide-to-build-a-facial-recognition-system-8da97cd89847


#import libraries
import cv2
import face_recognition

# Get a reference to webcam

imagem = cv2.imread('ronaldinho.png')


imagem2 = cv2.imread('turma.jpg')


face_encoding = face_recognition.face_encodings(imagem)[0]

faces_conhecidas = [
    face_encoding
]

face_locations = []

import pdb; pdb.set_trace()
rgb_frame = imagem2[:, :, ::-1]

#Detecta todas as faces em uma imagem
face_locations = face_recognition.face_locations(rgb_frame)
face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)


face_names = []
for face_encoding in face_encodings:
   # Compara a imagem de busca com todos os rostos existentes na imagem atual.
   match = face_recognition.compare_faces(faces_conhecidas, face_encoding, tolerance=0.50)


name = None
if match:
  name = "Ronaldinho"

face_names.append(name)

#Aplica a label nas faces encontradas
for (top, right, bottom, left), name in zip(face_locations, face_names):
    if not name:
       continue

#Desenha um retangulo  em torno da face
cv2.rectangle(imagem2, (left, top), (right+5, bottom+5), (0, 127, 255), 2)

#Inclui o nome da face identificada
cv2.rectangle(imagem2, (left - 10, bottom + 30), (right + (len(name) * 4), bottom + 10), (0, 127, 255), cv2.FILLED)
font = cv2.FONT_HERSHEY_DUPLEX
cv2.putText(imagem2, name, (left - 10, bottom + 20), font, 0.5, (255, 255, 255), 1)


# Apresenta o resultado da imagem
cv2.imshow('Video', imagem2)


cv2.waitKey(0)
cv2.destroyAllWindows()