import logging
import os
from basecampy3 import Basecamp3
import azure.functions as func
import json
import requests
import datetime

app = func.FunctionApp()
# Initialize Basecamp3 instance

bc3 = Basecamp3.from_environment()
company_id = os.environ["BASECAMP_ACCOUNT_ID"]

def main(basecamptrriger: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    if basecamptrriger.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    logging.info('Azure Function processed a request.')

    # Retrieve environment variables
    REFRESH_TOKEN = os.environ["BASECAMP_REFRESH_TOKEN"]
    BASECAMP_CLIENT_ID = os.environ["BASECAMP_CLIENT_ID"]
    BASECAMP_CLIENT_SECRET = os.environ["BASECAMP_CLIENT_SECRET"]
    project_id = os.environ["BASECAMP_PROJECT_ID"]
    project_name = os.environ["BASECAMP_PROJECT_Name"]
    access_token = session.post('https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token=${REFRESH_TOKEN}&client_id=${BASECAMP_CLIENT_ID}&client_secret=${BASECAMP_CLIENT_SECRET}')

    session = bc3.session
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    logging.info(f"The ID of project '{project_name}' is: {project_id}")
    
    inbox_url = "https://3.basecampapi.com/4535691/buckets/36999152/inboxes/7258888101.json"
    
    try:
        # Retrieve inbox information
        response = session.get(inbox_url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        inbox_info = response.json()

        # Extract the URL for retrieving new forwards
        forwards_url = inbox_info.get("forwards_url")
        if not forwards_url:
            logging.error("Forwards URL not found.")
            return func.HttpResponse("Forwards URL not found", status_code=500)

        # Retrieve the new forwards
        response = session.get(forwards_url)
        response.raise_for_status()
        new_forwards = response.json()

        logging.info("New email forwards:")
        results = []
        for forward in new_forwards:
            logging.info("Processing forward:")
            logging.info(forward)

            # Check if there's already a comment mentioning @xccelerate
            comment_already_exists = False
            
            # Get comments for the forward
            recording_id = forward['id']
            comments_url = f"https://3.basecampapi.com/{company_id}/buckets/{project_id}/recordings/{recording_id}/comments.json"
            response = session.get(comments_url)
            response.raise_for_status()
            comments = response.json()
            
            for comment in comments:
                if '@Matthijs Brouns , @Rick Vergunst , @Wesley Boelrijk , @Gary Clark : New email received' in comment['content']:
                    comment_already_exists = True
                    break
                
            # Construct result with content and comment information
            result = {
                'id': forward['id'],
                'content': forward['content'],
                'comment_already_exists': comment_already_exists
            }
            results.append(result)
            
            if not comment_already_exists:
                # Add comment to the recording
                add_comment_url = f"https://3.basecampapi.com/{company_id}/buckets/{project_id}/recordings/{recording_id}/comments.json"
                
                comment_payload = {
                  "content": "<div> @Matthijs Brouns , @Rick Vergunst , @Wesley Boelrijk , @Gary Clark : New email received </div>"
                   # Example comment text mentioning AmaniAttia
                }

                # Make a POST request to create the comment
                response = session.post(add_comment_url, json=comment_payload, headers=headers)
                response.raise_for_status()  # Raise an exception for non-200 status codes
                logging.info("Comment added successfully.")
        
        logging.info("Processing completed.")

    except requests.RequestException as e:
        logging.error(f"Failed to retrieve email forwards: {str(e)}")
        return e
 