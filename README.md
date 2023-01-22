# Image to Text Converter

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
This is a code repository for an image-to-text converter that uses OpenCV, tesseract and python regular expression

<h3>Requirements</h3>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
In order to locally use this website, you must install the libraries requirements using the following command: 

```bash
 pip install -r requirements.txt
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Additionally, you will also need Tesseract, which can be found at this [link](https://tesseract-ocr.github.io/tessdoc/Compiling.html)

<h3>Environment Variables</h3>

In order to make Pytesseract, you must inform Tesseract folder location

`tess.pytesseract.tesseract_cmd` = r"C:\PYTESSERACT LOCATION.exe"

<h3>Expected Output</h3>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Using the following image as an example

<img src="https://user-images.githubusercontent.com/52424334/213899698-c3e0c73d-42d4-475a-95c7-60c7fa1658f9.jpg" width="500">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Through image manipulation using OpenCV and python, the code generates a centered and easier-to-read image

<img src="https://user-images.githubusercontent.com/52424334/213899700-3854ea09-aad1-441a-8137-c14c62f188d7.png" width="500">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Finally, Pytesseract takes this new Image and converts it to strings that can be filtered using regular expressions


<img src="https://user-images.githubusercontent.com/52424334/213899705-c2897134-5cd7-469e-b2a2-ab11300c7780.png" width="500">
