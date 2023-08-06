"""
Coarse frequency compensation algorithms.
"""
import logging
from typing import Tuple

import numpy as np
from numpy.fft import fft, fftshift

_log = logging.getLogger(__name__)

class CoarseFrequencyComp:
    r"""
    Open loop frequency correction to a PSK input signal.

    The algorithm estimates the frequency error :math:`\Delta\hat{f}` by using a periodogram of the :math:`m`\ :sup:`th`\  power of the received signal (the :math:`m`\ :sup:`th`\  power is used since it removes the :math:`m`\ :sup:`th`\  order PSK modulation, leaving only the carrier at a frequency :math:`m` times its original frequency):

    TODO equation

    where :math:`f_s` is the sampling frequency (specified by :attr:`sample_rate`), :math:`m` is the modulation order (specified by :attr:`mod_order`), :math:`r(n)` is the received sequence, and :math:`N` is the number of samples of the periodogram. To avoid aliasing :math:`\Delta\hat{f}` must be restricted to :math:`\left[\frac{-R_{sym}}{2}, \frac{R_{sym}}{2}\right]`, where :math:`R_{sym}=\frac{R_b}{log_2(m)}`, with :math:`R_b` representing the bit rate.

    The algorithm effectively searches for a frequency that maximizes the time average of the :math:`m`\ :sup:`th`\  power of the received signal multiplied by frequencies in the range of :math:`\left[\frac{-R_{sym}}{2}, \frac{R_{sym}}{2}\right]`. As the form of the algorithm is the definition of the DFT of :math:`r^{m}(n)`, searching for a frequency that maximizes the time average is equivalent to searching for a peak line in the spectrum of :math:`r^{m}(n)`. The number of points required by the FFT is

    TODO equation

    where :math:`f_r` is the desired frequency resolution, specified by :attr:`freq_res`. Note that :math:`log_2\left(\frac{f_s}{f_r}\right)` should be rounded up, since it might not be integer.
    """

    def __init__(self, mod_order: int, sample_rate: float, freq_res: float):
        """
        :param mod_order: Modulation order (e.g., 2 for BPSK, 4 for QPSK)
        :param sample_rate: Input signal sampling rate (Hz)
        :param freq_res: Desired frequency resolution (Hz)
        """
        self.mod_order = mod_order
        self.sample_rate = sample_rate
        self.freq_res = freq_res
        self._fft_size = int(2**np.ceil(np.log2(self.sample_rate / self.freq_res)))
        self._sum_phase = 0.0
        self._prev_buf = np.zeros(self._fft_size, dtype=complex)

    def __call__(self, inp: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        The main work function.

        :param inp: Input samples
        :return: Output samples, FFT of the input signal buffer, frequency offset
        """
        if len(inp) > self._fft_size:
            # TODO Implement average fft
            raise NotImplementedError('Average FFT not implemented')

        time_steps = np.arange(0, len(inp) + 1)
        raised = inp**self.mod_order
        out = np.empty_like(inp)
        buf = np.hstack((self._prev_buf[len(raised):], raised))
        self._prev_buf = buf

        abs_fft = abs(fft(buf, self._fft_size))
        shift_fft = fftshift(abs_fft)
        max_idx = np.argmax(shift_fft)
        offset_idx = max_idx - self._fft_size / 2
        df = self.sample_rate / self._fft_size
        freq_offset = df  * (offset_idx) / self.mod_order
        phase = freq_offset * time_steps / self.sample_rate

        # Frequency correction
        out = inp * np.exp(1j * 2 * np.pi * (self._sum_phase - phase[:-1]))
        self._sum_phase -= phase[-1]
        return out, shift_fft, freq_offset

    def __repr__(self):
        """
        Returns a string representation of the object.

        :return: A string representing the object and it's properties.
        """
        args = 'mod_order={}, sample_rate={}, freq_res={}'.format(self.mod_order, self.sample_rate, self.freq_res)
        return '{}({})'.format(self.__class__.__name__, args)
