import azure.cognitiveservices.speech as speechsdk
import time

done = False

def stop_cb(evt):
    """callback that stops continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    speech_recognizer.stop_continuous_recognition()
    # nonlocal done
    done = True

def append_to_file (evt, dest):
    print(evt.result.text)
    with open(dest, "a") as myfile:
        myfile.write(f'\n{evt.result.text}')
        myfile.close()

def speech_to_text (audio_filename, text_to):
    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    speech_key, service_region = "2d98d6cf18cc496799fe05959cd61caa", "brazilsouth"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language="pt-BR"

    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_input = speechsdk.AudioConfig(filename=audio_filename)

    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    print("Recognizing first result...")

    # Connect callbacks to the events fired by the speech recognizer
    # speech_recognizer.recognizing.connect(lambda evt: append_to_file(evt))
    speech_recognizer.recognized.connect(lambda evt: append_to_file(evt, text_to))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    # </SpeechContinuousRecognitionWithFile>