test-main.py
import app
import unittest

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_form_submission(self):
        response = self.app.post('/', data=dict(loan_amount=10000, loan_term=12, interest_rate=5))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Monthly payment:", response.data)
        self.assertIn(b"Overpayment:", response.data)
        self.assertIn(b"Total payout:", response.data)

    def test_int_to_currency(self):
        self.assertEqual(app.int_to_currency(1000), '1 000 ₽')
        self.assertEqual(app.int_to_currency(5000000), '5 000 000 ₽')


if __name__ == '__main__':
    unittest.main()