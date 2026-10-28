# MiProjM05: troubleshooting wake from standby

Use this guide if a Xiaomi Mi Smart Compact Projector works with a Bluetooth
HID remote while awake, wakes immediately after screen-off, but becomes
unreachable after several minutes of standby. A plain Bluetooth pairing
request may not solve this case.

**Scope:** this was verified on one `MiProjM05` running Android TV 9, with an
Ubuntu host, BlueZ 5.72 and Linux 7.0. Other models and firmware are unverified.
Sharing a physical remote model with a Mi Box does not establish compatibility.

**What this PR provides:** an opt-in Linux wake sender,
`tools/xiaomi_projector_wake.py`, and the findings below. The normal MiPower
switch does not automatically use this sender. This is not a complete HID
remote installer: it does not register a keyboard profile, provide a pairing
agent, enroll a host into the projector's wake list, or install an MQTT bridge.

## 1. Check that this is the same problem

The investigated setup had these symptoms:

- A Linux host already acted as a working **Classic HID** remote.
- The HID Sleep command turned the screen off. Wake worked while the Bluetooth
  connection remained active.
- After several minutes, Bluetooth disconnected and the projector's network
  control became unavailable. Another HID Wake could no longer reach it.
- The original Xiaomi RC still powered it on.
- A direct BlueZ `Pair` call on the existing Classic bond returned
  `AlreadyExists`. Replaying the captured advertisement before the host was
  recognized as a wake remote also failed, including at a 20 ms interval.

First prove that your HID remote works with the projector awake. If it cannot
pair, connect or deliver input, fix that prerequisite separately. Advertising
`MI RC` alone does not create a HID remote.

## 2. Identify the addresses before changing anything

These values have different jobs:

| Value | Purpose |
| --- | --- |
| Linux host adapter's public Bluetooth MAC | Sender identity; the address the tested projector enrolled as a wake remote |
| Projector's Bluetooth MAC | The sender's `--target`; used to construct the target-specific packet bytes |
| Original Xiaomi remote's Bluetooth MAC | A reference when reading logs; do not clone it |
| Projector's Wi-Fi/Ethernet IP or MAC | Network diagnostics; not the sender's Bluetooth target |
| Host device name / controller alias | Used by the tested firmware's remote classification; not a new MAC address |
| HID UUIDs and VID/PID | Service/product identity; changing them is not the same as changing a MAC |

From an existing checkout containing this PR, inspect the host without issuing
pairing or reset commands:

```sh
bluetoothctl --version
bluetoothctl list
bluetoothctl show
bluetoothctl info PROJECTOR_BLUETOOTH_MAC
python3 tools/xiaomi_projector_wake.py --help
```

Replace uppercase placeholders with your own values. Record the current alias,
selected adapter, HID-emulator configuration and existing pairing state. For
multiple controllers, match the sender's `--index` to the actual `hciN` device;
it is independent of a previous interactive `bluetoothctl select` command.

The verified controller advertised with a public source address. The helper
does not disable Bluetooth privacy or force an over-the-air address mode.
A public address in `bluetoothctl show` does not by itself prove that every
advertisement uses that address; private-address configurations are unverified
here. Keep existing shared-adapter privacy settings rather than changing them
as a blind troubleshooting step.

