import os
import re
import shutil
import time
import zipfile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService # Similar thing for firefox also!
from subprocess import CREATE_NO_WINDOW


def download_playlist(playlist_id: str):
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options)

    # Open the webpage
    driver.get('https://spotifydown.com')

    # Wait for the page to load
    time.sleep(5)

    consent_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]')
    consent_button.click()

    # Locate the input field for the Spotify link
    input_field = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div[1]/input')  # Replace 'inputFieldID' with the actual ID of the input field

    # Enter the Spotify playlist link
    spotify_link = 'https://open.spotify.com/playlist/' + playlist_id
    input_field.send_keys(spotify_link)

    # Submit the link (this may vary depending on the website's form submission method)
    input_field.send_keys(Keys.RETURN)

    # Let the driver wait until the name field is displayed
    name_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/p[1]')
    name = name_field.text

    if name == "An error occurred. Please try again.":  # If the playlist is not found
        print("Playlist empty.")
        driver.quit()
        return
    print("Loading playlist: ", name)

    # Locate and click the download button
    download_button = driver.find_element(By.XPATH,
                                          '/html/body/div[1]/div/div[2]/div[1]/button')  # Replace 'downloadButtonID' with the actual ID of the download button
    download_button.click()

    duration = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/p[2]/b[2]')
    duration = int(duration.text.split(' ')[1])

    time.sleep(2)
    okay_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/button[1]')
    okay_button.click()

    download_folder = os.path.join(r"C:\Users\danie\Downloads")
    expected_file_name = name + '_SpotifyDown_com.zip'  # Replace with the actual expected file name or pattern

    # Check if the file is downloaded
    file_path = os.path.join(download_folder, expected_file_name)
    downloaded = False
    for _ in range((duration + 1) * 60):  # Adjust the range value based on your expected download time
        if os.path.exists(file_path):
            downloaded = True
            break
        time.sleep(1)  # Check every second

    print("Downloaded: ", name)
    time.sleep(5)
    # Close the WebDriver
    driver.quit()


def download_multiple(playlist_ids: list, progressbar):
    file_names = []
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")  # Suppress most logs

    # Optional: if you need to suppress specific logs, you can use logging preferences
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=chrome_options)

    # Open the webpage
    driver.get('https://spotifydown.com')

    # Wait for the page to load
    time.sleep(5)

    consent_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]')
    consent_button.click()

    for i in range(len(playlist_ids)):
        playlist_id = playlist_ids[i]
        # Locate the input field for the Spotify link
        input_field = driver.find_element(By.XPATH,
                                          '/html/body/div[1]/div/div[1]/input')  # Replace 'inputFieldID' with the actual ID of the input field

        # Enter the Spotify playlist link
        spotify_link = 'https://open.spotify.com/playlist/' + playlist_id
        input_field.send_keys(spotify_link)

        # Submit the link (this may vary depending on the website's form submission method)
        input_field.send_keys(Keys.RETURN)

        # Wait for the download button to become available (this may vary depending on the website's loading time)
        time.sleep(5)  # Adjust the sleep time as needed

        name_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/p[1]')
        name = name_field.text
        if name == "Something went wrong. Please try again later.":  # If the playlist is not found
            print("Playlist empty.")
            time.sleep(2)
            driver.get("https://spotifydown.com")
            time.sleep(2)
            continue

        # Locate and click the download button
        download_button = driver.find_element(By.XPATH,
                                              '/html/body/div[1]/div/div[2]/div[1]/button')  # Replace 'downloadButtonID' with the actual ID of the download button
        download_button.click()

        duration = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/p[2]/b[2]')
        duration = int(duration.text.split(' ')[1])

        time.sleep(2)
        okay_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/button[1]')
        okay_button.click()


        download_folder = os.path.join(r"C:\Users\danie\Downloads")
        expected_file_name = name + '_SpotifyDown_com.zip'  # Replace with the actual expected file name or pattern

        # Check if the file is downloaded
        file_path = os.path.join(download_folder, expected_file_name)
        duration_time = int((duration + 1) * 60)
        for passed in range(duration_time):  # Adjust the range value based on your expected download time
            try:
                prog = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div/div[3]/p[2]")
                current, limit = map(int, prog.text.split(" / "))
                progressbar.update_total(i, limit)
            except:
                pass
            if os.path.exists(file_path):
                break
            time.sleep(1)  # Check every second
            progressbar.update_progress(i, current, f"Downloading...")
        if os.path.exists(file_path):
            progressbar.update_progress(i, progressbar.states[i]["total"], f"Downloaded")
            file_names.append(file_path)
        else:
            progressbar.update_progress(i, 0, f"Try again...")
            i -= 1
        time.sleep(2)
        driver.get("https://spotifydown.com")
        time.sleep(2)

    # Close the WebDriver
    driver.quit()
    return file_names


def sanitize_filename(filename):
    # Replace invalid characters with an underscore
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized


def extract_zip(zip_path, extract_to):
    # Extract the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            # Sanitize the member name to ensure it is a valid file name
            sanitized_member = sanitize_filename(member)
            member_path = os.path.join(extract_to, sanitized_member)

            # Create any directories that don't exist yet
            if not os.path.exists(os.path.dirname(member_path)):
                os.makedirs(os.path.dirname(member_path))

            # Extract the member
            with zip_ref.open(member) as source, open(member_path, "wb") as target:
                shutil.copyfileobj(source, target)

