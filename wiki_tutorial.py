class WikiTutorial:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Now that you're familiar with Slack :slack:, let's introduce you to some other tools we use. :too_cool_for_school_parrot:\n\n\n"
                "*Continue by completing the steps below:*"
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
            f"{task_checkmark} *Subscribe to the Fraser lab calendar* :alarm_clock:\n"
            "We host our lab calendar on Google Calendar :google:, where you can find info on lab meetings, "
            "seminars, and happy hours :beers:.\n"
            "Slack Thomas to be added, and include the email account you would like added."
        )
        information = (
            ":information_source: *<https://calendar.google.com/calendar/r?cid=MDc2b2xlamQxaG9xYzlpbHQ5Y2ticnMwaTBAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ|"
            "Access Fraser Lab Calendar>*"
        )
        return self._get_task_block(text, information)

    def _get_wiki_block(self):
        task_checkmark = self._get_checkmark(self.wiki_task_completed)
        text = (
            f"{task_checkmark} *Access the lab wiki* :wikipedia:\n"
            "Info on the lab, resources, protocols, and computational guidance"
            " can be found on the wiki. Contributing to the wiki is an important duty for all labmembers."
            " Type `wiki` in a Direct Message to yourself for the link! "
            " After logging in to Medwiki using your SUnet credentials, slack Thomas for access to our wiki."
            ":information_source: *<https://app.slack.com/client/T03KX6SN3/C03KX6SP9/user_profile/W9ZFK3AG6"
            "|Learn How to Access a Stanford School of Medicine Medwiki>*"
        )
        information = (
            ":information_source: *<https://stanford.service-now.com/it_services?id=kb_article&sys_id=e6a0d3cc13c33e00d08ebda12244b0b2"
            "|Learn How to Access a Stanford School of Medicine Medwiki>*"
        )
        return self._get_task_block(text, information)

    def _get_quickstart_block(self):
        task_checkmark = self._get_checkmark(self.quickstart_task_completed)
        text = (
            f"{task_checkmark} *Read the Fraser lab quickstart guide* :sonic:\n"
            "Finish your onboarding by using the Fraser lab quickstart guide on our wiki. "
            " Here, you'll find more info to help get you set up, including information "
            " on lab ordering and using our computing resources."
        )
        information = (
            ":information_source: *<https://medwiki.stanford.edu/display/fraserlab/Fraser+Lab+Quickstart+Guide"
            "|Read our Quickstart Guide>*"
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
