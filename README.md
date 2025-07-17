# Cableway-Report-GUI
Developed a PyQt5-based desktop application to digitize cableway inspection reports, enabling inspectors to input structural data, drag-and-drop images, and generate formatted PDF summaries using the fpdf library. 

## Instructions for Usage
- Ensure you have Python 3.6 - 3.11 installed on your device as these versions of python seem to work well with the libraries used.
- Run “pip install PyQt5” and “pip install fpdf” in the terminal if not already
installed
- In the terminal, navigate to the directory in which the python file is located and run “python form_gen.py”
- A pop-up form should appear for you to input information
- Drag-and-drop area and image upload button are present and worked as intended in my testing
- By pressing the “generate pdf” the pdf is saved and named “Cableway_Report_yyyy-mm-dd_name_number”. You can find the pdf in the same directory as the python file.

## About the Code
The main functions of the code are:
- init_ui (lines 20 - 472) is responsible for creating the user interface and storing all the inputs
- upload_images (lines 512 - 536) checks if the selected image is a .png, .jpg, or .jpeg and throws a warning if it is not
- generate_pdf (lines 539 - 769) is responsible for taking the input data and creating the report with the data.
