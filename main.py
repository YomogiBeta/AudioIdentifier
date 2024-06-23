# from AudioController.AudioControllerClient import AudioControllerClient
# from AudioController.AudioControllerServer import AudioControllerServer
from AudioIdentifier import AudioIdentifier
import sounddevice as sd
import sys


def check_port(aPort):
    if not aPort.isnumeric():
        print("Please input a number.")
        sys.exit()

    aPort = int(aPort)

    if aPort < 1024 or aPort > 65535:
        print("Please input a number between 1024 and 65535.")
        sys.exit()

    return aPort


if __name__ == '__main__':
    # Unity 連携コード
    # aServerPort = sys.argv[1]
    # aMySelfPort = sys.argv[2]
    # check_port(aServerPort)
    # check_port(aMySelfPort)

    # client = AudioControllerClient(int(aServerPort))
    # server = AudioControllerServer(int(aMySelfPort), client)
    # audio_identifier = AudioIdentifier(client)

    # def task():
    #     with sd.InputStream(channels=audio_identifier.chennels(),
    #                         samplerate=audio_identifier.rate(),
    #                         dtype='float32',
    #                         callback=audio_identifier.audio_callback):
    #         print("Recording... Press Ctrl+C to stop.")
    #         while client.is_running():
    #             sd.sleep(int(audio_identifier.duration() * 1000))

    # client.start(task)
    # server.start()

    # server.thread().join()
    # client.thread().join()

    audio_identifier = AudioIdentifier(None)
    with sd.InputStream(channels=audio_identifier.chennels(),
                        samplerate=audio_identifier.rate(),
                        dtype='float32',
                        callback=audio_identifier.audio_callback):
        print("Recording... Press Ctrl+C to stop.")
        while True:
            sd.sleep(int(audio_identifier.duration() * 1000))
