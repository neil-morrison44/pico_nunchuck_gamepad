import usb_hid

# This is only one example of a gamepad descriptor, and may not suit your needs.
# https://marcelmg.github.io/usb_snes_gamepad/
GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # USAGE_PAGE(Generic Desktop)
    0x09, 0x05,  # USAGE(Game Pad)
    0xa1, 0x01,  # COLLECTION(Application)
    0xa1, 0x00,  # COLLECTION(Physical)
    0x05, 0x09,  # USAGE_PAGE(Button)
    0x19, 0x01,  # USAGE_MINIMUM(Button 1)
    0x29, 0x0c,  # USAGE_MAXIMUM(Button 12)
    0x15, 0x00,  # LOGICAL_MINIMUM(0)
    0x25, 0x01,  # LOGICAL_MAXIMUM(1)
    0x75, 0x01,  # REPORT_SIZE(1)
    0x95, 0x10,  # REPORT_COUNT(16)
    0x81, 0x02,  # INPUT(Data, Var, Abs)
    0xc0,       # END_COLLECTION
    0xc0  # END_COLLECTION
))

gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(4,),           # Descriptor uses report ID 4.
    in_report_lengths=(2,),    # This gamepad sends 4 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable(
    (gamepad,)
)
