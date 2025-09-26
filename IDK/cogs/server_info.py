import discord
from discord.ext import commands
from discord import app_commands
from config_info import stored_channel_ids  

class ServerHelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="server_help",
        description="Get links to the configured server channels"
    )
    async def server_help(self, interaction: discord.Interaction):
        guild = interaction.guild

        info_channel = guild.get_channel(stored_channel_ids.get("information", 0))
        announce_channel = guild.get_channel(stored_channel_ids.get("announcement", 0))
        support_channel = guild.get_channel(stored_channel_ids.get("support", 0))

        embed = discord.Embed(
            title="Server Help Directory",
            description="Use the buttons below to quickly jump to important channels.",
            color=discord.Color.blurple()
        )

        view = discord.ui.View()
        has_buttons = False
        
        if info_channel:
            embed.add_field(name="Information", value=info_channel.mention, inline=False)
            view.add_item(discord.ui.Button(
                label="Information Channel",
                url=f"https://discord.com/channels/{guild.id}/{info_channel.id}"
            ))
            has_buttons = True
            
        if announce_channel:
            embed.add_field(name="Announcements", value=announce_channel.mention, inline=False)
            view.add_item(discord.ui.Button(
                label="Announcements Channel",
                url=f"https://discord.com/channels/{guild.id}/{announce_channel.id}"
            ))
            has_buttons = True
            
        if support_channel:
            embed.add_field(name="Support Channel", value=support_channel.mention, inline=False)
            view.add_item(discord.ui.Button(
                label="Support Channel",
                url=f"https://discord.com/channels/{guild.id}/{support_channel.id}"
            ))
            has_buttons = True
            
        if has_buttons:
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await interaction.response.send_message(
                "No channels are currently configured. Please run `/config_information` first.",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(ServerHelpCog(bot))
