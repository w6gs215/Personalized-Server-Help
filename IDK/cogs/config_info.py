import discord
from discord.ext import commands
from discord import app_commands

# THE SHARED DICT IS HERE
stored_channel_ids = {
    "information": None,
    "announcement": None,
    "support": None,
}

class ConfigDirectoryCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="config_information",
        description="Configure the Info Directory by selecting channels"
    )
    @app_commands.describe(
        information_channel="Select the Information Channel",
        announcement_channel="Select the Announcement Channel",
        support_channel="Select the Support Channel"
    )
    async def config_information(
        self,
        interaction: discord.Interaction,
        information_channel: discord.TextChannel,
        announcement_channel: discord.TextChannel,
        support_channel: discord.TextChannel
    ):
        stored_channel_ids["information"] = information_channel.id
        stored_channel_ids["announcement"] = announcement_channel.id
        stored_channel_ids["support"] = support_channel.id

        # Ephemeral reply in the same channel, only visible to user
        await interaction.response.send_message(
            "Server Directory setup! Run `/server_help` to see how it works!",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(ConfigDirectoryCog(bot))