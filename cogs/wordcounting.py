import discord
from discord.ext import commands
from discord import app_commands


class WordCounting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Add words from message to database
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        words = message.content.split()
        for word in words:
            self.bot.db.execute(
                "INSERT INTO user_words (discord_id, word) VALUES (:discord_id, :word)", {"discord_id": message.author.id, "word": word}
            )

    @app_commands.command(description="Get the top 10 words used")
    async def word_status(self, interaction: discord.Interaction):
        result = self.bot.db.fetch_all("SELECT word, COUNT(*) as count FROM user_words GROUP BY word ORDER BY count DESC LIMIT 10")

        embed = discord.Embed(
            title="Word Status",
            description="\n".join([f"{row[0]}: {row[1]}" for row in result]),
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Get the top 10 words by an user")
    @discord.app_commands.describe(user="The user to get the status of")
    async def user_status(self, interaction, user: discord.Member = None):
        if user is None:
            user = interaction.user
        result = self.bot.db.fetch_all(
            "SELECT word, COUNT(*) as count FROM user_words WHERE discord_id = :discord_id GROUP BY word ORDER BY count DESC LIMIT 10",
            {"discord_id": user.id},
        )
        embed = discord.Embed(
            title=f"User Status of {user.name}",
            description="\n".join([f"{row[0]}: {row[1]}" for row in result]),
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(WordCounting(bot))
