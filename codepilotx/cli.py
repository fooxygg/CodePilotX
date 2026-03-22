import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich import print as rprint
from . import client, config as cfg, __version__

app = typer.Typer(help="CodePilotX - Local AI Coding Copilot", add_completion=False)
console = Console()


def _stream_print(prompt: str, system: str = ""):
    full = ""
    with console.status("[bold green]Pensando...[/]", spinner="dots"):
        first = True
        output = ""
        for token in client.chat_stream(prompt, system):
            if first:
                console.print()
                first = False
            output += token
    console.print(Markdown(output))


@app.command()
def chat(
    message: str = typer.Argument(None, help="Mensaje directo (opcional)"),
):
    """Chat interactivo con el copilot."""
    conf = cfg.load()
    server = conf["server_url"]
    model = conf["model"]

    if not client.ping():
        rprint(f"[red]No se puede conectar a {server}[/]")
        rprint("[yellow]Verifica que Ollama este corriendo o configura el server: cpx config server <url>[/]")
        raise typer.Exit(1)

    if message:
        _stream_print(message)
        return

    rprint(f"[bold cyan]CodePilotX[/] [dim]v{__version__}[/] | modelo: [green]{model}[/] | servidor: [dim]{server}[/]")
    rprint("[dim]Escribe tu pregunta. /exit para salir, /clear para limpiar.[/]\n")

    while True:
        try:
            msg = Prompt.ask("[bold cyan]>[/]")
        except (KeyboardInterrupt, EOFError):
            rprint("\n[dim]Saliendo...[/]")
            break

        if msg.strip() in ("/exit", "/quit", "exit", "quit"):
            break
        if msg.strip() == "/clear":
            console.clear()
            continue
        if not msg.strip():
            continue

        _stream_print(msg)


@app.command()
def ask(message: str = typer.Argument(..., help="Pregunta one-shot")):
    """Una pregunta rapida sin modo interactivo."""
    if not client.ping():
        rprint("[red]Servidor no disponible.[/]")
        raise typer.Exit(1)
    _stream_print(message)


@app.command()
def serve(
    port: int = typer.Option(4444, help="Puerto donde escucha el servidor"),
    host: str = typer.Option("0.0.0.0", help="Host"),
):
    """Inicia el servidor en TU PC para conectarte desde VPS u otro lugar."""
    from .server import start
    start(host=host, port=port)


@app.command()
def config(
    key: str = typer.Argument(..., help="server | model | api-key"),
    value: str = typer.Argument(..., help="Valor a configurar"),
):
    """
    Configura el copilot.

    Ejemplos:\n
      cpx config server http://TU_IP:4444\n
      cpx config model mi-coder\n
      cpx config api-key mi_clave_secreta
    """
    key_map = {"server": "server_url", "model": "model", "api-key": "api_key"}
    real_key = key_map.get(key, key)
    cfg.set_value(real_key, value)
    rprint(f"[green]Configurado:[/] {real_key} = {value}")


@app.command()
def status():
    """Muestra el estado actual y configuracion."""
    conf = cfg.load()
    online = client.ping()
    estado = "[green]ONLINE[/]" if online else "[red]OFFLINE[/]"

    rprint(f"\n  [bold]CodePilotX[/] v{__version__}")
    rprint(f"  Servidor : {conf['server_url']} {estado}")
    rprint(f"  Modelo   : {conf['model']}")
    rprint(f"  API Key  : {'[green]configurada[/]' if conf['api_key'] else '[dim]no configurada[/]'}\n")


def main():
    app()
