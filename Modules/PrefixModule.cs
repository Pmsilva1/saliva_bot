using Discord.Commands;
using Discord;

namespace Saliva.Modules;

public class PrefixModule : ModuleBase<SocketCommandContext>
{
    [Command("ping")]
    public async Task HadndlePingCommand()
    {
        await Context.Message.ReplyAsync("PING!");
    }
}