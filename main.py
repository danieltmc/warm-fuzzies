from jotform import *

def main():
    apiKey = input('Enter the JotForm API key\n')
    jotformClient = JotformAPIClient(apiKey)

if __name__ == '__main__':
    main()