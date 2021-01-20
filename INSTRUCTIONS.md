# Instructions
This is a two-part setup. You must complete the **Initial Setup** section and one of the options from **Web Server**

## Initial Setup
[ ] - www.api.slack.com, click **Your Apps** in top-right of screen
[ ] - App Home, Edit Bot (Name: MatchMaker, username: matchmaker)
[ ] - **OAuth & Permissions**, Add Workspace to Create OAuth Access Token
[ ] - In repository, edit the `.env` file and paste token to `SLACK_TOKEN` environment variable
[ ] - In the **Basic Information** tab, copy **Signing Secret** and put in `SIGNING_SECRET` variable in `.env`
[ ] - In Slack, you should see MatchMaker

## Web Server
### Heroku or DigitalOcean droplet (deployment):
- [ ] In 'Your Apps' on slackapi website, click Event Subscriptions and enable
- [ ] Use link associated with your instance in the following format `MY_INSTANCE_URL.COM/slack/events`

### Ngrok local instance (development)
**Must be repeated every time launching temporary local webserver**
- [ ] run `ngrok http <PORT>`, where `<PORT>` matches port the indicated by flask when running `bot.py`
- [ ] copy one of the `Forwarding` links on the left side of the `->`
- [ ] paste into your app's Event Subscriptions in the format `FORWARDING_URL/slack/events`