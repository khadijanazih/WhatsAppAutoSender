from setup import bucket
import pywhatkit,pyautogui,time
def get_file_download_url(file_name):
    blob = bucket.blob(file_name)  # Access the specified file

    try:
        blob.make_public()  # Make the file public
        download_url = blob.public_url
        return download_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def sendmsgs (data_array):
    for tel,message in data_array:
        print(message)
        pywhatkit.sendwhatmsg_instantly(tel, message,10,True)
        time.sleep(8)
        pyautogui.press('enter')
