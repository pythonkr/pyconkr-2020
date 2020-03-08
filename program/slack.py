from slacker import Slacker
from constance import config


token = config.SLACK_TOKEN
CFP_CHANNEL = '#org-webservice'


def new_cfp_registered(title):
    if token:
        slack = Slacker(token)
        # color: danger(red), good(green)
        text = '안녕, 나는 알려주길 좋아하는 CFP-BOT! CFP에 바뀐 게 있어 AWS에서 따라왔지!'
        attachment = {
            "color": 'good',
            "title": '새로운 CFP가 등록되었습니다. :)',
            "text": '제목: {}'.format(title),
        }

        slack.chat.post_message(
            CFP_CHANNEL, text=text, attachments=[attachment],
            username='cfp-bot', icon_emoji=':female_mage:')


def cfp_updated(title):
    if token:
        slack = Slacker(token)
        # color: danger(red), good(green)
        text = '안녕, 나는 알려주길 좋아하는 CFP-BOT! CFP에 바뀐 게 있어 AWS에서 따라왔지!'
        attachment = {
            "color": 'good',
            "title": '수정된 CFP가 있습니다. :)',
            "text": '제목: {}'.format(title),
        }

        slack.chat.post_message(
            CFP_CHANNEL, text=text, attachments=[attachment], icon_emoji=':female_mage:'
        )