import unittest

from utils import *

class TestBlockType(unittest.TestCase):

    def test_block_to_block_type_heading(self):
        tests = [("# Heading with one #", BlockType.HEADING),
                ("## Heading with two #", BlockType.HEADING),
                ("### Heading with three #", BlockType.HEADING),
                ("#### Heading with four #", BlockType.HEADING),
                ("##### Heading with five #", BlockType.HEADING),
                ("###### Heading with six #", BlockType.HEADING),
                ("####### Not a heading", BlockType.PARAGRAPH),
        ]

        for test in tests:
            block_type =  block_to_block_type(test[0])
            self.assertEqual(block_type, test[1])

    def test_block_to_block_type_code(self):
        tests = [("```This is a code block```", BlockType.CODE),
                 ("```Not a code block", BlockType.PARAGRAPH),
                 ("Also not a clode block```", BlockType.PARAGRAPH),
                ]
                 
        for test in tests:
            block_type =  block_to_block_type(test[0])
            self.assertEqual(block_type, test[1])

    def test_block_to_block_type_quote(self):
        
        tests = [(">This is a quote block.", BlockType.QUOTE),
                 ("> This is another quote block.\n>over two lines", BlockType.QUOTE),
                 ("This is not a quote block", BlockType.PARAGRAPH),
                 ]
        
        for test in tests:
            block_type =  block_to_block_type(test[0])
            self.assertEqual(block_type, test[1])

    def test_block_to_block_type_ul(self):
        tests = [("- This is an unordered list.\n- Of three\n- items", BlockType.UNORDERED_LIST),
                 ("-This is not an unordered list.\n- Of three\n- items", BlockType.PARAGRAPH),
                 ]

        for test in tests:
            block_type =  block_to_block_type(test[0])
            self.assertEqual(block_type, test[1])

    def test_block_to_block_type_ol(self):
        tests = [("1. List item 1\n2. List item 2\n3. List item 3", BlockType.ORDERED_LIST),
                ("1. List item 1\n3. Out of order list item 2\n2. Out of order list item 3", BlockType.PARAGRAPH),
        ]

        for test in tests:
            block_type =  block_to_block_type(test[0])
            self.assertEqual(block_type, test[1])
    
    def test_block_to_block_type_p(self):
        test = """
                A plain old paragraph
                of multi-line text.
                Nothin to see here.
        """

        self.assertEqual(block_to_block_type(test), BlockType.PARAGRAPH)
