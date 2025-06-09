from django.test import TestCase

#  to conduct tests here.
class TestViews(TestCase):
    def setUp(self):
        # Set up any necessary data or state before each test
        pass

    def test_example(self):
        # Example test case
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to the Main App")
    
    def tearDown(self):
        # Clean up after each test if necessary
        pass
