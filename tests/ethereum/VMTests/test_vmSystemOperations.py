"""DO NOT MODIFY: Test `/Users/dc/projects/manticore/tests/ethereum/tests/VMTests/vmSystemOperations` generated with make_VMTests.py"""
import unittest
from binascii import unhexlify

import rlp
import sha3
from rlp.sedes import CountableList, BigEndianInt, Binary

from manticore.core.smtlib import ConstraintSet
from manticore.core.smtlib.visitors import to_constant
from manticore.platforms import evm


class Log(rlp.Serializable):
    fields = [
        ("address", Binary.fixed_length(20, allow_empty=True)),
        ("topics", CountableList(BigEndianInt(32))),
        ("data", Binary()),
    ]


class EVMTest_vmSystemOperations(unittest.TestCase):
    # https://nose.readthedocs.io/en/latest/doc_tests/test_multiprocess/multiprocess.html#controlling-distribution
    _multiprocess_can_split_ = True
    # https://docs.python.org/3.7/library/unittest.html#unittest.TestCase.maxDiff
    maxDiff = None

    SAVED_DEFAULT_FORK = evm.DEFAULT_FORK

    @classmethod
    def setUpClass(cls):
        evm.DEFAULT_FORK = "frontier"

    @classmethod
    def tearDownClass(cls):
        evm.DEFAULT_FORK = cls.SAVED_DEFAULT_FORK

    def test_return0(self):
        """
        Textcase taken from https://github.com/ethereum/tests
        File: return0.json
        sha256sum: 0317578f90e3f451ed9d51947d1303493022caa568aa4927eb113e1c9a0183e6
        Code:     PUSH1 0x37
                  PUSH1 0x0
                  MSTORE8
                  PUSH1 0x0
                  MLOAD
                  PUSH1 0x0
                  SSTORE
                  PUSH1 0x1
                  PUSH1 0x0
                  RETURN
        """

        constraints = ConstraintSet()
        world = evm.EVMWorld(
            constraints,
            blocknumber=0,
            timestamp=1,
            difficulty=256,
            coinbase=244687034288125203496486448490407391986876152250,
            gaslimit=10000000,
        )

        bytecode = unhexlify("603760005360005160005560016000f3")
        world.create_account(
            address=0xCD1722F3947DEF4CF144679DA39C4C32BDC35681, balance=23, code=bytecode, nonce=0
        )
        address = 0xCD1722F3947DEF4CF144679DA39C4C32BDC35681
        price = 0x5AF3107A4000
        data = unhexlify("aa")
        caller = 0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6
        value = 23
        gas = 100000

        # open a fake tx, no funds send
        world._open_transaction("CALL", address, price, data, caller, value, gas=gas)

        # This variable might seem redundant in some tests - don't forget it is auto generated
        # and there are cases in which we need it ;)
        result = None
        returndata = b""
        try:
            while True:
                world.current_vm.execute()
        except evm.EndTx as e:
            result = e.result
            if result in ("RETURN", "REVERT"):
                returndata = to_constant(e.data)
        except evm.StartTx as e:
            self.fail("This tests should not initiate an internal tx (no CALLs allowed)")
        # Add pos checks for account 0xcd1722f3947def4cf144679da39c4c32bdc35681
        # check nonce, balance, code
        self.assertEqual(world.get_nonce(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681), 0)
        self.assertEqual(
            to_constant(world.get_balance(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681)), 23
        )
        self.assertEqual(
            world.get_code(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681),
            unhexlify("603760005360005160005560016000f3"),
        )
        # check storage
        self.assertEqual(
            to_constant(world.get_storage_data(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681, 0x00)),
            0x3700000000000000000000000000000000000000000000000000000000000000,
        )
        # check outs
        self.assertEqual(returndata, unhexlify("37"))
        # check logs
        logs = [
            Log(unhexlify("{:040x}".format(l.address)), l.topics, to_constant(l.memlog))
            for l in world.logs
        ]
        data = rlp.encode(logs)
        self.assertEqual(
            sha3.keccak_256(data).hexdigest(),
            "1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
        )

        # test used gas
        self.assertEqual(to_constant(world.current_vm.gas), 79973)

    def test_return1(self):
        """
        Textcase taken from https://github.com/ethereum/tests
        File: return1.json
        sha256sum: 8bb16dfbc95077f7abc51d07cdba90b310b680750f22ad7bd5aaa1b4bda98d08
        Code:     PUSH1 0x37
                  PUSH1 0x0
                  MSTORE8
                  PUSH1 0x0
                  MLOAD
                  PUSH1 0x0
                  SSTORE
                  PUSH1 0x2
                  PUSH1 0x0
                  RETURN
        """

        constraints = ConstraintSet()
        world = evm.EVMWorld(
            constraints,
            blocknumber=0,
            timestamp=1,
            difficulty=256,
            coinbase=244687034288125203496486448490407391986876152250,
            gaslimit=10000000,
        )

        bytecode = unhexlify("603760005360005160005560026000f3")
        world.create_account(
            address=0xCD1722F3947DEF4CF144679DA39C4C32BDC35681, balance=23, code=bytecode, nonce=0
        )
        address = 0xCD1722F3947DEF4CF144679DA39C4C32BDC35681
        price = 0x5AF3107A4000
        data = unhexlify("aa")
        caller = 0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6
        value = 23
        gas = 100000

        # open a fake tx, no funds send
        world._open_transaction("CALL", address, price, data, caller, value, gas=gas)

        # This variable might seem redundant in some tests - don't forget it is auto generated
        # and there are cases in which we need it ;)
        result = None
        returndata = b""
        try:
            while True:
                world.current_vm.execute()
        except evm.EndTx as e:
            result = e.result
            if result in ("RETURN", "REVERT"):
                returndata = to_constant(e.data)
        except evm.StartTx as e:
            self.fail("This tests should not initiate an internal tx (no CALLs allowed)")
        # Add pos checks for account 0xcd1722f3947def4cf144679da39c4c32bdc35681
        # check nonce, balance, code
        self.assertEqual(world.get_nonce(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681), 0)
        self.assertEqual(
            to_constant(world.get_balance(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681)), 23
        )
        self.assertEqual(
            world.get_code(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681),
            unhexlify("603760005360005160005560026000f3"),
        )
        # check storage
        self.assertEqual(
            to_constant(world.get_storage_data(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681, 0x00)),
            0x3700000000000000000000000000000000000000000000000000000000000000,
        )
        # check outs
        self.assertEqual(returndata, unhexlify("3700"))
        # check logs
        logs = [
            Log(unhexlify("{:040x}".format(l.address)), l.topics, to_constant(l.memlog))
            for l in world.logs
        ]
        data = rlp.encode(logs)
        self.assertEqual(
            sha3.keccak_256(data).hexdigest(),
            "1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
        )

        # test used gas
        self.assertEqual(to_constant(world.current_vm.gas), 79973)

    def test_suicideSendEtherToMe(self):
        """
        Textcase taken from https://github.com/ethereum/tests
        File: suicideSendEtherToMe.json
        sha256sum: 2ff81b7cdd2b1dd1f69c4bc9ba0b7369b4c624291d5021fbe638ce130a18df26
        Code:     ADDRESS
                  SELFDESTRUCT
        """

        constraints = ConstraintSet()
        world = evm.EVMWorld(
            constraints,
            blocknumber=0,
            timestamp=1,
            difficulty=256,
            coinbase=244687034288125203496486448490407391986876152250,
            gaslimit=10000000,
        )

        bytecode = unhexlify("30ff")
        world.create_account(
            address=0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6,
            balance=100000000000000000000000,
            code=bytecode,
            nonce=0,
        )
        bytecode = unhexlify("6000355415600957005b60203560003555")
        world.create_account(
            address=0xCD1722F3947DEF4CF144679DA39C4C32BDC35681, balance=23, code=bytecode, nonce=0
        )
        address = 0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6
        price = 0x5AF3107A4000
        data = ""
        caller = 0xCD1722F3947DEF4CF144679DA39C4C32BDC35681
        value = 100000
        gas = 1000

        # open a fake tx, no funds send
        world._open_transaction("CALL", address, price, data, caller, value, gas=gas)

        # This variable might seem redundant in some tests - don't forget it is auto generated
        # and there are cases in which we need it ;)
        result = None
        returndata = b""
        try:
            while True:
                world.current_vm.execute()
        except evm.EndTx as e:
            result = e.result
            if result in ("RETURN", "REVERT"):
                returndata = to_constant(e.data)
        except evm.StartTx as e:
            self.fail("This tests should not initiate an internal tx (no CALLs allowed)")
        # Add pos checks for account 0xcd1722f3947def4cf144679da39c4c32bdc35681
        # check nonce, balance, code
        self.assertEqual(world.get_nonce(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681), 0)
        self.assertEqual(
            to_constant(world.get_balance(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681)), 23
        )
        self.assertEqual(
            world.get_code(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681),
            unhexlify("6000355415600957005b60203560003555"),
        )
        # check outs
        self.assertEqual(returndata, unhexlify(""))
        # check logs
        logs = [
            Log(unhexlify("{:040x}".format(l.address)), l.topics, to_constant(l.memlog))
            for l in world.logs
        ]
        data = rlp.encode(logs)
        self.assertEqual(
            sha3.keccak_256(data).hexdigest(),
            "1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
        )

        # test used gas
        self.assertEqual(to_constant(world.current_vm.gas), 998)

    def test_TestNameRegistrator(self):
        """
        Textcase taken from https://github.com/ethereum/tests
        File: TestNameRegistrator.json
        sha256sum: dd000f5977416de19410170b8a7acb5060011594fd97c81f307f015cd5bdd51e
        Code:     PUSH1 0x0
                  CALLDATALOAD
                  SLOAD
                  ISZERO
                  PUSH1 0x9
                  JUMPI
                  STOP
                  JUMPDEST
                  PUSH1 0x20
                  CALLDATALOAD
                  PUSH1 0x0
                  CALLDATALOAD
                  SSTORE
        """

        constraints = ConstraintSet()
        world = evm.EVMWorld(
            constraints,
            blocknumber=0,
            timestamp=1,
            difficulty=256,
            coinbase=244687034288125203496486448490407391986876152250,
            gaslimit=1000000,
        )

        bytecode = unhexlify("6000355415600957005b60203560003555")
        world.create_account(
            address=0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6,
            balance=100000000000000000000000,
            code=bytecode,
            nonce=0,
        )
        address = 0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6
        price = 0x5AF3107A4000
        data = unhexlify(
            "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffafffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa"
        )
        caller = 0xCD1722F3947DEF4CF144679DA39C4C32BDC35681
        value = 1000000000000000000
        gas = 100000

        # open a fake tx, no funds send
        world._open_transaction("CALL", address, price, data, caller, value, gas=gas)

        # This variable might seem redundant in some tests - don't forget it is auto generated
        # and there are cases in which we need it ;)
        result = None
        returndata = b""
        try:
            while True:
                world.current_vm.execute()
        except evm.EndTx as e:
            result = e.result
            if result in ("RETURN", "REVERT"):
                returndata = to_constant(e.data)
        except evm.StartTx as e:
            self.fail("This tests should not initiate an internal tx (no CALLs allowed)")
        # Add pos checks for account 0xf572e5295c57f15886f9b263e2f6d2d6c7b5ec6
        # check nonce, balance, code
        self.assertEqual(world.get_nonce(0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6), 0)
        self.assertEqual(
            to_constant(world.get_balance(0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6)),
            100000000000000000000000,
        )
        self.assertEqual(
            world.get_code(0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6),
            unhexlify("6000355415600957005b60203560003555"),
        )
        # check storage
        self.assertEqual(
            to_constant(
                world.get_storage_data(
                    0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6,
                    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA,
                )
            ),
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA,
        )
        # check outs
        self.assertEqual(returndata, unhexlify(""))
        # check logs
        logs = [
            Log(unhexlify("{:040x}".format(l.address)), l.topics, to_constant(l.memlog))
            for l in world.logs
        ]
        data = rlp.encode(logs)
        self.assertEqual(
            sha3.keccak_256(data).hexdigest(),
            "1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
        )

        # test used gas
        self.assertEqual(to_constant(world.current_vm.gas), 79915)

    def test_suicideNotExistingAccount(self):
        """
        Textcase taken from https://github.com/ethereum/tests
        File: suicideNotExistingAccount.json
        sha256sum: e2cb030ec446c6acca6c87a741d254ededf0713f3147b6e5e725d6795b4b9fea
        Code:     PUSH20 0xaa1722f3947def4cf144679da39c4c32bdc35681
                  SELFDESTRUCT
        """

        constraints = ConstraintSet()
        world = evm.EVMWorld(
            constraints,
            blocknumber=0,
            timestamp=1,
            difficulty=256,
            coinbase=244687034288125203496486448490407391986876152250,
            gaslimit=10000000,
        )

        bytecode = unhexlify("73aa1722f3947def4cf144679da39c4c32bdc35681ff")
        world.create_account(
            address=0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6,
            balance=100000000000000000000000,
            code=bytecode,
            nonce=0,
        )
        bytecode = unhexlify("6000355415600957005b60203560003555")
        world.create_account(
            address=0xCD1722F3947DEF4CF144679DA39C4C32BDC35681, balance=23, code=bytecode, nonce=0
        )
        address = 0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6
        price = 0x5AF3107A4000
        data = ""
        caller = 0xCD1722F3947DEF4CF144679DA39C4C32BDC35681
        value = 100000
        gas = 1000

        # open a fake tx, no funds send
        world._open_transaction("CALL", address, price, data, caller, value, gas=gas)

        # This variable might seem redundant in some tests - don't forget it is auto generated
        # and there are cases in which we need it ;)
        result = None
        returndata = b""
        try:
            while True:
                world.current_vm.execute()
        except evm.EndTx as e:
            result = e.result
            if result in ("RETURN", "REVERT"):
                returndata = to_constant(e.data)
        except evm.StartTx as e:
            self.fail("This tests should not initiate an internal tx (no CALLs allowed)")
        # Add pos checks for account 0xaa1722f3947def4cf144679da39c4c32bdc35681
        # check nonce, balance, code
        self.assertEqual(world.get_nonce(0xAA1722F3947DEF4CF144679DA39C4C32BDC35681), 0)
        self.assertEqual(
            to_constant(world.get_balance(0xAA1722F3947DEF4CF144679DA39C4C32BDC35681)),
            100000000000000000000000,
        )
        self.assertEqual(world.get_code(0xAA1722F3947DEF4CF144679DA39C4C32BDC35681), unhexlify(""))
        # Add pos checks for account 0xcd1722f3947def4cf144679da39c4c32bdc35681
        # check nonce, balance, code
        self.assertEqual(world.get_nonce(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681), 0)
        self.assertEqual(
            to_constant(world.get_balance(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681)), 23
        )
        self.assertEqual(
            world.get_code(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681),
            unhexlify("6000355415600957005b60203560003555"),
        )
        # check outs
        self.assertEqual(returndata, unhexlify(""))
        # check logs
        logs = [
            Log(unhexlify("{:040x}".format(l.address)), l.topics, to_constant(l.memlog))
            for l in world.logs
        ]
        data = rlp.encode(logs)
        self.assertEqual(
            sha3.keccak_256(data).hexdigest(),
            "1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
        )

        # test used gas
        self.assertEqual(to_constant(world.current_vm.gas), 997)

    def test_return2(self):
        """
        Textcase taken from https://github.com/ethereum/tests
        File: return2.json
        sha256sum: 25972361a5871003f44467255a656b9e7ba3762a5cfe02b56a0197318d375b9a
        Code:     PUSH1 0x37
                  PUSH1 0x0
                  MSTORE8
                  PUSH1 0x0
                  MLOAD
                  PUSH1 0x0
                  SSTORE
                  PUSH1 0x21
                  PUSH1 0x0
                  RETURN
        """

        constraints = ConstraintSet()
        world = evm.EVMWorld(
            constraints,
            blocknumber=0,
            timestamp=1,
            difficulty=256,
            coinbase=244687034288125203496486448490407391986876152250,
            gaslimit=10000000,
        )

        bytecode = unhexlify("603760005360005160005560216000f3")
        world.create_account(
            address=0xCD1722F3947DEF4CF144679DA39C4C32BDC35681, balance=23, code=bytecode, nonce=0
        )
        address = 0xCD1722F3947DEF4CF144679DA39C4C32BDC35681
        price = 0x5AF3107A4000
        data = unhexlify("aa")
        caller = 0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6
        value = 23
        gas = 100000

        # open a fake tx, no funds send
        world._open_transaction("CALL", address, price, data, caller, value, gas=gas)

        # This variable might seem redundant in some tests - don't forget it is auto generated
        # and there are cases in which we need it ;)
        result = None
        returndata = b""
        try:
            while True:
                world.current_vm.execute()
        except evm.EndTx as e:
            result = e.result
            if result in ("RETURN", "REVERT"):
                returndata = to_constant(e.data)
        except evm.StartTx as e:
            self.fail("This tests should not initiate an internal tx (no CALLs allowed)")
        # Add pos checks for account 0xcd1722f3947def4cf144679da39c4c32bdc35681
        # check nonce, balance, code
        self.assertEqual(world.get_nonce(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681), 0)
        self.assertEqual(
            to_constant(world.get_balance(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681)), 23
        )
        self.assertEqual(
            world.get_code(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681),
            unhexlify("603760005360005160005560216000f3"),
        )
        # check storage
        self.assertEqual(
            to_constant(world.get_storage_data(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681, 0x00)),
            0x3700000000000000000000000000000000000000000000000000000000000000,
        )
        # check outs
        self.assertEqual(
            returndata,
            unhexlify("370000000000000000000000000000000000000000000000000000000000000000"),
        )
        # check logs
        logs = [
            Log(unhexlify("{:040x}".format(l.address)), l.topics, to_constant(l.memlog))
            for l in world.logs
        ]
        data = rlp.encode(logs)
        self.assertEqual(
            sha3.keccak_256(data).hexdigest(),
            "1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
        )

        # test used gas
        self.assertEqual(to_constant(world.current_vm.gas), 79970)

    def test_suicide0(self):
        """
        Textcase taken from https://github.com/ethereum/tests
        File: suicide0.json
        sha256sum: b6a8903cf90bc139d273b9408ec6aad5832bc94a2f87ee21cc018a4f1aea2fd8
        Code:     CALLER
                  SELFDESTRUCT
        """

        constraints = ConstraintSet()
        world = evm.EVMWorld(
            constraints,
            blocknumber=0,
            timestamp=1,
            difficulty=256,
            coinbase=244687034288125203496486448490407391986876152250,
            gaslimit=10000000,
        )

        bytecode = unhexlify("33ff")
        world.create_account(
            address=0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6,
            balance=100000000000000000000000,
            code=bytecode,
            nonce=0,
        )
        bytecode = unhexlify("6000355415600957005b60203560003555")
        world.create_account(
            address=0xCD1722F3947DEF4CF144679DA39C4C32BDC35681, balance=23, code=bytecode, nonce=0
        )
        address = 0xF572E5295C57F15886F9B263E2F6D2D6C7B5EC6
        price = 0x5AF3107A4000
        data = ""
        caller = 0xCD1722F3947DEF4CF144679DA39C4C32BDC35681
        value = 100000
        gas = 1000

        # open a fake tx, no funds send
        world._open_transaction("CALL", address, price, data, caller, value, gas=gas)

        # This variable might seem redundant in some tests - don't forget it is auto generated
        # and there are cases in which we need it ;)
        result = None
        returndata = b""
        try:
            while True:
                world.current_vm.execute()
        except evm.EndTx as e:
            result = e.result
            if result in ("RETURN", "REVERT"):
                returndata = to_constant(e.data)
        except evm.StartTx as e:
            self.fail("This tests should not initiate an internal tx (no CALLs allowed)")
        # Add pos checks for account 0xcd1722f3947def4cf144679da39c4c32bdc35681
        # check nonce, balance, code
        self.assertEqual(world.get_nonce(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681), 0)
        self.assertEqual(
            to_constant(world.get_balance(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681)),
            100000000000000000000023,
        )
        self.assertEqual(
            world.get_code(0xCD1722F3947DEF4CF144679DA39C4C32BDC35681),
            unhexlify("6000355415600957005b60203560003555"),
        )
        # check outs
        self.assertEqual(returndata, unhexlify(""))
        # check logs
        logs = [
            Log(unhexlify("{:040x}".format(l.address)), l.topics, to_constant(l.memlog))
            for l in world.logs
        ]
        data = rlp.encode(logs)
        self.assertEqual(
            sha3.keccak_256(data).hexdigest(),
            "1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
        )

        # test used gas
        self.assertEqual(to_constant(world.current_vm.gas), 998)


if __name__ == "__main__":
    unittest.main()
