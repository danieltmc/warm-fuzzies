from jotform import *

def selectFormId(forms):
    # If there is only one form, then return that form's ID
    if len(forms) is 1:
        return forms[0]['id']
    else:
        # List forms that the user can choose
        for i in range(len(forms)):
            print "#{num} {name}".format(num=i+1, name=forms[i]['title'])
        # Return the ID of the form that the user chose
        return forms[int(input("Select the number of the form that you would like to process\n"))-1]['id']

def main():
    apiKey = input('Enter the JotForm API key\n')
    jotformClient = JotformAPIClient(apiKey)
    forms = jotformClient.get_forms()
    formId = selectFormId(forms)

if __name__ == '__main__':
    main()