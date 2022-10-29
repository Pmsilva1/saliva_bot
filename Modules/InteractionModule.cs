using Discord.Interactions;
using System.Drawing;

namespace Saliva.Modules;

public class InteractionModule : InteractionModuleBase<SocketInteractionContext>
{
    [SlashCommand("ping", "Receive a ping message!")]
    public async Task HandlePingCommand()
    {
        await RespondAsync("PING!");
    }

    [SlashCommand("meme","Creates a meme")]
    public async Task HandleMemeCommand(
        [Summary(description: "Insert the first line of the meme")] string text)
    {
        Image image = Image.FromFile("Memes/64sz4u.png"); //or .jpg, etc...
        Graphics graphics = Graphics.FromImage(image);
        Font font = new Font("Times New Roman", 26);
        graphics.DrawString(text, font, Brushes.White, 200, 0);
        image.Save("Memes/meme1.png", System.Drawing.Imaging.ImageFormat.Png);


        await Context.Channel.SendFileAsync("Memes/meme1.png");
    }
}