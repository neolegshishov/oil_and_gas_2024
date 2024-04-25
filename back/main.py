import json
import os.path

from flask import Flask, send_file, request, render_template
from joblib import load
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

import uuid


app = Flask(__name__)
app.template_folder = 'templates'
app.static_folder = 'static'


MODEL = load('itog.joblib')


def get_predict(data: dict):
	print(data)
	dictionary = dict(
		zip(
			['Time', 'Temperature', 'Uvx', 'Uvy', 'Uvz', 'Collision', 'Gas'],
			[
				[float(data['time'])], [float(data['temperature'])], [float(data['Ux'])], [float(data['Uy'])], [float(data['Uz'])], [0], [0]
			]
		)
	)
	array = DataFrame(dictionary)
	answer = MODEL.predict(array)

	# Векторы a и b
	a = np.array([float(data['Ux']), float(data['Uy']), float(data['Uz'])])
	b = np.array(answer[0])

	print(a, b)

	# Временной массив
	t = np.linspace(0, 1, 40)

	# Задаем позиционные массивы для векторов
	x_a = np.linspace(0, a[0], 20)
	y_a = np.linspace(0, a[1], 20)
	z_a = np.linspace(0, a[2], 20)

	x_b = np.linspace(a[0], a[0] + b[0], 20)
	y_b = np.linspace(a[1], a[1] + b[1], 20)
	z_b = np.linspace(a[2], a[2] + b[2], 20)

	# Задаем набор данных для анимации
	dataSet_a = np.array([x_a, y_a, z_a])  # Для вектора a
	dataSet_b = np.array([x_b, y_b, z_b])  # Для вектора b

	numDataPoints = len(t)

	def animate_func(num):
		ax.clear()
		if num < numDataPoints:
			ax.plot3D(dataSet_a[0, :num + 1], dataSet_a[1, :num + 1], dataSet_a[2, :num + 1], c='blue')
			if num > 20:
				num_b = num - 20
				ax.plot3D(dataSet_b[0, :num_b + 1], dataSet_b[1, :num_b + 1], dataSet_b[2, :num_b + 1], c='red')
				ax.scatter(dataSet_b[0, num_b], dataSet_b[1, num_b], dataSet_b[2, num_b], c='red', marker='o')
		else:
			ax.plot3D(dataSet_a[0, :], dataSet_a[1, :], dataSet_a[2, :], c='blue')
			ax.plot3D(dataSet_b[0, :], dataSet_b[1, :], dataSet_b[2, :], c='red')

		ax.plot3D([0, 0], [0, 0], [0, 0], c='black', marker='o')
		ax.set_xlim3d([-10, 10])
		ax.set_ylim3d([-10, 10])
		ax.set_zlim3d([-10, 10])

		ax.set_title('Vector Animation')
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')

	# Рисуем анимацию
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	line_ani = animation.FuncAnimation(fig, animate_func, interval=50, frames=numDataPoints * 2)
	# Сохраняем анимацию
	f = uuid.uuid4().hex + '.gif'
	writergif = animation.PillowWriter(fps=numDataPoints)
	line_ani.save(f, writer=writergif)
	return os.path.abspath(f)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
	return send_file(get_predict(json.loads(request.data.decode())), mimetype='image/gif')


app.run(host='0.0.0.0', port=8000, debug=True)
