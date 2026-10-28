"""Replay a captured Xiaomi wake payload in a temporary unused advertising slot."""
import ctypes
import re
import socket
import struct
import sys
import time

def wake_fields(address):
    if not re.fullmatch(r'(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}', address):
        raise ValueError('Expected a Bluetooth MAC address')
    suffix = bytes.fromhex(address.replace(':', ''))[-3:][::-1]
    return {
        0x01: bytes([0x05]),
        0xFF: bytes([0x00, 0x01]),
        0x08: b'MI RC',
        0x02: bytes([0x12, 0x18]),
        0x0D: bytes([0x04, 0x05, 0x00]),
        0x0A: bytes([0x00]),
        0xFE: suffix,
    }


def raw_payload(address):
    return b''.join(bytes([len(value) + 1, kind]) + value for kind, value in wake_fields(address).items())




class ManagementError(RuntimeError):
    pass


def command(opcode, payload=b'', index=0):
    if opcode not in (0x0004, 0x003D, 0x003F, 0x0054, 0x0055):
        raise ValueError('This helper only supports controller info and advertising instances')
    with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI) as channel:
        address = ctypes.create_string_buffer(struct.pack('HHH', socket.AF_BLUETOOTH, 0xFFFF, 3))
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.bind(channel.fileno(), ctypes.byref(address), 6):
            raise OSError(ctypes.get_errno(), 'Cannot bind management socket')
        channel.settimeout(5)
        channel.send(struct.pack('<HHH', opcode, index, len(payload)) + payload)
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            packet = channel.recv(65535)
            if len(packet) < 9:
                continue
            event, controller, length = struct.unpack_from('<HHH', packet)
            if event not in (1, 2) or controller != index:
                continue
            response, status = struct.unpack_from('<HB', packet, 6)
            if response != opcode:
                continue
            if status:
                raise ManagementError(f'Command 0x{opcode:04x} failed with status 0x{status:02x}')
            if length < 3 or len(packet) < 6 + length:
                raise ManagementError('Incomplete management reply')
            return packet[9:6 + length]
        raise TimeoutError('No matching management reply within 5 seconds')


def features(index=0):
    data = command(0x003D, index=index)
    if len(data) < 8:
        raise ManagementError('Incomplete advertising features')
    flags, maximum, scan_maximum, slots, count = struct.unpack_from('<IBBBB', data)
    if len(data) < 8 + count or count > slots:
        raise ManagementError('Malformed advertising instance list')
    return maximum, slots, set(data[8:8 + count])


def advertise(address, seconds=10, index=0, *, connectable=False, cancel_event=None):
    if not 1 <= seconds <= 20:
        raise ValueError('Temporary advertising must be bounded to 1..20 seconds')
    before_info = command(0x0004, index=index)
    if len(before_info) < 17:
        raise ManagementError('Incomplete controller information')
    settings = int.from_bytes(before_info[13:17], 'little')
    if not connectable and settings & 2:
        raise RuntimeError('Global connectable mode is on; refusing a potentially connectable beacon')
    packet = raw_payload(address)
    maximum, slots, occupied = features(index)
    if len(packet) > maximum:
        raise RuntimeError('Wake payload exceeds advertising capacity')
    free = sorted(set(range(1, slots + 1)) - occupied)
    if not free:
        raise RuntimeError('No unused advertising slot; existing advertisements will not be replaced')
    instance = free[-1]
    print('Existing advertising slots:', sorted(occupied), '; temporary unused slot:', instance, flush=True)
    added = False
    try:
        flags = int(connectable) | (1 << 12) | (1 << 13) | (1 << 14)
        params = struct.pack('<BIHHIIb', instance, flags, 5, seconds, 0x20, 0x20, 0)
        response = command(0x0054, params, index)
        if len(response) != 4 or response[0] != instance:
            raise ManagementError('Unexpected advertising parameters acknowledgement')
        added = True
        if len(packet) > response[2]:
            raise RuntimeError('Wake payload exceeds per-instance advertising capacity')
        response = command(0x0055, bytes([instance, len(packet), 0]) + packet, index)
        if response != bytes([instance]):
            raise ManagementError('Unexpected advertising data acknowledgement')
        print('Captured wake payload added; connectable:', connectable, '; interval 20 ms', flush=True)
        if cancel_event is None:
            time.sleep(seconds)
        else:
            cancel_event.wait(seconds)
    finally:
        if added and instance in features(index)[2]:
            command(0x003F, bytes([instance]), index)
            print('Removed only the temporary advertising slot', flush=True)
    after_info = command(0x0004, index=index)
    if before_info[:6] != after_info[:6] or before_info[13:17] != after_info[13:17]:
        raise RuntimeError('Adapter address or shared settings changed unexpectedly')
    remaining = features(index)[2]
    if remaining != occupied:
        raise RuntimeError(f'Advertising slots changed unexpectedly: {sorted(remaining)}')
    print('Existing advertisements and public adapter address preserved', flush=True)



def main():
    import argparse
    parser = argparse.ArgumentParser(description='Experimental MiProjM05 wake sender; run on the Linux Bluetooth host')
    parser.add_argument('--target', required=True, help='Projector Bluetooth address, not its Wi-Fi address')
    parser.add_argument('--index', type=int, default=0, help='Bluetooth controller index (default: 0)')
    parser.add_argument('--seconds', type=int, default=20, help='Bounded transmission duration, 1..20 seconds')
    args = parser.parse_args()
    if not 0 <= args.index < 0xFFFF:
        parser.error('Controller index must be between 0 and 65534')
    if sys.platform != 'linux':
        parser.exit(1, 'Run the wake sender on the Linux Bluetooth host.\n')
    try:
        raw_payload(args.target)
        advertise(args.target, args.seconds, args.index, connectable=True)
    except (OSError, RuntimeError, ValueError) as error:
        parser.exit(1, f'Wake advertisement failed: {error}\n')


if __name__ == '__main__':
    main()
