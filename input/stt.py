import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


# ============================================================
# KAI VOCABULARY / STT NORMALIZATION
# ============================================================

VOCABULARY = {

    # STT mistakes
    "guy": "kai",
    "okay": "kai",

    # Phrase variations
    "hey kai": "hey kai",
    "hello pi": "hey kai",
    "okay bye": "hey kai",

    # Pronunciation variations
    "hey guy": "hey kai",
    "okay guy": "okay kai",
    "hey pi": "hey kai",
    "okay pi": "okay kai",

    # Indian-accent / pronunciation variations
    "bye": "kai",
    "pi": "kai",
    "hello kind": "hey kai",
    "kind": "kai",
    "hey kind": "hey kai",
    "okay kind": "okay kai",
    "pai": "kai",
    "hey pai": "hey kai",
    "okay pai": "okay kai",
    "hello pai": "hey kai",
    "kyle": "kai",
    "hello kyle": "hey kai",
    "okay kyle": "okay kai"
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize common Whisper pronunciation/STT mistakes.
    """

    text = text.lower().strip()

    # --------------------------------------------------------
    # Phrase replacements first
    # --------------------------------------------------------

    for wrong, correct in VOCABULARY.items():

        if " " in wrong:
            text = text.replace(
                wrong,
                correct
            )

    # --------------------------------------------------------
    # Individual word replacements
    # --------------------------------------------------------

    words = text.split()

    words = [
        VOCABULARY.get(
            word,
            word
        )
        for word in words
    ]

    return " ".join(words)


# ============================================================
# STT ENGINE
# ============================================================

class STT:

    def __init__(
        self,
        model_name: str = "large-v3",
        device: str = "cuda",
        compute_type: str = "float16"
    ):
        """
        Initialize Faster-Whisper once.

        The model is NOT loaded every time the user speaks.
        """

        print(
            f"[STT] Loading Whisper model: "
            f"{model_name}"
        )

        self.model = WhisperModel(
            model_name,
            device=device,
            compute_type=compute_type
        )

        print("[STT] Whisper ready.")

    # ========================================================
    # RECORD AUDIO
    # ========================================================

    def record_audio(
        self,
        filename: str = "recording.wav",
        duration: int = 5,
        sample_rate: int = 48000
    ):
        """
        Record microphone input and save it as WAV.
        """

        print("\n[STT] Speak now...")

        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        write(
            filename,
            sample_rate,
            audio
        )

        print(
            f"[STT] Audio saved: {filename}"
        )

        return filename

    # ========================================================
    # TRANSCRIBE
    # ========================================================

    def transcribe(
        self,
        audio_file: str = "recording.wav"
    ) -> str:
        """
        Convert recorded audio into text.
        """

        print("[STT] Transcribing...")

        segments, info = self.model.transcribe(
            audio_file,
            language="en"
        )

        text = ""

        for segment in segments:
            text += segment.text

        text = normalize_text(
            text
        )

        print(
            f"[STT] Recognized: {text}"
        )

        return text.strip()

    # ========================================================
    # RECORD + TRANSCRIBE
    # ========================================================

    def get_speech_text(
        self,
        duration: int = 5
    ) -> str:
        """
        Complete microphone → text pipeline.
        """

        audio_file = self.record_audio(
            duration=duration
        )

        return self.transcribe(
            audio_file
        )


# ============================================================
# SIMPLE FUNCTION INTERFACE
# ============================================================

_stt_engine = None


def get_speech_text(
    duration: int = 5
) -> str:
    """
    Simple interface for SSK.

    Usage:

        text = get_speech_text()
    """

    global _stt_engine

    if _stt_engine is None:

        _stt_engine = STT()

    return _stt_engine.get_speech_text(
        duration=duration
    )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    text = get_speech_text()

    print(
        "\nFinal text:"
    )

    print(text)