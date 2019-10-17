import pickle
import numpy as np


class MovieBasedPredictor(object):
	def __init__(self):
		self.item_distributions = dict()

	def train(self, training_set_file_path):
		with open(training_set_file_path, 'rb') as training_set_file:
			training_set = pickle.load(training_set_file)
			rows_non_zero, cols_non_zero = training_set.nonzero()
			for i in range(len(rows_non_zero)):
				current_user, current_item = rows_non_zero[i], cols_non_zero[i]
				try:
					self.item_distributions[current_item].append(training_set[current_user, current_item])

				except:
					self.item_distributions[current_item] = []
					self.item_distributions[current_item].append(training_set[current_user, current_item])

	def predict(self, testing_set_file_path, possible_values):
		with open(testing_set_file_path, 'rb') as testing_set_file:
			testing_set = pickle.load(testing_set_file)
			rows_non_zero, cols_non_zero = testing_set.nonzero()
			mae = 0
			for i in range(len(rows_non_zero)):
				user, item = rows_non_zero[i], cols_non_zero[i]
				actual_rating = testing_set[user, item]
				try:
					train_ratings_for_item = self.item_distributions[item]
					predicted_rating = train_ratings_for_item[np.random.randint(0, len(train_ratings_for_item))]
				except:
					predicted_rating = possible_values[np.random.randint(0, len(possible_values))]
				mae += abs(actual_rating - predicted_rating) / len(rows_non_zero)
			return mae