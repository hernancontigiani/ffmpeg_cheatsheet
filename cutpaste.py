import os
from datetime import datetime


class Tramo():
    def __init__(self, start, end):
        self.start = start
        self.end = end

        tstart = self.__text2time(self.start)
        tend = self.__text2time(self.end)

        self.duration =  (tend - tstart).seconds

    def __text2time(self, text):
        if text.count(':') == 1:
            return datetime.strptime(text, '%M:%S')
        if text.count(':') == 2:
            return datetime.strptime(text, '%H:%M:%S')

        raise ValueError

class Seccion():
    def __init__(self, video_input, name):
        self.video_input = video_input
        self.name = name
        self.tramos = []

    def add(self, start, end):
        self.tramos.append(Tramo(start, end))

    def create(self):
        tramo_list = open('tramo_list.txt', 'w')
        for i, tramo in enumerate(self.tramos):
            os.system(f'ffmpeg -ss {tramo.start} -i {self.video_input} -t {tramo.duration} -c copy {i}.mp4 -y')
            tramo_list.write(f"file '{i}.mp4'\n")
        tramo_list.flush()
        base_path = os.path.dirname(self.video_input)
        output_path = os.path.join(base_path, self.name)
        # Para ffmpeg >=4.3
        #os.system(f'ffmpeg -f concat -safe 0 -i tramo_list.txt -filter_complex "xfade=offset=4.5:duration=1" -c copy {output_path}.mp4 -y')
        os.system(f'ffmpeg -f concat -safe 0 -i tramo_list.txt -c copy {output_path}.mp4 -y')
        
        


if __name__ == '__main__':

    folder = './'       # video folder name

    # Se asume que dentro de la carpeta hay un video que lleva el mismo nombre
    video_path = os.path.join(folder, 'input.mp4')
    escenas = os.path.join(folder, 'escenas.txt')
    secciones = []

    with open(escenas, 'r') as fi:
        for line in fi:
            data = [x for x in line.replace('\n', '').split('\t') if len(x) > 0]
            if len(data) == 0:
                break

            if len(secciones) > 0:
                if secciones[-1].name != data[0]:
                    secciones.append(Seccion(video_path, data[0]))
            else:
                secciones.append(Seccion(video_path, data[0]))
            secciones[-1].add(data[1], data[2])

    for seccion in secciones:
        seccion.create()


