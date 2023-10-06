import os
from typing import Dict, Iterable, Optional, Sequence, Union
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.models.blocks import Block


def build_message(
    websites: Iterable[Iterable[str]],
    checked_time: str,
) -> Sequence[Dict]:
    return (
        # Mention
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "@channel",
            },
        },
        # Title
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":alert_party: Alert about connection status to the site\n サイトへの接続状況のアラート",
            },
        },
        # Summary
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "\n".join(
                    (
                        "You received this message because it is currently unable to access these following sites.",
                        "以下のサイトへのアクセスができていないため、このメッセージが配信されました。",
                    )
                ),
            },
        },
        # Websites list
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n".join(
                    (
                        f"> {index}. {site_name}：{site_url}"
                        for (index, (site_name, site_url)) in enumerate(
                            websites, start=1
                        )
                    )
                ),
            },
        },
        # Checked time
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": f"Checked at/確認時点：{checked_time}",
            },
        },
        # Conclusion
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Please have a check./ご確認をお願いします。",
            },
        },
    )


def send_message(
    channel_id: str,
    blocks: Optional[Union[str, Sequence[Union[Dict, Block]]]],
):
    load_dotenv()
    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    client.chat_postMessage(channel=channel_id, blocks=blocks)
