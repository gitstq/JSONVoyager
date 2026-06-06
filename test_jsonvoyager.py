#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONVoyager Test Suite
"""

import unittest
import json
import os
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jsonvoyager import JSONVoyager, Colors


class TestJSONVoyager(unittest.TestCase):
    """Test cases for JSONVoyager"""

    def setUp(self):
        self.app = JSONVoyager()
        self.sample_data = {
            "name": "test",
            "count": 42,
            "active": True,
            "metadata": None,
            "items": [1, 2, 3],
            "user": {"name": "Alice", "age": 30}
        }

    def test_load_json_from_string(self):
        """Test loading JSON from string"""
        success, msg = self.app.load_json('{"test": true}')
        self.assertTrue(success)
        self.assertEqual(self.app.data, {"test": True})

    def test_load_json_invalid(self):
        """Test loading invalid JSON"""
        success, msg = self.app.load_json('not json')
        self.assertFalse(success)
        self.assertIn("Invalid JSON", msg)

    def test_query_simple(self):
        """Test simple query"""
        self.app.data = self.sample_data
        result = self.app.query("name")
        self.assertEqual(result, "test")

    def test_query_nested(self):
        """Test nested query"""
        self.app.data = self.sample_data
        result = self.app.query("user.name")
        self.assertEqual(result, "Alice")

    def test_query_array(self):
        """Test array query"""
        self.app.data = self.sample_data
        result = self.app.query("items.1")
        self.assertEqual(result, 2)

    def test_query_not_found(self):
        """Test query not found"""
        self.app.data = self.sample_data
        result = self.app.query("nonexistent.path")
        self.assertIsNone(result)

    def test_flatten(self):
        """Test flatten function"""
        self.app.data = self.sample_data
        items = self.app._flatten(self.app.data)
        paths = [".".join(str(p) for p in path) for path, _ in items]
        self.assertIn("name", paths)
        self.assertIn("user.name", paths)
        self.assertIn("items.0", paths)

    def test_stats(self):
        """Test statistics"""
        self.app.data = self.sample_data
        stats = self.app._get_stats()
        self.assertEqual(stats["keys"], 8)  # name, count, active, metadata, items, user, name, age
        self.assertEqual(stats["strings"], 2)
        self.assertEqual(stats["numbers"], 5)  # count, items(1,2,3), age
        self.assertEqual(stats["booleans"], 1)
        self.assertEqual(stats["nulls"], 1)

    def test_colorize_json(self):
        """Test colorize output"""
        self.app.data = {"test": "value"}
        output = self.app._colorize_json(self.app.data)
        self.assertIn("test", output)
        self.assertIn(Colors.CYAN, output)

    def test_format_value(self):
        """Test value formatting"""
        self.assertIn("test", self.app._format_value("test"))
        self.assertIn("42", self.app._format_value(42))
        self.assertIn("true", self.app._format_value(True))
        self.assertIn("null", self.app._format_value(None))

    def test_export_json(self):
        """Test JSON export"""
        self.app.data = self.sample_data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        try:
            success, msg = self.app.export("json", temp_path)
            self.assertTrue(success)
            with open(temp_path, 'r') as f:
                loaded = json.load(f)
            self.assertEqual(loaded["name"], "test")
        finally:
            os.unlink(temp_path)

    def test_export_csv(self):
        """Test CSV export"""
        self.app.data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        success, msg = self.app.export("csv")
        self.assertTrue(success)

    def test_get_type_name(self):
        """Test type name detection"""
        self.assertIn("object", self.app._get_type_name({}))
        self.assertIn("array", self.app._get_type_name([]))
        self.assertIn("string", self.app._get_type_name("test"))
        self.assertIn("integer", self.app._get_type_name(42))
        self.assertIn("boolean", self.app._get_type_name(True))
        self.assertIn("null", self.app._get_type_name(None))

    def test_truncate(self):
        """Test text truncation"""
        self.assertEqual(self.app._truncate("hello", 10), "hello")
        self.assertEqual(self.app._truncate("hello world", 8), "hello...")


class TestIntegration(unittest.TestCase):
    """Integration tests"""

    def test_full_workflow(self):
        """Test complete workflow"""
        app = JSONVoyager()

        # Load JSON
        success, _ = app.load_json('{"users": [{"name": "Alice"}, {"name": "Bob"}]}')
        self.assertTrue(success)

        # Query
        result = app.query("users.0.name")
        self.assertEqual(result, "Alice")

        # Stats
        stats = app._get_stats()
        self.assertGreater(stats["keys"], 0)

        # Flatten
        items = app._flatten(app.data)
        self.assertTrue(len(items) > 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
