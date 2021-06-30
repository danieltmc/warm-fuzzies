from jotform import *
from PIL import Image
from PIL import ImageDraw
from io import BytesIO
import requests

def selectFormId(forms):
    # If there is only one form, then return that form's ID
    if len(forms) is 1:
        return forms[0]['id']
    else:
        # List forms that the user can choose
        for i in range(len(forms)):
            print '#{num} {name}'.format(num=i+1, name=forms[i]['title'])
        # Return the ID of the form that the user chose
        return forms[int(input('Select the number of the form that you would like to process\n'))-1]['id']

def watermarkPhotos(submissions, apiKey, saveLocation):
    for submission in submissions:
        studentName = submission['answers']['3']['prettyFormat']
        imageUrl = submission['answers']['4']['answer'][0]
        # Preserve format of uploaded image
        imageExtension = imageUrl[imageUrl.rindex('.'):]
        # Images can only be downloaded while authenticated
        # Include API key in headers to download the image
        imageRequest = requests.get(imageUrl, headers={'apiKey':apiKey})
        studentImage = Image.open(BytesIO(imageRequest.content))
        width, height = studentImage.size
        # Add 200px white margin at the bottom of the image for the student's name
        watermarkedImage = Image.new(studentImage.mode, (width, height + 200), (255, 255, 255))
        watermarkedImage.paste(studentImage, (0, 0))
        # Add student's name on bottom margin in black text
        ImageDraw.Draw(watermarkedImage).text((0, height), studentName, (0, 0, 0))
        watermarkedImage.save(saveLocation + '\\' + studentName + imageExtension)

def main():
    apiKey = input('Enter the JotForm API key\n')
    jotformClient = JotformAPIClient(apiKey)
    forms = jotformClient.get_forms()
    formId = selectFormId(forms)
    saveLocation = input('Enter the path to the folder where you would like the files saved.\n\
                         You will need to create a folder if one does not already exist.\n\
                         \n(e.g. "C:\\Users\\MartyBaker\\Documents\\WarmFuzzies2021\\\n')
    watermarkPhotos(jotformClient.get_form_submissions(formId), apiKey, saveLocation)

if __name__ == '__main__':
    main()