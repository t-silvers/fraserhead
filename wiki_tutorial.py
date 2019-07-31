class WikiTutorial:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Now that you're familiar with slack :slack:, let's introduce you to some other tools we use. :too_cool_for_school_parrot:\n\n"
                "*Get started by completing the steps below:*"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "Fraserhead"
        self.icon_emoji = ":rio_the_zonkey:"
        self.timestamp = ""
        self.calendar_task_completed = False
        self.wiki_task_completed = False
        self.quickstart_task_completed = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.WELCOME_BLOCK,
                self.DIVIDER_BLOCK,
                *self._get_calendar_block(),
                self.DIVIDER_BLOCK,
                *self._get_wiki_block(),
                self.DIVIDER_BLOCK,
                *self._get_quickstart_block(),
            ],
        }

    def _get_calendar_block(self):
        task_checkmark = self._get_checkmark(self.calendar_task_completed)
        text = (
            f"{task_checkmark} *Add an emoji reaction to this message* :thinking_face:\n"
            "You can quickly respond to any message on Slack with an emoji reaction. "
            "Reactions can be used for any purpose: voting, checking off to-do items, showing excitement."
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/206870317-Emoji-reactions|"
            "Learn How to Use Emoji Reactions>*"
        )
        return self._get_task_block(text, information)

    def _get_wiki_block(self):
        task_checkmark = self._get_checkmark(self.wiki_task_completed)
        text = (
            f"{task_checkmark} *Access the lab wiki* :wikipedia:\n"
            "Info on the lab, resources, protocols, and computational guidance"
            " can be found on the wiki. Please spend some time looking through it!"
            " Contributing to the wiki is an important duty for all labmembers."
            " Type `wiki` for the link!"
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/205239997-Pinning-messages-and-files"
            "|Learn How to Pin a Message>*"
        )
        return self._get_task_block(text, information)

    def _get_quickstart_block(self):
        task_checkmark = self._get_checkmark(self.quickstart_task_completed)
        text = (
            f"{task_checkmark} *Start a thread* :scroll:\n"
            "Threads keep discussions in Slack organized. A thread will remain connected to its original message, "
            " and only those that have contributed to it or who are following it will be notified of new replies. "
            "(Unless you check the box to the left of `Also send to #channel-name`.)"
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/115000769927-Use-threads-to-organize-discussions-#-start-or-reply-to-a-thread"
            "|Learn How to Start a Thread>*"
        )
        return self._get_task_block(text, information)

    @staticmethod
    def _get_checkmark(task_completed: bool) -> str:
        if task_completed:
            return ":hunter-yas:"
        return ":shiran:"

    @staticmethod
    def _get_task_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]
