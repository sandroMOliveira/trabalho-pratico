# -*- coding: UTF-8 -*-

import cv2
import face_recognition
import numpy as np
import csv

def convertMillis(millis):
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    return f'{minutes}:{seconds}'

def split_video_channels():
    print('''
        Integrantes:
        Daniel Águila,
        Gabrielle Liberato,
        Sandro Oliveira
    ''')

    image_recognation = face_recognition.load_image_file('rostos/ronaldinho.png')
    face_encoding = face_recognition.face_encodings(image_recognation)[0]

    find_faces = [
        face_encoding
    ]

    faces_locations = []
    face_encodings = []
    face_names = []
    frame_number = 0


    cap = cv2.VideoCapture('videos/ronaldinho.mp4')
    size = (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    codec = cv2.VideoWriter_fourcc(*'DIVX')
    output_face = cv2.VideoWriter('ronaldinho_face.avi', codec, 29.97, size)
    frame_number = 0
    count_aparicao = 0
    tempo_aparicao = {}
    tempo_init = 0
    print('Seu vídeo está em processamento, vá tomar um café ou assistir um GOT!')
    file = csv.writer(open('relatorio.csv', 'w'))
    file.writerow(['Aparicao', 'Personagem', 'Tempo Inicial', 'Tempo Final'])
    while True:
        ret_val, frame = cap.read()
        frame_number += 1
        if frame is None:
            break

        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        faces_encondings = face_recognition.face_encodings(rgb_frame, face_locations)

        
        face_names = []

        # import pdb; pdb.set_trace()
        for face_encoding in faces_encondings:
            match = face_recognition.compare_faces(find_faces, face_encoding, tolerance=0.50)
        
            # import pdb; pdb.set_trace()
            name = None
            if match[0]:
                # import pdb; pdb.set_trace()
                tempo_init = cap.get(cv2.CAP_PROP_POS_MSEC) if tempo_init == 0 else 0
                name = "Ronaldinho"
            elif not match[0] and tempo_init > 0:
                count_aparicao += 1
                file.writerow([
                    count_aparicao, 
                    'Ronaldinho', 
                    convertMillis(tempo_init), 
                    convertMillis(cap.get(cv2.CAP_PROP_POS_MSEC))
                ])
                tempo_init = 0
            face_names.append(name)

        #Aplica a label nas faces encontradas
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if not name:
                continue

            # Desenha um retangulo  em torno da face
            cv2.rectangle(frame, (left, top), (right + 5, bottom + 5), (0, 127, 255), 2)

            # Inclui o nome da face identificada
            cv2.rectangle(frame, (left - 10, bottom + 30), (right + (len(name) * 4), bottom + 10), (0, 127, 255),
                            cv2.FILLED)

            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left - 10, bottom + 20), font, 0.5, (255, 255, 255), 1)

        #Para ver o os frames em construção
        print(f'Writing frame {frame_number} / {length}')
        # cv2.imshow('Video Face', frame)
        output_face.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print('Terminou!')
    cap.release()
    cv2.destroyAllWindows()

split_video_channels()
