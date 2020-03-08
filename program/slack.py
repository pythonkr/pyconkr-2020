from slacker import Slacker
from constance import config


token = config.SLACK_TOKEN
CFP_CHANNEL = '#org-webservice'
URL_TEMPLATE = 'https://pycon.kr/2020/admin/program/proposal/{}/change'


def new_cfp_registered(pk, title):
    if token:
        slack = Slacker(token)
        # color: danger(red), good(green)
        text = '안녕, 나는 알려주길 좋아하는 CFP-BOT! CFP에 바뀐 게 있어 AWS에서 따라왔지!'
        url = URL_TEMPLATE.format(pk)

        attachment = {
            "color": 'good',
            "title": '새로운 CFP가 등록되었습니다. :)',
            "text": '제목: {}\n 주소: {}'.format(title, url),
        }

        slack.chat.post_message(
            CFP_CHANNEL, text=text, attachments=[attachment],
            username='cfp-bot', icon_emoji=':female_mage:')


def cfp_updated(pk, title):
    if token:
        slack = Slacker(token)
        # color: danger(red), good(green)
        text = '안녕, 나는 알려주길 좋아하는 CFP-BOT! CFP에 바뀐 게 있어 AWS에서 따라왔지!'
        url = URL_TEMPLATE.format(pk)

        attachment = {
            "color": 'good',
            "title": '수정된 CFP가 있습니다. :)',
            "text": '제목: {}\n 주소: {}'.format(title, url),
        }

        slack.chat.post_message(
            CFP_CHANNEL, text=text, attachments=[attachment], icon_emoji=':female_mage:'
        )
