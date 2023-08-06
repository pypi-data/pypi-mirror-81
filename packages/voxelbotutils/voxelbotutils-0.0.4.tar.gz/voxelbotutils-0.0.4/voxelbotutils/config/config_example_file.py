config_file = """
token = "bot_token"  # The token for the bot
topgg_token = ""  # The token used to post data to top.gg
owners = [ 141231597155385344, ]  # The first should always be the developer
dm_uncaught_errors = false  # Whether or not to DM the owners when errors are encountered
default_prefix = "!"  # The prefix for the bot's commands
guild_id = 0  # The ID of the main/support guild
event_webhook_url = ""  # Some events will be posted via webhook to this url

# Data that's copied directly over to a command
[command_data]
    guild_invite = ""  # A link to be used on !support
    github_link = ""  # A link to be used on !git
    donate_link = ""  # A link to be used on !donate
    invite_command_permissions = []  # args here are passed directly to discord.Permissions. An empty list disabled the invite command
    echo_command_enabled = true  # Whether or not the invite command is enabled
    stats_command_enabled = true  # Whether or not the stats command is enabled
    vote_command_enabled = false  # Whether or not the top.gg vote command is enabled
    updates_channel_id = 0  # The ID of the news channel for the bot

# This data is passed directly over to asyncpg.connect()
[database]
    user = "database_username"
    password = "database_password"
    database = "database_name"
    host = "127.0.0.1"
    port = 5432
    enabled = false

# This data is passed directly over to aioredis.connect()
[redis]
    host = "127.0.0.1"
    port = 6379
    db = 0
    enabled = false

# The data that gets shoves into custom context for the embed
[embed]
    enabled = false  # whether or not to embed messages by default
    content = ""  # default content to be added to the embed message
    colour = 0  # a specific colour for the embed - 0 means random
    [embed.author]
        enabled = false
        name = "{ctx.bot.user}"
        url = ""  # the url added to the author
    [[embed.footer]]  # an array of possible footers
        text = "Add the bot to your server! ({ctx.clean_prefix}invite)"  # text to appear in the footer
        amount = 1  # the amount of times this particular text is added to the pool

# What the bot is playing
[presence]
    activity_type = "watching"  # Should be one of 'playing', 'listening', 'watching', 'competing'
    text = "VoxelBotUtils"
    status = "online"  # Should be one of 'online', 'invisible', 'idle', 'dnd'

# Used to generate the invite link - if not set then will use the bot's ID, which is correct more often than not
[oauth]
    client_id = ""

# This is where you can set up all of your analytics to be sent to GA
[google_analytics]
    tracking_id = ""  # Tracking ID for your GA instance
    app_name = ""  # The name of your bot - what you want GA to name this traffic source
    document_host = ""  # The (possibly fake) URL you want to tell GA this website is
"""
