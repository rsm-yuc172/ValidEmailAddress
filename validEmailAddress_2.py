"""
File: validEmailAddress_2.py
Name: Jack Chen
----------------------------
Select Ten features selected to support:
feature1:  There is no @ in the email. (deduct)
feature2:  After splitting the email with '@', the last str in the list starts with an alpha.
feature3:  No double '.' after the last '@'  (deduct)
feature4:  All ch are alpha after the last '@'.
feature5:  All ch are non-str and non-int before the first '@'. (deduct)
feature6:  Ends with .com/.tw/.edu/.org
feature7:  Email length > 20
feature8:  Start with int or str
feature9:  no str before the first @ (deduct)
feature10: no str after the last @ (deduct)

Accuracy of your model: 0.8461538461538461
"""

import numpy as np

WEIGHT = [                           # The weight vector selected by you
	[-3],                              # (Please fill in your own weights)
	[0.25],
	[-1.8],
	[0.45],
	[-1.8],
	[0.3],
	[0.3],
	[-0.6],
	[-1.8],
	[-1.8]
]

DATA_FILE = 'is_valid_email.txt'     # This is the file name to be processed


def main():
	maybe_email_list = read_in_data()
	accurate_data = 0  # Summing up the total # of accurate data
	n = 1
	for maybe_email in maybe_email_list:
		feature_vector = np.array(feature_extractor(maybe_email))  # 5x1 np array
		weight_vector = np.array(WEIGHT).T  # 1x5 np array
		score = weight_vector.dot(feature_vector)  # counting each email's score w/ numpy array
		if maybe_email in maybe_email_list[:13] and score <= 0:  # the first 13 data should be invalid
			accurate_data += 1
		elif maybe_email in maybe_email_list[13:] and score > 0:  # the last 13 data should be valid
			accurate_data += 1
		print(f"Data{n}: {score}")
		n += 1
	print(accurate_data / len(maybe_email_list))


def feature_extractor(maybe_email):
	"""
	:param maybe_email: str, the string to be processed
	:return: list, feature vector with value 0's and 1's
	"""
	feature_vector = [0] * len(WEIGHT)
	for i in range(len(feature_vector)):
		if i == 0:  # (Deduct) There is no @ in the email.
			feature_vector[i] = 1 if '@' not in maybe_email else 0
		elif i == 1:  # After splitting the email with '@', the last str in the list starts with an alpha.
			if not feature_vector[0]:
				feature_vector[i] = 1 if maybe_email.split('@')[-1][0].isalpha() else 0
		elif i == 2:  # (Deduct) No double '.' after the last '@'.
			if not feature_vector[0]:
				if '.' in maybe_email.split('@')[-1]:
					for j in range(len(maybe_email.split('@')[-1])-1):
						if maybe_email.split('@')[-1][j] == '.':
							if maybe_email.split('@')[-1][j] == maybe_email.split('@')[-1][j+1]:
								feature_vector[i] = 1
		elif i == 3:  # All ch are alpha after the last '@'.
			if not feature_vector[0]:
				feature_vector[i] = 1
				for email in maybe_email.split('@')[-1].split('.'):
					for ch in email:
						feature_vector[i] = 0 if not ch.isalpha else 0
						break
		elif i == 4:  # (Deduct) All ch are non-str and non-int before the first '@'.
			if not feature_vector[0]:
				feature_vector[i] = 1
				for email in maybe_email.split('@')[0]:
					for ch in email:
						if ch.isalpha() or ch.isdigit():
							feature_vector[i] = 0
							break
		elif i == 5:  # Ends with .com/.tw/.edu/.org
			feature_vector[i] = 1 if maybe_email.endswith('.com\n') or maybe_email.endswith('.tw\n') \
								or maybe_email.endswith('.edu\n') or maybe_email.endswith('.org\n') else 0
		elif i == 6:  # Email length > 20
			feature_vector[i] = 1 if len(maybe_email) > 20 else 0
		elif i == 7:  # Start with int or str
			feature_vector[i] = 0
			feature_vector[i] = 1 if not maybe_email[0].isalpha() and not maybe_email[0].isdigit() else 0
		elif i == 8:  # (Deduct) No str before the first @.
			if not feature_vector[0]:
				feature_vector[i] = 1 if len(maybe_email.split('@')[0]) == 0 else 0
		elif i == 9:  # (Deduct) No str after the last @.
			if not feature_vector[0]:
				feature_vector[i] = 1 if maybe_email.find('@') == len(maybe_email) - 2 else 0
	return feature_vector


def read_in_data():
	"""
	:return: list, containing strings that may be valid email addresses
	"""
	lst = []
	with open(DATA_FILE, 'r') as f:
		for line in f:
			lst.append(line)
	return lst


if __name__ == '__main__':
	main()
