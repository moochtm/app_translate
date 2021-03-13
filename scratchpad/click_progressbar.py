import click
import time

if __name__ == "__main__":
    click.echo("This is unstyled text")
    click.echo(
        click.style("Red ", fg="red") +
        click.style("Green ", fg="green") +
        click.style("Blue ", fg="blue") +
        "Unstyled"
    )

    click.secho("BOLD yellow text", fg="yellow", bold=True)
    click.secho(
        "Underlined magenta text", fg="magenta", underline=True)
    click.secho(
        "BOLD underlined cyan text",
        fg="cyan", bold=True, underline=True)

    click.secho(
        "BOLD white foreground with ugly cyan background",
        bold=True, bg="cyan")

    """
    Demonstrates a progress bar without an iterable to
    iterate over.
    """
    length = 400
    with click.progressbar(label="Processing",
                           length=length,
                           show_eta=True,
                           show_pos=True,
                           show_percent=True) as progress_bar:
        click.echo("Starting progress bar")
        progbar_pos = 0
        while progbar_pos < length:
            progress_bar.update(1)
            time.sleep(0.05)
            progbar_pos = progbar_pos + 1
            # print(current)


    """
    Demonstrates how a progress bar can be tied to processing of
    an iterable.
    """

    # Could be a list, tuple and a whole bunch of other containers
    iterable = range(256)

    label_text = "Processing items in the iterable..."

    with click.progressbar(iterable, label=label_text) as items:
        for item in items:
            # Do some processing
            time.sleep(0.023) # This is really hard work

