import unittest

from APICodeLEIA import VirtualRegisterPool, Register, VirtualRegister

class Tests(unittest.TestCase):
    def test_pool(self):
        pool = VirtualRegisterPool()
        tmp0 = pool.new_register()
        self.assertEqual(str(tmp0), 'temp_0')
        tmp1 = pool.new_register()
        self.assertEqual(str(tmp1), 'temp_1')
        r1 = Register(1)
        r2 = Register(2)
        pool.set_reg_allocation({
            tmp0: r1,
            tmp1: r2
        })
        self.assertEqual(str(tmp0), 'temp_0')
        self.assertEqual(str(tmp1), 'temp_1')
        self.assertEqual(tmp0.get_alloced_loc(), r1)
        self.assertEqual(tmp1.get_alloced_loc(), r2)

if __name__ == '__main__':
    unittest.main()
