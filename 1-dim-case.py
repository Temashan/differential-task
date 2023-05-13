import numpy as np
import matplotlib.pyplot as plt
import cv2
import glob
import os

D, v, dt, dx, T, L = list(map(float, input().split()))

# Задаем параметры задачи
# D = 0.1  # Коэффициент диффузии
# v = 0.5  # Скорость конвекции
# dt = 0.01  # Шаг времени
# dx = 0.1  # Шаг пространственного разбиения
# T = 1.0  # Общее время
# L = 1.0  # Длина области

# Вычисляем количество временных и пространственных шагов
Nt = int(T / dt)
Nx = int(L / dx)

# Создаем массив для хранения концентрации в каждый момент времени и в каждой точке
c = np.zeros((Nt, Nx))

# Задаем начальное распределение концентрации
c[0, :] = 1.0  # Начальная концентрация

# Создаем список для хранения кадров видеоряда
frames = []

# Цикл по временным шагам
for n in range(Nt - 1):
    # Цикл по пространственным шагам
    for i in range(1, Nx - 1):
        # Рассчитываем изменение концентрации с использованием метода конечных разностей
        c[n + 1, i] = c[n, i] + (dt * D * (c[n, i + 1] - 2 * c[n, i] + c[n, i - 1]) / dx ** 2) \
                      - (dt * v * (c[n, i + 1] - c[n, i - 1]) / (2 * dx))

    # Графическое представление результата
    x = np.linspace(0, L, Nx)
    plt.plot(x, c[n, :])
    plt.xlabel('x')
    plt.ylabel('Концентрация')
    plt.title('Распределение концентрации со временем')
    plt.ylim(0, 1)  # Ограничение по оси y для лучшей видимости
    plt.grid(True)

    # Преобразуем текущий график в изображение
    fig = plt.gcf()
    fig.canvas.draw()
    image = np.array(fig.canvas.renderer.buffer_rgba())

    # Добавляем кадр в список
    # frames.append(image)

    plt.savefig(f'frame_{n:04d}.png', dpi=300)

    # Очищаем текущий график для следующего временного шага
    plt.clf()

    # Читаем сохраненное изображение и добавляем его в список кадров
    frame = cv2.imread(f'frame_{n:04d}.png')
    frames.append(frame)

# Создаем видеоряд
height, width, _ = frames[0].shape
video = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

# Записываем кадры в видеоряд
for frame in frames:
    video.write(frame)

# Закрываем видеоряд
video.release()

directory = os.getcwd()
files = glob.glob(directory + "\\*.png")

for file in files:
    os.remove(file)

print('Everything is done')

