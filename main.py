from AudioController.AudioControllerClient import AudioControllerClient
from AudioController.AudioControllerServer import AudioControllerServer
from AudioIdentifier import AudioIdentifier
import sounddevice as sd
import sys


def check_port(a_port):
    if not a_port.isnumeric():
        print("Please input a number.")
        sys.exit()

    a_port = int(a_port)

    if a_port < 1024 or a_port > 65535:
        print("Please input a number between 1024 and 65535.")
        sys.exit()

    return a_port


if __name__ in ('__main__', 'audioidentifier__main__', 'AudioIdentifier_main__'):
    # Unity 連携コード
    a_server_port = sys.argv[1]
    a_myself_port = sys.argv[2]
    check_port(a_server_port)
    check_port(a_myself_port)

    client = AudioControllerClient(int(a_server_port))
    server = AudioControllerServer(int(a_myself_port), client)
    audio_identifier = AudioIdentifier(client)

    def task():
        with sd.InputStream(channels=audio_identifier.chennels(),
                            samplerate=audio_identifier.rate(),
                            dtype='float32',
                            callback=audio_identifier.audio_callback):
            print("Recording... Press Ctrl+C to stop.")
            while client.is_running():
                sd.sleep(int(audio_identifier.duration() * 1000))

    client.start(task)
    server.start()

    server.thread().join()
    client.thread().join()

    # ターミナル稼働テスト用
    # audio_identifier = AudioIdentifier(None)
    # with sd.InputStream(channels=audio_identifier.chennels(),
    #                     samplerate=audio_identifier.rate(),
    #                     dtype='float32',
    #                     callback=audio_identifier.audio_callback):
    #     print("Recording... Press Ctrl+C to stop.")
    #     while True:
    #         sd.sleep(int(audio_identifier.duration() * 1000))