Preserve an existing working bond. In particular, `bluetoothctl pair` is not a
read-only wake probe: the [BlueZ 5.72 manual](https://raw.githubusercontent.com/bluez/bluez/5.72/client/bluetoothctl.rst)
describes removing an existing pairing before pairing again. This PR checks
fresh target-specific state and skips `pair` for paired or unknown targets.
Do not delete the host's Bluetooth key database or remove unrelated accessories.

## 3. Let the projector recognize the existing HID host

On the inspected firmware, `BleRemoteService` recognizes wake remotes through
Xiaomi VID/PID checks **or** accepted device-name prefixes, including `MI RC`.
It maintains a separate `rc_macaddr` wake-address list.

The successful host name was **`MI RC HA Projector`**. The host kept its public
MAC, existing bond, Linux VID/PID and standard HID service UUIDs. It did not
impersonate the original remote's address or copy Xiaomi product IDs.

1. Update the name in your existing HID emulator's configuration if it manages
   the adapter alias. Otherwise it may overwrite a one-off alias change later.
   The controller alias is shared by every application using that adapter.
2. For a manual alias change, select the intended controller in `bluetoothctl`.
   These are **interactive bluetoothctl commands**, not a shell script:

   ```text
   list
   select HOST_ADAPTER_BLUETOOTH_MAC
   show
   system-alias "MI RC HA Projector"
   show
   quit
   ```

3. Keep the original Xiaomi remote paired. With the projector awake, open
   **Remotes & accessories** and its accessory search again, so the projector
   can refresh its cached name for the existing host. Use your HID emulator's
   bounded discovery window if required, then close that window. In the
   verified setup, rediscovery updated the name without removing the bond or
   pairing again.
4. Reconnect the existing Classic HID remote. If the projector still displays
   the old name, resolve that before interpreting another wake test.
5. In the verified Classic-HID setup, the emulator's **own continuous BLE
   advertisement was disabled**; its Classic HID profile remained registered.
   This avoided advertising a second LE pairing route during classification.
   Configure this in the emulator, not by clearing all advertisements on a
   shared controller. Do not apply this step to a remote that depends on LE
   HID instead of Classic HID.

The successful configuration combined recognition of the host address with a
public-address `ADV_IND` packet at 20 ms and no continuous advertisement from
our emulator. Renaming alone is not claimed to be sufficient on every firmware.

### Optional: confirm enrollment in the firmware log

If ADB is already enabled and authorized for diagnosis, inspect the projector
log. `PROJECTOR_IP:5555` below assumes an already connected, authorized ADB
session; enabling ADB is not required for ordinary use of the wake sender.

```sh
adb -s PROJECTOR_IP:5555 shell logcat -d -v time -s BleRemoteService
```

The successful run contained the following sequence (addresses anonymized):

```text
checkXiaomiRcName:MI RC HA Projector
compare rc name ok!
isRc,checkPidAndVid:true
setWakeUpRcAddr: HOST_ADAPTER_BLUETOOTH_MAC idx: 2
saveWakeUpRcAddr, saveToEnv=true,cacheNeedUpdate=true
wakeUpTotal: ORIGINAL_REMOTE_BLUETOOTH_MAC;HOST_ADAPTER_BLUETOOTH_MAC;
```

This confirms that this firmware recognized the host and saved both addresses.
A missing log line is not conclusive by itself: logging, buffering and firmware
may differ. Do not manually overwrite bootloader environment values to force
an enrollment. Disable temporary ADB access again when diagnosis is finished.

## 4. Test one complete standby/wake cycle

Run on the **Linux Bluetooth host**, not automatically inside the HA container.
The sender needs `CAP_NET_ADMIN` (normally root), support for advertising
instances and the extended advertising-parameter management command, and an
unused advertising instance.

1. While the projector is awake, verify input from the existing HID host.
2. Use the HID **Sleep** command to turn the screen off. Repeated Power presses
   can instead confirm full shutdown; that is a different test. Full-shutdown
   wake was not separately revalidated with the final configuration.
3. Wait until the existing Bluetooth connection has actually dropped and the
   projector's ordinary network control is unavailable. Immediate wake only
   tests shallow sleep. In our runs, this transition took several minutes;
   do not assume a fixed delay applies to every device.
4. Do not press the physical remote during the test. Send one bounded packet
   burst, replacing the example address with the projector's **Bluetooth** MAC:

   ```sh
   sudo python3 tools/xiaomi_projector_wake.py \
     --target AA:BB:CC:11:22:33 --index 0 --seconds 20
   ```

5. Allow up to 90 seconds from the wake request for startup and independently
   check the screen and your HA power-state entity. If it does not return,
   record the failure rather than treating a zero exit status as power-on.

The helper uses legacy connectable undirected advertising (`ADV_IND`) at
20 ms, preserves the host identity, bounds transmission to 1–20 seconds,
and checks shared state before/after. It does not reset the adapter or load
keys. Coordinate access: concurrent sender processes or other advertising
reconfiguration during transmission are unsupported.

Expected helper output includes:

```text
Existing advertising slots: [...] ; temporary unused slot: N
Captured wake payload added; connectable: True ; interval 20 ms
Existing advertisements and public adapter address preserved
```

A zero exit code confirms sender completion and host checks, **not** that the
projector received the signal or powered on. The script does not wait for the
projector's network or display.

## 5. Connect a working sender to Home Assistant

The verified deployment used a separate host service for Classic HID input and
wake advertisements, with MQTT commands from HA. HA and its shared Bluetooth
service did not need a restart for those tests; the HA container did not need
additional controller-management privileges.

This PR does **not** include that service. The following is an integration
pattern for an **already implemented** bridge, not an installable MQTT bridge.
Publishing the example topic alone does not execute the Linux sender.

The bridge must:

- Accept commands only for the configured, approved projector.
- Handle `wake` by sending ordinary HID Wake when connected, or the bounded
  sender above when disconnected.
- Handle `sleep` by delivering HID Sleep through the existing remote.
- Serialize transmissions and ignore retained command messages.
- Report failures; let HA independently observe the projector's power state.

After configuring that bridge and HA's MQTT integration, merge a script like
this into `scripts.yaml`. Replace `remote.projector` with your actual Android
TV Remote **power-state** entity and replace the topic with your bridge's
configured command topic. Do not overwrite unrelated scripts.

```yaml
projector_wake:
  alias: Wake projector
  mode: single
  sequence:
    - if:
        - condition: state
          entity_id: remote.projector
          state: "on"
      then:
        - stop: "Projector is already on."
    - action: mqtt.publish
      data:
        topic: example/projector/command
        payload: wake
        retain: false
    - wait_template: "{{ is_state('remote.projector', 'on') }}"
      timeout: "00:01:30"
      continue_on_timeout: true
    - if:
        - condition: template
          value_template: "{{ not wait.completed }}"
      then:
        - stop: "Projector did not confirm power-on within 90 seconds."
          error: true
```

A bridge implementing `sleep` can receive this action from an existing sleep
script, followed by a wait for the actual off/unavailable state:

```yaml
action: mqtt.publish
data:
  topic: example/projector/command
  payload: sleep
  retain: false
```

Reload scripts using HA's script reload action after validating the merged
configuration. Ordinary operation then needs neither a browser nor ADB.

For an API-based check, use your own authorized HA API client:

```text
POST /api/services/script/projector_wake     body: {}
GET  /api/states/remote.projector
```

Check the returned **device state**, not merely HTTP success or the script
returning to `off` (which only means its run ended). See the
[HA REST API](https://developers.home-assistant.io/docs/api/rest/),
[MQTT actions](https://www.home-assistant.io/integrations/mqtt/) and
[script action syntax](https://www.home-assistant.io/docs/scripts/perform-actions/).
Keep API credentials out of issue reports, shell examples and committed files.

## Troubleshooting

| Symptom | Next check |
| --- | --- |
| Host is absent from accessory search or cannot deliver input | Fix the existing HID profile, input support and appropriate device classification first. The sender alone is not a keyboard emulator. |
| `AlreadyExists` or MiPower reports an already-paired target | Keep the working bond. The default pairing-request backend is being skipped intentionally; it is separate from this sender. |
| Name changed on Linux but not on the projector | Check whether the HID emulator overwrites the alias; refresh accessory discovery and reconnect the existing host. |
| Immediate wake works, later wake fails | Test after actual Bluetooth/network loss, then verify enrollment and the Bluetooth target address. |
| Sender exits successfully but the screen stays off | Verify the host's saved wake identity, target Bluetooth MAC and independent power state. Packet completion is not a power acknowledgement. |
| First Sleep after reconnect is lost | Allow Android to finish input registration before the first HID report. A 750 ms queued-report delay solved this in the tested host service; it is outside this sender and not a universal timing value. |
| Cannot bind the management socket | Check host-side privileges. Running inside an unprivileged HA container does not automatically give controller-management access. |
| Management command is unsupported / no unused slot | Record kernel, controller and error details. Do not replace an occupied instance or reset shared Bluetooth to force a test. |
| Shared-state verification fails | Stop this test and coordinate other advertising changes; the sender does not roll back unrelated applications' configuration. |

To revert the setup, stop your own sender/bridge changes and restore the
recorded HID configuration and adapter alias. Preserve the original remote
and existing key storage. Broad Bluetooth resets and deleting all bonds were
not part of the successful procedure.

For a useful issue report, include model/firmware, Linux/BlueZ versions,
controller capabilities, whether Classic HID input works, pairing state,
classification-log outcome, command output, timings and observed display state.
Replace real addresses consistently with labels. Do not upload bond files,
link keys, API tokens or entire authentication/debug databases.

## Evidence and packet details

In the first successful radio-level cycle, network access returned 46 seconds
after transmission began; Android reported Awake/display ON, and the operator
confirmed no physical remote press. A subsequent full HA REST sleep/deep-
standby/wake cycle reached actual `on` in 66.8 seconds, with display ON checked
independently. The host bond file stayed unchanged. These are individual
measurements, not guaranteed startup times.

The captured 31-byte advertisement was:

| AD type | Observed bytes |
| --- | --- |
| Flags `01` | `05` |
| Manufacturer field `FF` | `00 01`, with no following manufacturer payload |
| Short name `08` | `MI RC` |
| Partial 16-bit UUIDs `02` | `12 18` (HID) |
| Class `0D` | `04 05 00` |
| TX power `0A` | `00` |
| Observed type `FE` | Last three target Bluetooth address bytes, reversed |

The packet layout and firmware behavior come from this device's capture and
code inspection, not a published Xiaomi protocol specification. See
[BlueZ's management API](https://raw.githubusercontent.com/bluez/bluez/5.72/doc/mgmt-api.txt)
for the per-instance commands and
[Xiaomi's projector FAQ](https://www.mi.com/global/support/faq/details/KA-06604/)
for the original remote's power behavior. A single successful model/firmware
combination does not establish support for the whole Xiaomi projector range.
