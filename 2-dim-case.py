import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import glob

directory = os.getcwd()

D, v, dt, dx, T, L, Nx, Ny = list(map(float, input().split()))

# Задаем параметры задачи
# D = 0.1  # Коэффициент диффузии
# v = 0.5  # Скорость конвекции
# dt = 0.01  # Шаг времени
# T = 1.0  # Общее время
# L = 1.0  # Длина почвенной области
# Nx = 20  # Количество пространственных шагов вдоль оси x
# Ny = 20  # Количество пространственных шагов вдоль оси y

# Вычисляем размеры пространственной сетки
dx = L / (Nx - 1)
dy = L / (Ny - 1)

# Вычисляем количество временных шагов
Nt = int(T / dt)

# Создаем сетку для хранения концентрации
c = np.zeros((Nt, Nx, Ny))

# Задаем начальное распределение концентрации
c[0, :, :] = 1.0

# Создаем список для хранения кадров видеоряда
frames = []

# Цикл по временным шагам
for n in range(Nt - 1):
    # Цикл по пространственным шагам
    for i in range(1, Nx - 1):
        for j in range(1, Ny - 1):
            # Рассчитываем изменение концентрации с использованием метода конечных разностей
            c[n + 1, i, j] = c[n, i, j] + (dt * D * ((c[n, i + 1, j] - 2 * c[n, i, j] + c[n, i - 1, j]) / dx ** 2 +
                                                     (c[n, i, j + 1] - 2 * c[n, i, j] + c[n, i, j - 1]) / dy ** 2)) \
                             - (dt * v * (c[n, i + 1, j] - c[n, i - 1, j]) / (2 * dx)) \
                             - (dt * v * (c[n, i, j + 1] - c[n, i, j - 1]) / (2 * dy))

    # Генерируем кадр для текущего временного шага
    plt.contourf(c[n, :, :], cmap='viridis')
    plt.colorbar(label='Концентрация')
    plt.xlabel('x')
    plt.ylabel('y')

    # Сохраняем текущий график как изображение
    plt.savefig(f'frame_{n:04d}.png', dpi=300)

    # Очищаем текущий график для следующего временного шага
    plt.clf()

    # Читаем сохраненное изображение и добавляем его в список кадров
    frame = cv2.imread(f'frame_{n:04d}.png')
    frames.append(frame)

# Создаем видеоряд
height, width, _ = frames[0].shape
video_writer = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

# Записываем каждый кадр в видео
for frame in frames:
    for i in range(100):
        video_writer.write(frame)

# Завершаем запись видео
video_writer.release()


files = glob.glob(directory + "\\*.png")

for file in files:
    os.remove(file)

print('Everything is done')
