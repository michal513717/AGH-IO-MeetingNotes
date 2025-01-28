import pyaudio

class Helper:
    
    @staticmethod
    def getDefaultSpeakers(): 
        try:
            audio_interface = pyaudio.PyAudio()

            wasapi_info = audio_interface.get_host_api_info_by_type(pyaudio.paWASAPI)

            default_speakers = audio_interface.get_device_info_by_index(wasapi_info["defaultOutputDevice"])

            if not default_speakers["isLoopbackDevice"]:
                for loopback in audio_interface.get_loopback_device_info_generator():
                    if default_speakers["name"] in loopback["name"]:
                        print(f"Recording from: ({default_speakers['index']}){default_speakers['name']}")

                        return loopback
                else:
                    print("Default loopback output device not found.\n\nRun `python -m pyaudiowpatch` to check available devices.\nExiting...\n")
                    exit()
        except Exception as e:
            raise RuntimeError(f"Audio device initialization failed: {e}")
