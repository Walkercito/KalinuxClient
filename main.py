from src.core.discovery import Core
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import print


console = Console()


def display_menu():
    console.print("\n[bold cyan]=== Device Menu ===[/bold cyan]")
    console.print("[green]1.[/green] List available devices")
    console.print("[green]2.[/green] Connect to device")
    console.print("[green]3.[/green] Exit")
    return Prompt.ask("Select option", choices=["1", "2", "3"], default="1")


if __name__ == "__main__":
    core = Core()
    core.send_discovery_response()
    core.start_discovery()

    console.print("[bold green]Core started. Use the menu to interact.[/bold green]")
    while True:
        
        try:
            choice = display_menu()
            if choice == "1":
                console.print("\n[bold cyan]Available devices:[/bold cyan]")
                devices = core.list_available_devices()
                
                if isinstance(devices, str): 
                    devices = [devices]
                
                if devices:
                    table = Table(title="Devices")
                    table.add_column("Index", style="bold green")
                    table.add_column("Device Name", style="bold cyan")
                    for idx, device in enumerate(devices, start=1):
                        table.add_row(str(idx), device)
                    console.print(table)
                
                else:
                    console.print("[yellow]No devices found.[/yellow]")
            
            elif choice == "2":
                console.print("\n[bold cyan]Available devices:[/bold cyan]")
                devices = core.list_available_devices()
                
                if isinstance(devices, str):
                    devices = [devices]
                
                if devices:
                    table = Table(title="Devices")
                    table.add_column("Index", style="bold green")
                    table.add_column("Device Name", style="bold cyan")
                    
                    for idx, device in enumerate(devices, start=1):
                        table.add_row(str(idx), device)
                    console.print(table)
                    peer_idx = Prompt.ask("Enter device number to connect", 
                                          choices=[str(i + 1) for i in range(len(devices))])
                    
                    if core.connect_to_peer(int(peer_idx) - 1):
                        console.print("[bold green]Connection established![/bold green]")
                    
                    else:
                        console.print("[bold red]Invalid device selection.[/bold red]")
                
                else:
                    console.print("[yellow]No devices available to connect.[/yellow]")
            
            elif choice == "3":
                console.print("[bold yellow]Shutting down...[/bold yellow]")
                break
        
        except KeyboardInterrupt:
            console.print("\n[bold red]Core stopped.[/bold red]")
            break
        
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
