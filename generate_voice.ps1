param (
    [string]$text = "Headshot pa tu casa",
    [string]$output = "voice.wav"
)

Add-Type -AssemblyName System.Speech
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speak.SetOutputToWaveFile($output)
$speak.Speak($text)
$speak.Dispose()
Write-Output "Done: $output"
