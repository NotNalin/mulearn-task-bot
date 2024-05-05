import discord
from discord.ext import commands
from discord import app_commands

ROLES = ["Red", "Green", "Blue"]


class Role(discord.ui.Select):
    """ Select menu with callback handler """
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="Red", description="Red colour role", emoji="🟥"),
            discord.SelectOption(label="Green", description="Green colour role", emoji="🟩"),
            discord.SelectOption(label="Blue", description="Blue colour role", emoji="🟦"),
        ]
        super().__init__(
            placeholder="Choose your role colour...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name=self.values[0])
        if role:
            try:
                for i in interaction.user.roles:
                    if i.name in ROLES and i != role:
                        await interaction.user.remove_roles(i) # Remove all roles in ROLES that are not the selected role
                await interaction.user.add_roles(role)
                self.bot.db.execute(
                    "INSERT INTO user_role (discord_id, role_id) VALUES (:discord_id, :role_id)",
                    {"discord_id": interaction.user.id, "role_id": role.id},
                )
                await interaction.response.send_message(f"You chose the role {self.values[0]}", ephemeral=True)
            except discord.errors.Forbidden:
                await interaction.response.send_message("I don't have permission to add roles to you", ephemeral=True)
        else:
            await interaction.response.send_message("I couldn't find that role", ephemeral=True)


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="select_role", description="Sends a select menu for you to pick a role")
    async def select_role(self, interaction: discord.Interaction):
        view = discord.ui.View()
        view.add_item(Role(self.bot))
        await interaction.response.send_message(view=view)


async def setup(bot):
    await bot.add_cog(Roles(bot))
