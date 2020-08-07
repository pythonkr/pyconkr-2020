from django.urls import reverse
from slacker import Slacker
from constance import config


token = config.SLACK_TOKEN
CFP_CHANNEL = config.SLACK_CHANNEL
CFS_CHANNEL = config.CFS_NOTI_CHANNEL


def new_cfp_registered(hostname, pk, title):
    if token:
        slack = Slacker(token)
        # color: danger(red), good(green)
        text = '안녕, 나는 알려주길 좋아하는 CFP-BOT! CFP에 바뀐 게 있어 AWS에서 따라왔지!'
        # url = URL_TEMPLATE.format(pk)
        url = hostname + reverse('admin:program_proposal_change', args=(pk,))

        attachment = {
            "color": 'good',
            "title": '새로운 CFP가 등록되었습니다. :)',
            "text": '제목: {}\n 주소: {}'.format(title, url),
        }

        slack.chat.post_message(
            CFP_CHANNEL, text=text, attachments=[attachment],
            username='cfp-bot', icon_emoji=':female_mage:')


def cfp_updated(hostname, pk, title):
    if token:
        slack = Slacker(token)
        # color: danger(red), good(green)
        text = '안녕, 나는 알려주길 좋아하는 CFP-BOT! CFP에 바뀐 게 있어 AWS에서 따라왔지!'
        # url = URL_TEMPLATE.format(pk)
        url = hostname + reverse('admin:program_proposal_change', args=(pk,))

        attachment = {
            "color": 'good',
            "title": '수정된 CFP가 있습니다. :)',
            "text": '제목: {}\n 주소: {}'.format(title, url),
        }

        slack.chat.post_message(
            CFP_CHANNEL, text=text, attachments=[attachment], icon_emoji=':female_mage:'
        )


def new_cfs_registered(hostname, pk, title):
    if token:
        slack = Slacker(token)
        # color: danger(red), good(green)
        text = '안녕, 나는 알려주길 좋아하는 CFS-BOT! 새로운 스폰서 신청이 있어 AWS에서 따라왔지!'
        # url = URL_TEMPLATE.format(pk)
        url = hostname + reverse('admin:sponsor_sponsor_change', args=(pk,))

        attachment = {
            "color": 'good',
            "title": '새로운 CFS가 등록되었습니다. :)',
            "text": '스폰서 이름: {}\n 주소: {}'.format(title, url),
        }

        slack.chat.post_message(
            CFS_CHANNEL, text=text, attachments=[attachment],
            username='cfs-bot', icon_emoji=':female_mage:')


def cfs_updated(hostname, pk, title):
    if token:
        slack = Slacker(token)
        # color: danger(red), good(green)
        text = '안녕, 나는 알려주길 좋아하는 CFS-BOT! 신청한 스폰서 내용 중 바뀐게 있어 AWS에서 따라왔지!'
        # url = URL_TEMPLATE.format(pk)
        url = hostname + reverse('admin:sponsor_sponsor_change', args=(pk,))

        attachment = {
            "color": 'good',
            "title": '수정된 CFS가 있습니다. :)',
            "text": '스폰서 이름: {}\n 주소: {}'.format(title, url),
        }

        slack.chat.post_message(
            CFS_CHANNEL, text=text, attachments=[attachment], icon_emoji=':female_mage:'
        )