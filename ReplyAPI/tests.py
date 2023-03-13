from datetime import date
from django.test import TestCase
from .models import User, Payment
from django.urls import reverse
from ReplyAPI.models import User
from ReplyAPI.forms import RegisterForm, PaymentForm
from django.test import TestCase
from .forms import RegisterForm, PaymentForm


class UserModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            credit_card='1234567890123456',
            dob='2000-01-01'
        )

    def test_user_model(self):
        """Test user model attributes"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.credit_card, '1234567890123456')
        self.assertEqual(str(self.user.dob), '2000-01-01')



class PaymentModelTestCase(TestCase):

    def setUp(self):
        self.payment = Payment.objects.create(
            credit_card='1234567890123456',
            amount='100'
        )

    def test_payment_model(self):
        """Test payment model attributes"""
        self.assertEqual(self.payment.credit_card, '1234567890123456')
        self.assertEqual(self.payment.amount, '100')



class HomeViewTestCase(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

class RegisterViewTestCase(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'Register')

    def test_register_view_post_invalid_form(self):
        response = self.client.post(reverse('register'), data={})
        self.assertEqual(response.status_code, 400)

    def test_register_view_post_existing_username(self):
        User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword', dob='2000-01-01')
        response = self.client.post(reverse('register'), data={'username': 'testuser', 'email': 'testuser2@example.com', 'password': 'testpassword2', 'dob': '2000-01-01'})
        self.assertEqual(response.status_code, 400)

    def test_register_view_post_underage(self):
        dob = date.today().replace(year=date.today().year - 17).strftime('%Y-%m-%d')
        response = self.client.post(reverse('register'), data={'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpassword', 'dob': dob})
        self.assertEqual(response.status_code, 403)

    def test_register_view_post_valid_form(self):
        response = self.client.post(reverse('register'), data={'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpassword', 'dob': '2000-01-01'})
        self.assertEqual(response.status_code, 201)


class PaymentViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpassword',
            dob='2000-01-01'
        )
        self.payment = Payment.objects.create(
            credit_card='1234567890123456',
            amount='100'
        )

    def test_payment_view_post_invalid_credit_card(self):
        response = self.client.post(reverse('payment'), data={'credit_card': '123', 'amount': '100'})
        self.assertEqual(response.status_code, 400)

    def test_payment_view_post_invalid_amount(self):
        response = self.client.post(reverse('payment'), data={'credit_card': '1234567890123456', 'amount': '1'})
        self.assertEqual(response.status_code, 400)

    def test_payment_view_post_nonexistent_credit_card(self):
        response = self.client.post(reverse('payment'), data={'credit_card': '1234567890123450', 'amount': '100'})
        self.assertEqual(response.status_code, 404)


class RegisterFormTestCase(TestCase):

    def test_register_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'dob': '2000-01-01',
            'credit_card': '4434567890123456',
            'password': 'testpassword',
            'password_confirmation': 'testpassword',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())


class PaymentFormTestCase(TestCase):

    def test_payment_form_invalid_data(self):
        form_data = {
            'credit_card': '1234',
            'amount': -100.00,
        }
        form = PaymentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('credit_card', form.errors)
        self.assertIn('amount', form.errors)

