import os
from decouple import config


import discord
from discord.ext import commands
from discord import app_commands

from database.connection import DBConnection

COGS = ["cogs.welcome", "cogs.wordcounting", "cogs.roles"]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("."), intents=discord.Intents.all())
        self.db = DBConnection()
        self.db.execute("CREATE TABLE IF NOT EXISTS welcome(GUILD_ID BIGINT, CHANNEL_ID BIGINT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS user_words(discord_id BIGINT, word VARCHAR(255))")
        self.db.execute("CREATE TABLE IF NOT EXISTS user_role(discord_id BIGINT, role_id BIGINT)")

    async def setup_hook(self):
        for cog in COGS:
            await self.load_extension(cog)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        await bot.tree.sync()

    async def on_tree_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.errors.Forbidden):
            try:
                await interaction.response.send_message("I don't have permission to do that.", ephemeral=True)
            except discord.errors.InteractionResponded:
                await interaction.followup.send("I don't have permission to do that.", ephemeral=True)
        elif isinstance(error, discord.app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to do that.", ephemeral=True)
        else:
            raise error

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        await super().on_command_error(ctx, error)


bot = Bot()
bot.tree.on_error = bot.on_tree_error


@bot.tree.command(name="help", description="List of commands")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Help", description="List of commands")
    embed.add_field(
        name="Welcome",
        value="/set_welcome_channel [channel] - Set the welcome channel\n/remove_welcome_channel - Remove the welcome channel",
        inline=False,
    )
    embed.add_field(
        name="Word Counting",
        value="/word_status - Get the top 10 words used\n/user_status [user] - Get the top 10 words used by an user",
        inline=False,
    )
    embed.add_field(name="Roles", value="/select_role - Sends a select menu for you to pick a role", inline=False)
    await interaction.response.send_message(embed=embed)


bot.run(config("BOT_TOKEN"))
