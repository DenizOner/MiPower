import struct,unittest
from unittest.mock import patch
from tools import xiaomi_projector_wake as w

ADDRESS='AA:BB:CC:11:22:33'
INFO=bytes.fromhex('010203040506')+bytes(11)

class WakeTests(unittest.TestCase):
    def test_recorded_packet_layout_with_anonymized_address(self):
        self.assertEqual(w.raw_payload(ADDRESS).hex(),'02010503ff000106084d4920524303021218040d040500020a0004fe332211')
        self.assertEqual(len(w.raw_payload(ADDRESS)),31)
    def test_invalid_address_is_rejected(self):
        for value in ('','AA:BB:CC:11:22','AA:BB:CC:11:22:33:44','GG:BB:CC:11:22:33'):
            with self.subTest(value=value),self.assertRaises(ValueError):w.raw_payload(value)
    def test_no_slot_never_overwrites_existing_advertisements(self):
        with patch.object(w,'command',return_value=INFO) as cmd,patch.object(w,'features',return_value=(31,2,{1,2})):
            with self.assertRaisesRegex(RuntimeError,'No unused advertising slot'):w.advertise(ADDRESS,connectable=True)
            self.assertEqual([c.args[0] for c in cmd.call_args_list],[0x0004])
    def test_data_failure_removes_only_the_new_slot(self):
        def respond(opcode,payload=b'',index=0):
            if opcode==0x0004:return INFO
            if opcode==0x0054:return bytes([5,0,31,31])
            if opcode==0x0055:raise w.ManagementError('injected data failure')
            if opcode==0x003F:return b'\x05'
            raise AssertionError(hex(opcode))
        with patch.object(w,'command',side_effect=respond) as cmd,patch.object(w,'features',side_effect=[(31,5,{1}),(31,5,{1,5})]):
            with self.assertRaisesRegex(w.ManagementError,'injected'):w.advertise(ADDRESS,connectable=True)
            self.assertEqual(cmd.call_args_list[-1].args,(0x003F,b'\x05',0))
            params=cmd.call_args_list[1].args[1]
            slot,flags,duration,timeout,minimum,maximum,power=struct.unpack('<BIHHIIb',params)
            self.assertEqual((slot,timeout,minimum,maximum),(5,10,32,32))
            self.assertTrue(flags & 1)
    def test_success_restores_existing_slot_set_and_shared_state(self):
        def respond(opcode,payload=b'',index=0):
            return INFO if opcode==0x0004 else bytes([5,0,31,31]) if opcode==0x0054 else b'\x05'
        with patch.object(w,'command',side_effect=respond) as cmd,patch.object(w,'features',side_effect=[(31,5,{1}),(31,5,{1,5}),(31,5,{1})]),patch.object(w.time,'sleep'):
            w.advertise(ADDRESS,connectable=True)
            self.assertEqual([c.args[1] for c in cmd.call_args_list if c.args[0]==0x003F],[b'\x05'])
    def test_duration_is_bounded_before_any_controller_command(self):
        with patch.object(w,'command') as cmd:
            for seconds in (0,21,-1):
                with self.assertRaises(ValueError):w.advertise(ADDRESS,seconds,connectable=True)
            cmd.assert_not_called()

if __name__=='__main__':unittest.main()
