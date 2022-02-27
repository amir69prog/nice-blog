from enum import Enum

class PostMessages(Enum):
    READING_TIME_HELP_TEXT = 'Please enter the reading time as `seconds`'
    POST_CREATED_SUCCESSFULLY = 'Your post has been created successfully.'
    POST_DELETED_SUCCESSFULLY = 'Your post has been deleted successfully.'
    POST_UPDATED_SUCCESSFULLY = 'Your post has been updated successfully.'