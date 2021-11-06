import struct
import time


class Gamepad:

    def __init__(self, device):
        self._gamepad_device = device

        # Reuse this bytearray to send mouse reports.
        # Typically controllers start numbering buttons at 1 rather than 0.
        # report[0] buttons 1-8 (LSB is button 1)
        # report[1] buttons 9-16
        self._report = bytearray(2)

        # Remember the last report as well, so we can avoid sending
        # duplicate reports.
        self._last_report = bytearray(2)

        # Store settings separately before putting into report. Saves code
        # especially for buttons.
        self._buttons_state = 0

        # Send an initial report to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    def press_buttons(self, buttons):
        """Press and hold the given buttons."""
        for button in buttons:
            self._buttons_state |= 1 << self._validate_button_number(
                button) - 1
        # self._send()

    def release_buttons(self, buttons):
        """Release the given buttons."""
        for button in buttons:
            self._buttons_state &= ~(
                1 << self._validate_button_number(button) - 1)
        # self._send()

    def reset_all(self):
        """Release all buttons and set joysticks to zero."""
        self._buttons_state = 0
        self.send(always=True)

    def send(self, always=False):
        """Send a report with all the existing settings.
        If ``always`` is ``False`` (the default), send only if there have been changes.
        """
        struct.pack_into(
            "<H",
            self._report,
            0,
            self._buttons_state,
        )

        if always or self._last_report != self._report:
            # print([hex(byte) for byte in self._report])
            self._gamepad_device.send_report(self._report)
            # Remember what we sent, without allocating new storage.
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 16:
            raise ValueError("Button number must in range 1 to 16")
        return button
