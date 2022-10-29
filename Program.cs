using Discord;
using Discord.Interactions;
using Discord.WebSocket;
using Discord.Commands;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Configuration.Json;

using Saliva.Bot;
using Saliva.Modules;

namespace Saliva.Main;

public class Bot
{
    public static Task Main() => new Bot().MainAsync();

    /*private ServiceProvider ConfigureServices() => 
        new ServiceCollection()
            .AddSingleton<DiscordSocketClient>()*/
    public async Task MainAsync()
    {
        var config = new ConfigurationBuilder()
            .SetBasePath(Directory.GetCurrentDirectory())
            .AddJsonFile("config.json")
            .Build();

        using IHost host = Host.CreateDefaultBuilder()
            .ConfigureServices((_, services) =>
            services
            .AddSingleton(config)
            // Add the DiscordSocketClient, along with specifying the GatewayIntents and user caching
            .AddSingleton(x => new DiscordSocketClient(new DiscordSocketConfig
            {
                GatewayIntents = GatewayIntents.AllUnprivileged,
                AlwaysDownloadUsers = true
            }))
            .AddSingleton(x => new InteractionService(x.GetRequiredService<DiscordSocketClient>()))
            .AddSingleton<InteractionHandler>()
            .AddSingleton(x => new CommandService())
            .AddSingleton<PrefixHandler>()
            )
            .Build();
        await RunAsync(host);
    }

    public async Task RunAsync(IHost host)
    {
        using IServiceScope serviceScope = host.Services.CreateScope();
        IServiceProvider provider = serviceScope.ServiceProvider;

        var _client = provider.GetRequiredService<DiscordSocketClient>();
        var sCommands = provider.GetRequiredService<InteractionService>();
        await provider.GetRequiredService<InteractionHandler>().InitializeAsync();
        var config = provider.GetRequiredService<IConfigurationRoot>();
        var pCommands = provider.GetRequiredService<PrefixHandler>();
        pCommands.AddModule<Saliva.Modules.PrefixModule>();
        await pCommands.InitializeAsync();


        // Subscribe to client log events
        _client.Log += async (LogMessage msg) => { Console.WriteLine(msg.Message); };
        sCommands.Log += async (LogMessage msg) => { Console.WriteLine(msg.Message); };

        _client.Ready += async () =>
        {
            Console.WriteLine("Bot Ready!");
            await sCommands.RegisterCommandsToGuildAsync(UInt64.Parse(config["testGuild"]));
        };

        await _client.LoginAsync(TokenType.Bot, config["tokens:discord"]);
        await _client.StartAsync();

        await Task.Delay(-1);
    }
}


