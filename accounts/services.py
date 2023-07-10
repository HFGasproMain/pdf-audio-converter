import os
import PyPDF2
from gtts import gTTS
from django.conf import settings




def convert_pdf_to_audio(pdf_file_path, language):
    audio_directory = os.path.join(settings.MEDIA_ROOT, 'audio_files')
    print(f'which directory => {audio_directory}')

    # Check if the audio directory exists
    if not os.path.exists(audio_directory):
        # Create the audio directory
        os.mkdir(audio_directory)
    
    # Open the PDF file
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text content from each page of the PDF
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()

    # Convert the extracted text to audio using gTTS
    tts = gTTS(text_content, lang=language)
    
    # Define the path to save the audio file
    #audio_file_path = f"media/audio_files/{os.path.basename(pdf_file_path)}.mp3"
    audio_file_path = os.path.join(audio_directory, f"{os.path.basename(pdf_file_path)}.mp3")
    print(f'audio_file_path {audio_file_path}')
    
    # Save the audio file
    tts.save(audio_file_path)
    
    # Return the path of the generated audio file
    return audio_file_path
