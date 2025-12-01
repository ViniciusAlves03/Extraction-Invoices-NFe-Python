class Strings:
    APP = {
        "TITLE": 'Extraction Service API',
        "APP_DESCRIPTION": 'Micro-service for data extraction.'
    }

    ERROR_MESSAGE = {
        "UNEXPECTED": 'An unexpected error has occurred. Please try again later...',
        "INTERNAL_SERVER_ERROR": 'An internal server error has occurred.',

        "VALIDATE": {
            "REQUIRED_FIELDS": 'Required fields were not provided...',
            "INVALID_FIELDS": 'One or more request fields are invalid...',
            "UUID_NOT_VALID_FORMAT": 'The ID provided does not have a valid format!',
            "INVALID_DATE_FORMAT": 'Date: {0}, is not in valid format.'
        },

        "FILE": {
            "NOT_SUPPORTED": "File format {0} is not supported.",
            "EMPTY": "The uploaded file is empty."
        }
    }
