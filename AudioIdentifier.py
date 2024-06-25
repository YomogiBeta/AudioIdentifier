import tensorflow as tf
import numpy as np
import time as libTime
import sys
import os

from AudioController.AudioControllerClient import AudioControllerClient


class AudioIdentifier:

    _model_path = f'resource{os.sep}1.tflite'
    _mapping_path = f'resource{os.sep}yamnet_class_map.csv'
    # Parameters for audio stream
    _CHANNELS = 1
    _RATE = 15600
    _EXPECTED_SAMPLES = 15600
    _DURATION = 2

    _SOUND_DEVICE_STEP = 0.026

    def _find_data_file(self, filename):
        """frozen状況に合わせて引数のファイル名のファイルパスを取得する

        https://cx-freeze.readthedocs.io/en/latest/faq.html#data-files

        Args:
            filename (str):
                ファイル名.

        Returns:
            str:
                引数のファイル名のファイルパス.
        """
        if getattr(sys, "frozen", False):
            datadir = os.path.dirname(sys.executable)
        else:
            datadir = os.path.abspath(".")
        return os.path.join(datadir, filename)

    def __init__(self, client):
        self._client: AudioControllerClient = client
        self._interpreter = tf.lite.Interpreter(self._find_data_file(self._model_path))
        self._input_details = self._interpreter.get_input_details()
        # self._interpreter.experimental_options = {'use_gpu': True}
        # self._interpreter.allocate_tensors()
        self._waveform_input_index = self._input_details[0]['index']
        self._output_details = self._interpreter.get_output_details()
        self._scores_output_index = self._output_details[0]['index']

        a_class_labels_file = open(self._find_data_file(self._mapping_path), 'r')
        a_labels_list = [line.strip() for line in a_class_labels_file]
        self._a_class_labels = [label.split(',')[2] for label in a_labels_list]

        self._anAudioList = []
        self._aSecondIndex = 0
        self._aSendTimeStamp = 0
        self._aStopTime = 0.1

        self._check_items = ["Hands",
                             "Clapping",
                             "Finger snapping",
                             "Knock",
                             "Bouncing",
                             "Wood block",
                             "Door",
                             "Tick",
                             "Clock"]
        self._io_dict = {
            "Hands": "CLAP",
            "Clapping": "CLAP",
            "Finger snapping": "CLAP",
            "Knock": "DESK",
            "Bouncing": "DESK",
            "Wood block": "DESK",
            "Door": "DESK",
            "Tick": "DESK",
            "Clock": "DESK"
        }

    def preprocess_audio(self, waveform):
        # Resize or pad the waveform to match EXPECTED_SAMPLES
        if len(waveform) < self._EXPECTED_SAMPLES:
            # Pad the waveform with zeros at the end
            padded_waveform = np.zeros(self._EXPECTED_SAMPLES,
                                       dtype=np.float32)
            padded_waveform[:len(waveform)] = waveform
            return padded_waveform
        elif len(waveform) > self._EXPECTED_SAMPLES:
            # Resize the waveform to EXPECTED_SAMPLES
            resized_waveform = waveform[:self._EXPECTED_SAMPLES]
            return resized_waveform
        else:
            return waveform

    def classify_audio(self, waveform):
        # Preprocess the waveform to match EXPECTED_SAMPLES
        processed_waveform = self.preprocess_audio(waveform)

        # Resize input tensor and set the data
        self._interpreter.resize_tensor_input(self._waveform_input_index,
                                              processed_waveform.shape,
                                              strict=True)
        self._interpreter.allocate_tensors()
        self._interpreter.set_tensor(self._waveform_input_index,
                                     processed_waveform)

        # Perform inference
        self._interpreter.invoke()
        scores = self._interpreter.get_tensor(self._scores_output_index)

        # Find the top class index
        class_indexes = np.where(scores > 0.055)
        max_index = scores.argmax()
        results = [self._a_class_labels[max_index]]
        results = [self._a_class_labels[i] for i in class_indexes[1]]

        # print(f"Predicted label: {results}")

        return results

    def clear_state(self):
        self._anAudioList = []
        self._aSecondIndex = 0

    def check_pass(self, an_audio_type_list):
        for an_audio_type in an_audio_type_list:
            if an_audio_type in self._check_items:
                return an_audio_type
        return False

    def print_class(self, item):
        a_text = self._io_dict.get(item)
        if a_text:
            if self._client is not None:
                self._client.send(a_text)
            else:
                print(f"Predicted label: {a_text}")
            self._aSendTimeStamp = libTime.time()

    def setting_stop_time(self, item):
        a_text = self._io_dict.get(item)
        if a_text:
            if a_text == "DESK":
                self._aStopTime = 0.1
            else:
                self._aStopTime = 0.2

    def identification_send(self, force_clear=False):
        waveform = np.concatenate(self._anAudioList)
        result = self.classify_audio(waveform)
        # print(result)
        item = self.check_pass(result)

        if force_clear or item is not False:
            self.clear_state()

        if item is not False:
            self.print_class(item)
            self.setting_stop_time(item)

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Error: {status}")

        if self._aSendTimeStamp != 0 and libTime.time() - self._aSendTimeStamp < self._aStopTime:
            return

        # self._aSecondIndex = 0

        # Convert input data to float32 array
        waveform = np.array(indata[:, 0], dtype=np.float32)

        # waveformをaListに追加
        self._anAudioList.append(waveform)
        self._aSecondIndex += 0.026

        if self._aSecondIndex >= 0.48:
            self.identification_send(True)

        if self._aSecondIndex >= 0.35:
            self.identification_send()

        if self._aSecondIndex >= 0.28:
            self.identification_send()

        if self._aSecondIndex >= 0.16:
            self.identification_send()

    def chennels(self):
        return self._CHANNELS

    def rate(self):
        return self._RATE

    def duration(self):
        return self._DURATION
