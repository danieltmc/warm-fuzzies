from jotform import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
import requests


def selectFormId(forms):
    # If there is only one form, then return that form's ID
    if len(forms) is 1:
        return forms[0]['id']
    else:
        # List forms that the user can choose
        for i in range(len(forms)):
            print '#{num} {name}'.format(num=i + 1, name=forms[i]['title'])
        # Return the ID of the form that the user chose
        return forms[int(input('Select the number of the form that you would like to process\n')) - 1]['id']


def processSubmissions(submissions, apiKey, saveLocation):
    for submission in submissions:
        studentName = submission['answers']['3']['prettyFormat']
        imageUrl = submission['answers']['4']['answer'][0]
        # Preserve format of uploaded image
        imageExtension = imageUrl[imageUrl.rindex('.'):]
        # Images can only be downloaded while authenticated
        # Include API key in headers to download the image
        imageRequest = requests.get(imageUrl, headers={'apiKey': apiKey})
        studentImage = Image.open(BytesIO(imageRequest.content))
        # Rotate image if uploaded sideways (assuming uploaded image is in portrait)
        width, height = studentImage.size
        if (width > height): studentImage.rotate(270)
        resizedStudentImage = studentImage.resize((900, 1500)) # 3x5 @ 300dpi
        # Add student's name as a watermark
        watermarkedImage = watermarkPhoto(studentName, resizedStudentImage)
        watermarkedImage.save(saveLocation + '\\' + studentName + imageExtension)


def watermarkPhoto(studentName, resizedStudentImage):
    # Add white margin (1 inch around entire image) for the student's name
    watermarkedImage = Image.new(resizedStudentImage.mode, (1200, 1800), (255, 255, 255))
    watermarkedImage.paste(resizedStudentImage, (150, 150))
    # Add student's name on bottom margin in black text
    font = ImageFont.truetype('arial.ttf', size=96)
    draw = ImageDraw.Draw(watermarkedImage)
    textWidth, textHeight = draw.textsize(studentName, font=font)
    draw.text(
        ((1200 - textWidth) / 2, 1650),
        studentName,
        (0, 0, 0),
        font=ImageFont.truetype('arial.ttf', size=96)
    )
    return watermarkedImage


def main():
    apiKey = str(raw_input('Enter the JotForm API key\n'))
    jotformClient = JotformAPIClient(apiKey)
    forms = jotformClient.get_forms()
    formId = selectFormId(forms)
    saveLocation = raw_input('Enter the path to the folder where you would like the files saved.\n'
                             'You will need to create a folder if one does not already exist.\n'
                             '(e.g. "C:\\Users\\MartyBaker\\Documents\\WarmFuzzies2021\\")\n')
    print('\nDownloading and watermarking images now...')
    processSubmissions(jotformClient.get_form_submissions(formId), apiKey, saveLocation)
    print('All images have been downloaded and watermarked!')


if __name__ == '__main__':
    main()
