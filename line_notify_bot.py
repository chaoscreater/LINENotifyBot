# -*- coding: utf-8 -*-


"""line_notify_bot.py

Send messages, images, or stickers to a LINE group via LINE Notify.
This bot can't accept messages, i.e., is not interactive.
"""


__author__ = 'morita'
__version__ = '1.0.0'
__date__ = '2019-05-03'
__update__ = '2019-05-03'


import requests


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='line_notify_bot.py',
        usage='python line_notify_bot.py -a path/to/access_token -m <messsage> -i path/to/image -sp <sticker package ID> -s <sticker ID>',
        description='Send messages, images, or stickers to a LINE group via LINE Notify.',
        epilog='end',
        add_help=True,
        )
    parser.add_argument(
        '-a', '--accesstoken',
        help='path to a file in which access token is written',
        action='store',
        required=True,
        )
    parser.add_argument(
        '-m', '--message',
        help='message to be sent',
        action='store',
        required=True,
        )
    parser.add_argument(
        '-i', '--image',
        help='image to be sent',
        action='store',
        required=False,
        default=None,
        )
    parser.add_argument(
        '-sp', '--stickerpackage',
        help='sticker package ID',
        type=int,
        action='store',
        required=False,
        default=None,
        )
    parser.add_argument(
        '-s', '--sticker',
        help='sticker ID',
        type=int,
        action='store',
        required=False,
        default=None,
        )
    args = parser.parse_args()
    access_token_path = args.accesstoken
    message = args.message
    image_path = args.image
    sticker_package_id = args.stickerpackage
    sticker_id = args.sticker

    """
    message = 'test'
    image_path = 'test.png'
    sticker_package_id = 1
    sticker_id = 13
    """

    with  open(access_token_path, 'r') as fin:
        access_token = fin.read().strip()
    bot = LINENotifyBot(access_token=access_token)
    bot.send(
        message,
        image=image_path,
        sticker_package_id=sticker_package_id,
        sticker_id=sticker_id
        )


class LINENotifyBot:
    """Sends message to LINE group if given its access token.

    Args:
        access_token (str):
            Access token necessary to tap LINE Notify API.

    Attributes:
        __headers (dict): Necessary to send request to LINE Notify.
        API_URL (str): URL of LINE Notify API.
    """
    API_URL = 'https://notify-api.line.me/api/notify'
    def __init__(self, access_token):
        self.__headers = {'Authorization': 'Bearer ' + access_token}

    def send(self, message, image=None, sticker_package_id=None, sticker_id=None):
        """Send message to LINE group designated by access token.

        Args:
            message (str): Sent message. Maximum length is 1000.
                If set to None, message can't be sent.
                In this situation, image and sticker also can't be sent.
            images (list): List of paths to figure you want to send.
                Available extentions are png or jpeg only.
                There is a limitation to the number of image files
                which can be sent in one hour (1,000 images default).
                Defaults to None.
            sticker_package_id (int): ID of sticker package.
                If set to None, only message is sent.
                If set to unregistered integer,
                even message can't be sent.
                Defaults to None.
            sticker_id (int): ID of sticker.
                If set to None, only message is sent.
                If set to unregistered integer,
                even message can't be sent.
                Defaults to None.
        """
        payload = {
                    'message': message,
                    'stickerPackageId': sticker_package_id,
                    'stickerId': sticker_id,
                    }
        files = {}
        if image != None:
            files = {'imageFile': open(image, 'rb')}
        line_notify = requests.post(
            LINENotifyBot.API_URL,
            headers=self.__headers,
            data=payload,
            files=files,
            )


if __name__ == '__main__':
    main()
