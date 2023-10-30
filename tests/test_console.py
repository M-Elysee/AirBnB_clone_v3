#!/usr/bin/python3
""" Testing suite for console"""

import sys
import models
import unittest
from models import storage
from models import State
from models.engine.db_storage import DBStorage
from io import StringIO
import console
import inspect
import pep8
from console import HBNBCommand
from unittest.mock import create_autospec
from os import getenv
HBNBCommand = console.HBNBCommand


class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    def test_pep8_conformance_console(self):
        """Testing that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['console.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Testing that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Testing for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Testing for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")


class test_console(unittest.TestCase):
    """ Testing console module """
    def setUp(self):
        """ Testing setup"""
        self.backup = sys.stdout
        self.capt_out = StringIO()
        sys.stdout = self.capt_out

    def tearDown(self):
        """ Testing tear down """
        sys.stdout = self.backup

    def create(self):
        """ Testing instance of creating HBNBCommand class"""
        return HBNBCommand()

    def test_quit(self):
        """ Testing 'quit' command exists"""
        cons = self.create()
        self.assertTrue(cons.onecmd("quit"))

    def test_EOF(self):
        """ Testing 'EOF' command exists"""
        cons = self.create()
        self.assertTrue(cons.onecmd("EOF"))

    def test_all(self):
        """ Testing 'all' command exists"""
        cons = self.create()
        cons.onecmd("all")
        self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    @unittest.skipIf(db == "db", "Testing database storage only")
    def test_show(self):
        """ Testing 'show' command exists """
        cons = self.create()
        cons.onecmd("create User")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        cons.onecmd("show User " + user_id)
        xv = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertTrue(str is type(xv))

    @unittest.skipIf(db == "db", "Testing database storage only")
    def test_class_name_show(self):
        """ Testing class name missing error messages """
        cons = self.create()
        cons.onecmd("create User")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        cons.onecmd("show")
        xv = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual("** class name missing **\n", xv)

    def test_show_class_name(self):
        """Testing show message error for id missing
        """
        cons = self.create()
        cons.onecmd("create User")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        cons.onecmd("show User")
        xv = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual("** instance id missing **\n", xv)

    @unittest.skipIf(db == "db", "Testing database storage only")
    def test_show_no_instance_found(self):
        """Testing show message error for id missing
        """
        cons = self.create()
        cons.onecmd("create User")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        cons.onecmd("show User " + "124356876")
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual("** no instance found **\n", x)

    def test_create(self):
        """Testing that create works
        """
        cons = self.create()
        cons.onecmd("create User email=adriel@hbnb.com password=abc")
        self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    def test_class_name(self):
        """Testing error messages for class name missing.
        """
        cons = self.create()
        cons.onecmd("create")
        xv = (self.capt_out.getvalue())
        self.assertEqual("** class name missing **\n", xv)

    def test_class_name_doest_exist(self):
        """Testing error messages for class name missing.
        """
        cons = self.create()
        cons.onecmd("create Binita")
        xv = (self.capt_out.getvalue())
        self.assertEqual("** class doesn't exist **\n", xv)

    @unittest.skipIf(db != 'db', "Testing DBstorage only")
    def test_create_db(self):
        cons = self.create()
        cons.onecmd("create State name=California")
        sto_res = storage.all("State")
        self.assertTrue(len(sto_res) > 0)
