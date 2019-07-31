import os
import logging
import slack
import ssl as ssl_lib
import certifi
from onboarding_tutorial import OnboardingTutorial
from wiki_tutorial import WikiTutorial

onboarding_tutorials_sent = {}
wiki_tutorials_sent = {}


def prompt_start(web_client: slack.WebClient, user_id: str, channel: str):
    # Ask user to get started.
    web_client.chat_postMessage(
      channel=channel,
      text=":peanut: Hello there! Write 'hey, i'm new here' to get started."
    )

def start_onboarding(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new onboarding tutorial.
    onboarding_tutorial = OnboardingTutorial(channel)

    # Get the onboarding message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the onboarding message in Slack
    response = web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    onboarding_tutorial.timestamp = response["ts"]

    # Store the message sent in onboarding_tutorials_sent
    if channel not in onboarding_tutorials_sent:
        onboarding_tutorials_sent[channel] = {}
    onboarding_tutorials_sent[channel][user_id] = onboarding_tutorial

def start_wiki(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new onboarding tutorial.
    wiki_tutorial = WikiTutorial(channel)

    # Get the onboarding message payload
    message = wiki_tutorial.get_message_payload()

    # Post the onboarding message in Slack
    response = web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    wiki_tutorial.timestamp = response["ts"]

    # Store the message sent in onboarding_tutorials_sent
    if channel not in wiki_tutorials_sent:
        wiki_tutorials_sent[channel] = {}
    wiki_tutorials_sent[channel][user_id] = wiki_tutorial


# ================ Team Join Event =============== #
# When the user first joins a team, the type of the event will be 'team_join'.
# Here we'll link the onboarding_message callback to the 'team_join' event.
@slack.RTMClient.run_on(event=".team_join")
def onboarding_message(**payload):
    """Create and send an onboarding welcome message to new users. Save the
    time stamp of this message so we can update this message in the future.
    """
    # Get the id of the Slack user associated with the incoming event
    user_id = payload["data"]["user"]["id"]
    # Get WebClient so you can communicate back to Slack.
    web_client = payload["web_client"]

    # Open a DM with the new user.
    response = web_client.im_open(user=user_id)
    channel = response["channel"]["id"]

    # Post the onboarding message.
    start_onboarding(web_client, user_id, channel)


# ============= Reaction Added Events ============= #
# When a users adds an emoji reaction to the onboarding message,
# the type of the event will be 'reaction_added'.
# Here we'll link the update_emoji callback to the 'reaction_added' event.
@slack.RTMClient.run_on(event="reaction_added")
def update_emoji(**payload):
    """Update onboarding welcome message after receiving a "reaction_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data["item"]["channel"]
    user_id = data["user"]

    # Get the original tutorial sent.
    onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]

    # Mark the reaction task as completed.
    onboarding_tutorial.reaction_task_completed = True

    # Get the new message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the updated message in Slack
    updated_message = web_client.chat_update(**message)

    # Update the timestamp saved on the onboarding tutorial object
    onboarding_tutorial.timestamp = updated_message["ts"]

    all_done(onboarding_tutorial, channel_id)


# =============== Pin Added Events ================ #
# When a users pins a message the type of the event will be 'pin_added'.
# Here we'll link the update_pin callback to the 'reaction_added' event.
@slack.RTMClient.run_on(event="pin_added")
def update_pin(**payload):
    """Update onboarding welcome message after receiving a "pin_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data["channel_id"]
    user_id = data["user"]

    # Get the original tutorial sent.
    onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]

    # Mark the pin task as completed.
    onboarding_tutorial.pin_task_completed = True

    # Get the new message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the updated message in Slack
    updated_message = web_client.chat_update(**message)

    # Update the timestamp saved on the onboarding tutorial object
    onboarding_tutorial.timestamp = updated_message["ts"]

    all_done(onboarding_tutorial, channel_id)

# =============== Thread a message ================ #
# When a users threads a message, the event is a message of
# subtype message_replied.
@slack.RTMClient.run_on(event="message")
def update_thread(**payload):
    """Update onboarding welcome message after receiving a "pin_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    subtype = payload["data"].get("subtype")

    if subtype == "message_replied":

        data = payload["data"]
        web_client = payload["web_client"]
        channel_id = data.get("channel")
        user_id = data.get("message").get("replies")[0].get("user")

        # client = slack.WebClient(token=slack_token)
        # client.chat_postMessage(
        #   channel=channel_id,
        #   text="User id is %s\n Channel is %s" % (user_id, channel_id)
        # )

        # Get the original tutorial sent.
        onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]

        # Mark the pin task as completed.
        onboarding_tutorial.thread_task_completed = True

        # Get the new message payload
        message = onboarding_tutorial.get_message_payload()

        # Post the updated message in Slack
        updated_message = web_client.chat_update(**message)

        # Update the timestamp saved on the onboarding tutorial object
        onboarding_tutorial.timestamp = updated_message["ts"]

        all_done(onboarding_tutorial, channel_id)

# ============== All done event ============= #
def all_done(tutorial, channel):

    if tutorial.thread_task_completed & tutorial.pin_task_completed & tutorial.reaction_task_completed:

        client = slack.WebClient(token=slack_token)
        client.chat_postMessage(
          channel=channel,
          text="Congrats :tada:! You're done learning about slack :celebrate:. We depend heavily on slack here.\n Write 'Tell me about the lab' to continue."
        )

# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the update_share callback to the 'message' event.
@slack.RTMClient.run_on(event="message")
def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    # if text and text.lower() != "hey, i'm new here":
    #     return prompt_start(web_client, user_id, channel_id)

    if text and text.lower() == "hey, i'm new here":
        return start_onboarding(web_client, user_id, channel_id)

    if text and text.lower() == "tell me about the lab":
        return start_wiki(web_client, user_id, channel_id)


if __name__ == "__main__":
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()
