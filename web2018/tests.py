# -*- coding: utf-8 -*-

from django.test import TestCase


class ExampleTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_abc(self):
        self.assertEqual(1, 1)

