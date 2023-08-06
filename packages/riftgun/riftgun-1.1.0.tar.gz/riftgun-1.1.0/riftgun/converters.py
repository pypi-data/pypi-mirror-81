import discord
from discord.ext import commands


class GlobalConverter(commands.Converter):
    """The ABC class for global converters"""

    async def convert(self, ctx: commands.Context, argument: str):
        raise NotImplementedError

    @staticmethod
    def convertSync(ctx: commands.Context, argument: str):
        raise NotImplementedError


class GlobalTextChannel(GlobalConverter):
    """A converter that attempts to find the closest match to the provided channel."""

    async def convert(self, ctx, argument: str) -> discord.TextChannel:
        # this method only exists so that you can actually use it as a converter
        try:
            return await commands.TextChannelConverter().convert(ctx, argument)
        except commands.BadArgument:
            pass
        return self.convertSync(ctx, argument)

    @staticmethod
    def convertSync(ctx, argument: str) -> discord.TextChannel:
        """Converts a provided argument to a text channel."""

        if argument.isdigit(): argument = int(argument)

        def match(channel):
            if not isinstance(channel, discord.TextChannel):
                # ok, so, somehow this is being bypassed and is returning a voice channel. Not sure why.
                return False
            if channel.id == argument:
                return True
            else:
                arg = str(argument)
                if channel.name.lower() == str(arg).lower():
                    return True
                elif channel.name in arg:
                    return True
                elif arg in channel.name:
                    return True

        channel = discord.utils.find(match, sorted(list(ctx.bot.get_all_channels()), key=lambda x: x.id))

        if channel:
            return channel
        else:
            raise commands.BadArgument(f"Unable to convert \"{argument}\" to TextChannel, globally or locally.")


class GuildConverter(GlobalConverter):
    """Converts a provided guild name/id into a discord.Guild.

    Feel free to use this in your own projects."""

    @staticmethod
    def convertSync(ctx: commands.Context, argument: str):
        for guild in ctx.bot.guilds:
            if str(guild.id) == argument:
                return guild
            elif guild.name.lower() == argument.lower():
                return guild
            elif guild.name.lower() in argument.lower():
                return guild
            elif argument.lower() in guild.name.lower():
                return guild
            else:
                continue
        raise commands.BadArgument(f"Unable to convert \"{argument}\" to guild.")

    async def convert(self, ctx: commands.Context, argument: str):
        return self.convertSync(ctx, argument)
