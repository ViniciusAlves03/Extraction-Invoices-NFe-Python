class Strings:
    APP = {
        "TITLE": 'Extraction Service API',
        "APP_DESCRIPTION": 'Service for data extraction.'
    }

    ERROR_MESSAGE = {
        "UNEXPECTED": 'An unexpected error has occurred. Please try again later...',
        "INTERNAL_SERVER_ERROR": 'An internal server error has occurred.',

        "VALIDATE": {
            "REQUIRED_FIELDS": 'Required fields were not provided...',
            "INVALID_FIELDS": 'One or more request fields are invalid...',
            "UUID_NOT_VALID_FORMAT": 'The ID provided does not have a valid format!',
            "INVALID_MONEY_FORMAT": 'Invalid monetary value: {0}',
            "MATH_INCONSISTENCY": 'Mathematical inconsistency: Qty ({0}) * Unit ({1}) = {2}, but Total is {3}',
            "REQUIRED_EXCEL_FIELDS": 'Required fields (Title or Total) are empty.'
        },

        "DATE": {
            "YEAR_NOT_ALLOWED": 'Date {0} has year not allowed. The year must be greater than 1678 and less than 2261.',
            "INVALID_DATE_FORMAT": 'Date: {0}, is not in valid format.'
        },

        "FILE": {
            "NOT_SUPPORTED": "File format {0} is not supported.",
            "EMPTY": "The uploaded file is empty.",
            "GENERIC_ERROR": "Error processing file: {0}"
        },

        "EXTRACTOR": {
            "EXCEL_ERROR": "Excel processing error: {0}",
            "GEMINI_ERROR": "Gemini AI processing error: {0}",
            "GEMINI_INVALID_DATA": "Invalid data returned by AI: {0}"
        }
    }
