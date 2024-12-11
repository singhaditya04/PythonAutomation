from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

# Login Function
def login_to_portal(username, password):
    driver.get("https://www.linkedin.com/login")
    
    try:
        # Wait for the username field to load
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        
        # Wait for the Sign In button
        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in']")))
        sign_in_button.click()
    except Exception as e:
        print(f"Error during login: {e}")

# Search Jobs
def search_jobs(keyword, location):
    driver.get("https://www.linkedin.com/jobs")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search jobs']"))).send_keys(keyword)
    driver.find_element(By.CSS_SELECTOR, "input[aria-label='Search location']").send_keys(location + Keys.RETURN)

# Apply to Jobs
def apply_to_jobs():
    applied_jobs = []
    job_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-container")))
    for job in job_cards:
        try:
            job.click()
            time.sleep(2)  # Wait for details to load
            apply_button = driver.find_element(By.XPATH, "//button[text()='Easy Apply']")
            apply_button.click()
            time.sleep(2)  # Simulate human action
            applied_jobs.append(driver.current_url)
        except Exception:
            continue
    return applied_jobs

# Save Logs
def save_logs(job_urls):
    df = pd.DataFrame({'Job URL': job_urls})
    df.to_csv("applied_jobs.csv", mode='a', index=False, header=False)

# Main Script
try:
    login_to_portal("adisingh142003@gmail.com", "Aditya@10")
    search_jobs("Data Scientist", "Remote")
    applied_jobs = apply_to_jobs()
    save_logs(applied_jobs)
finally:
    driver.quit()
