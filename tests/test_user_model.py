import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):

	# Test setter method
	def test_password_setter(self):
		user = User(password='cat')
		self.assertTrue(user.password_hash is not None)


	# Test getter method
	def test_no_password_getter(self):
		user = User(password='cat')
		with self.assertRaises(AttributeError):
			user.password


	# Test password verification
	def test_password_verification(self):
		user = User(password='cat')
		self.assertTrue(user.verify_password('cat'))
		self.assertFalse(user.verify_password('dog'))


	# Test the same password and return diferent hashes
	def test_password_salt_are_random(self):
		user1 = User(password='cat')
		user2 = User(password='cat')
		self.assertFalse(user1.password_hash == user2.password_hash)