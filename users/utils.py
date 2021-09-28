from datetime import datetime
from django.conf import settings
from responses.models import UserResponse
from users.models import UserImage


class UserUtils:

    @staticmethod
    def get_user_data(user):
        user_data = {'dob':''}
        user_data['email'] = user.email
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        if user.dob:
            user_data['dob'] = user.dob.strftime("%m-%d-%Y")
        user_data['phone_number'] = user.phone_number
        user_data['state'] = user.state

        images = UserImage.objects.filter(user=user)
        user_data['images'] = [f"{settings.BE_DOMAIN}{image.image.url}" for image in images]

        responses = UserResponse.objects.filter(user=user)
        question_responses = {}
        for response in responses:
            question_responses[response.question_id] = response.answers
        user_data['question_responses'] = question_responses
        return user_data

