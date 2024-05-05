import discord
from discord.ext import commands
from discord import app_commands


class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        guild = member.guild
        result = self.bot.db.fetch_one("SELECT CHANNEL_ID FROM welcome WHERE GUILD_ID = :guild_id", {"guild_id": guild.id})
        if result is None:
            return
        channel = self.bot.get_channel(result[0])
        try:

            embed = discord.Embed(
                title=f"Welcome {member.name}",
                description=f"We hope you enjoy your stay here",
                color=discord.Color.random(),
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(
                name="Account created at",
                value=f"{member.created_at.strftime('%d/%m/%Y')}",
                inline=False,
            )
            embed.add_field(name="Server member count", value=f"{guild.member_count}", inline=False)
            await channel.send(f"{member.mention}", embed=embed)

        except discord.errors.Forbidden:
            print(f"Couldn't send message in {channel}.")
        try:
            await member.send(f"Welcome to the server {guild.name}, {member.mention}!\nWe hope you enjoy your stay.")
        except discord.errors.Forbidden:
            print(f"Couldn't send message to {member}.")
        print(f"{member} has joined the server.")

    @app_commands.command(name="set_welcome_channel", description="Set the welcome channel")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.bot.db.execute(
            "INSERT INTO welcome (GUILD_ID, CHANNEL_ID) VALUES (:guild_id, :channel_id)",
            {"guild_id": interaction.guild.id, "channel_id": channel.id},
        )
        await interaction.response.send_message(f"Welcome channel set to {channel.mention}.", ephemeral=True)

    @app_commands.command(name="remove_welcome_channel", description="Remove the welcome channel")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_welcome_channel(self, interaction: discord.Interaction):
        self.bot.db.execute("DELETE FROM welcome WHERE GUILD_ID = :guild_id", {"guild_id": interaction.guild.id})
        await interaction.response.send_message("Welcome channel removed.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Welcome(bot))
