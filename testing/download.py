from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the webpage
driver.get('https://spotifydown.com')

# Wait for the page to load
time.sleep(5)

consent_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]')
consent_button.click()

# Locate the input field for the Spotify link
input_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/input')  # Replace 'inputFieldID' with the actual ID of the input field

# Enter the Spotify playlist link
song_downloads = [0, 2, 4]
spotify_link = 'https://open.spotify.com/playlist/1f7FdluftB6scihHNwoYIk'
input_field.send_keys(spotify_link)

# Submit the link (this may vary depending on the website's form submission method)
input_field.send_keys(Keys.RETURN)

# Wait for the download button to become available (this may vary depending on the website's loading time)
time.sleep(5)  # Adjust the sleep time as needed

# scroll down a little bit
driver.execute_script("window.scrollTo(0, 500)")

name_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/p[1]')
name = name_field.text
song_list = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[3]')

songs = song_list.find_elements(By.CLASS_NAME, "grid")
# print the source code of the songs
for song in songs:
    index = int(song.find_element(By.TAG_NAME, 'span').text) - 1

    # Extract the song name
    song_name = song.find_element(By.TAG_NAME, 'p').text

    download_button = song.find_element(By.TAG_NAME, 'button')

    print(f"{index}: {song_name}")

for index in song_downloads:
    download_button = songs[index].find_element(By.TAG_NAME, 'button')
    download_button.click()
    time.sleep(20)

input("Press Enter to continue...")
driver.quit()
exit()

time.sleep(30)
# Locate and click the download button
download_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/button')  # Replace 'downloadButtonID' with the actual ID of the download button
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
for _ in range((duration+1)*60):  # Adjust the range value based on your expected download time
    if os.path.exists(file_path):
        downloaded = True
        break
    time.sleep(1)  # Check every second

time.sleep(20)

# Close the WebDriver
driver.quit()
