import os
from app.utils.logger import logger
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


def get_valid_credentials(user, db):

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )

    if not credentials.valid:

        logger.info(
            f"Refreshing Gmail token for {user.email}"
        )

        try:
            credentials.refresh(Request())

            user.access_token = credentials.token

            db.commit()

            logger.info(
                f"Gmail token refreshed for {user.email}"
            )

        except Exception as e:

            logger.error(
                f"Token refresh failed for {user.email}: {str(e)}"
            )

            raise
    return credentials