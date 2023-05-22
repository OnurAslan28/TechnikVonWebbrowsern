import unittest
from util.request import dechunk


class ChunkTest(unittest.TestCase):
    def test_dechunk(self):
        chunked_response = bytes("4\r\nFros\r\n8\r\nted is n\r\nA\r\now chunked\r\n0\r\n\r\n", "utf-8")
        unchunked_response = dechunk(chunked_response).decode("utf-8")
        self.assertEqual("Frosted is now chunked", unchunked_response)


if __name__ == "__main__":
    test = ChunkTest()
    test.test_dechunk()
    print("Everything passed")
