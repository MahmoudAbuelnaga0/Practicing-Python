# Automating Job Applying

A program that apply, check or save easy-applying jobs on linkedin that don't require additional information (only your resume).

## Instructions

- Install chrome driver for your chrome version and store its path in "chrome_driver_path" variable
- You need to upload your resume on job applying prefrences on linkedin
- Your number and email must be available on your account
- You need to fill the empty string constants in "main.py": LINKEDIN_EMAIL, LINKDIN_PASS and ROLE_U_SEARCHING_FOR
- Add to JOB_FUNCTIONS list in "main.py" functions that you want to apply on each job you find: save a job for later, follow company and easy applying on job
  - Note: Do not use "easy_apply" function except if you want to really apply for jobs
  - If you want to add easy applying to JOB_FUNCTIONS list keep it at the end of the list
- Captcha may be generated to check if you're a bot. You got to do it manually
