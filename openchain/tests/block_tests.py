from unittest import TestCase

from openchain.models.exception import BlockInvalidException
from openchain.models.factory import BlockchainFactory
from openchain.models.transaction import Transaction

from openchain.models.block import Block
from openchain.tests import TEST_PRIVATE_KEY


class BlockTestCase(TestCase):

    def setUp(self):
        Block.objects.delete_all()
        Transaction.objects.delete_all()

    def test_block_creation(self):
        block = Block()
        with self.assertRaises(BlockInvalidException):
            block.save()

    def test_block_generation(self):
        block = Block()
        block.generate()

        self.assertTrue(block.is_valid)
        self.assertNotEqual(block.nonce, 0)

        Block.objects.delete_all()

    def test_block_transactions(self):
        transaction_01 = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        transaction_01.signing(TEST_PRIVATE_KEY.to_string().hex())
        transaction_01.save()

        transaction_02 = Transaction(in_address='addr3', out_address='addr4', amount=20.50)
        transaction_02.signing(TEST_PRIVATE_KEY.to_string().hex())
        transaction_02.save()

        block_01 = Block(transactions=[transaction_01.__dict__,
                                       transaction_02.__dict__])
        block_01.generate()
        block_01.save()

        self.assertTrue(block_01.is_valid)
        self.assertNotEqual(block_01.nonce, 0)

        transaction_03 = Transaction(in_address='addr1', out_address='addr3', amount=7.00)
        transaction_03.signing(TEST_PRIVATE_KEY.to_string().hex())
        transaction_03.save()

        transaction_04 = Transaction(in_address='addr4', out_address='addr2', amount=5.50)
        transaction_04.signing(TEST_PRIVATE_KEY.to_string().hex())
        transaction_04.save()

        transaction_05 = Transaction(in_address='addr1', out_address='addr3', amount=2.30)
        transaction_05.signing(TEST_PRIVATE_KEY.to_string().hex())
        transaction_05.save()

        block_02 = Block(block_01.data_hash, transactions=[transaction_03.__dict__,
                                                           transaction_04.__dict__,
                                                           transaction_05.__dict__])
        block_02.generate()
        block_02.save()

        self.assertTrue(block_02.is_valid)
        self.assertNotEqual(block_02.nonce, 0)

        blockchain = BlockchainFactory.build_blockchain(Block.objects.get())
        self.assertEqual(len(blockchain.block_tree), 2)

        Block.objects.delete_all()
        Transaction.objects.delete_all()
