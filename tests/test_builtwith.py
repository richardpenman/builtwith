import builtwith
from pathlib import Path

import unittest


class TestBuiltwith(unittest.TestCase):
    def test_wordpress(self):
        p = Path(__file__).with_name("wordpress.html")
        html = p.open("r").read()
        b = builtwith.builtwith("", html=html)
        self.assertEqual(
            b,
            {
                "blogs": ["PHP", "WordPress"],
                "cms": ["WordPress"],
                "ecommerce": ["WooCommerce"],
                "javascript-frameworks": ["jQuery"],
                "programming-languages": ["PHP"],
            },
        )


if __name__ == "__main__":
    unittest.main()
