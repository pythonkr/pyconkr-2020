
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAdapter(DefaultSocialAccountAdapter):
    def populate_user(self,
                      request,
                      sociallogin,
                      data):
        user = super(SocialAdapter, self).populate_user(
            request, sociallogin, data)
        if user.username:
            return user
        # If username is empty, use email instead
        email = user.email
        emailtouname = email.split(
            '@')[0] + "_" + email.split('@')[1].split('.')[0]
        user.username = emailtouname
        return user
