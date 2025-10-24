import asyncio
from langchain.agents import create_agent
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
try:
    
    from .mcp_server import mcp_client
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from mcp_server import mcp_client
import argparse
import json
try:
    
    from .prompt import PAPER_ANALYSIS_PROMPT
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from prompt import PAPER_ANALYSIS_PROMPT

from dotenv import load_dotenv

load_dotenv('.env')

console = Console()

def setup_parser():
    parser = argparse.ArgumentParser(
        description="Agent CLI with MCP Tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  python agent.py\n  python agent.py --model anthropic:claude-3-5-sonnet-latest\n  python agent.py --query 'What is the weather?'"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="anthropic:claude-3-5-sonnet-latest",
        help="Model to use for the agent (default: anthropic:claude-3-5-sonnet-latest)"
    )
    
    parser.add_argument(
        "--query",
        type=str,
        help="Single query to run and exit (optional interactive mode if not provided)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--tools-limit",
        type=int,
        default=5,
        help="Number of tools to display in table (default: 5)"
    )
    
    return parser.parse_args()

def format_message_content(content):
    """Convert message content to a renderable string."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # Handle content arrays with text and tool_use blocks
        formatted = []
        for block in content:
            if isinstance(block, dict):
                if block.get('type') == 'text':
                    formatted.append(block.get('text', ''))
                elif block.get('type') == 'tool_use':
                    tool_info = f"\n[bold cyan]Tool:[/bold cyan] {block.get('name', 'Unknown')}"
                    if 'input' in block:
                        tool_info += f"\n[cyan]Input:[/cyan]\n{json.dumps(block['input'], indent=2)}"
                    formatted.append(tool_info)
            else:
                formatted.append(str(block))
        return '\n'.join(formatted)
    else:
        return str(content)

async def main():
    args = setup_parser()
    
    console.print(
        Panel(
            "[bold cyan]🤖 Agent CLI with MCP Tools ⛏️[/bold cyan]",
            expand=False,
            style="bold blue"
        )
    )
    
    # fetch tools asynchronously
    console.print("\n[yellow]Initializing MCP client...[/yellow]")
    with console.status("[bold green]Loading client...[/bold green]", spinner="dots"):
        client = await mcp_client()
        tools = await client.get_tools()
    
    console.print(f"[green]✓ Loaded {len(tools)} tools[/green]\n")
    
    # Display available tools
    if tools:
        table = Table(title="Available Tools", show_header=True, header_style="bold magenta")
        table.add_column("Tool Name", style="cyan")
        table.add_column("Description", style="white")
        
        for tool in tools[:args.tools_limit]:
            name = getattr(tool, 'name', 'Unknown')
            desc = getattr(tool, 'description', 'No description')[:50]
            table.add_row(name, desc)
        
        if len(tools) > args.tools_limit:
            table.add_row("[dim]...[/dim]", f"[dim]and {len(tools) - args.tools_limit} more[/dim]")
        
        console.print(table)
    
    # create agent with tools
    console.print(f"\n[yellow]Initializing agent with model: {args.model}[/yellow]")
    with console.status("[bold green]Setting up agent[/bold green]", spinner="dots"):
        agent = create_agent(args.model, tools, system_prompt=PAPER_ANALYSIS_PROMPT)
    
    console.print("[green]✓ Agent ready![/green]\n")
    
    # Single query mode
    if args.query:
        console.print(f"[cyan]Query:[/cyan] {args.query}\n")
        with console.status("[bold green]Processing...[/bold green]", spinner="dots"):
            result = await agent.ainvoke({"messages": [{"role": "user", "content": args.query}]})
        
        console.print("\n[bold green]Response:[/bold green]\n")
        
        for message in result["messages"]:
            role = getattr(message, 'type', 'unknown').upper()
            content = getattr(message, 'content', str(message))
            formatted_content = format_message_content(content)
            
            if role == 'HUMAN':
                console.print(Panel(formatted_content, title="[cyan]User[/cyan]", style="cyan"))
            elif role == 'AI':
                console.print(Panel(formatted_content, title="[green]Agent[/green]", style="green"))
            else:
                console.print(Panel(formatted_content, title=f"[yellow]{role}[/yellow]", style="yellow"))
        
        console.print("\n[dim]Papers downloaded at: C:\\arxiv_storage[/dim]")
        return
    
    # Interactive loop mode
    console.print("[dim]Type 'exit', 'quit', or 'q' to quit • 'help' for commands[/dim]\n")
    
    while True:
        try:
            query = console.input("[bold cyan]Enter a Query:[/bold cyan] ").strip()
            
            if not query:
                console.print("[yellow]Empty query, try again.[/yellow]")
                continue
            
            if query.lower() in ['exit', 'quit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if query.lower() == 'help':
                console.print(Panel(
                    "[cyan]Commands:[/cyan]\n"
                    "  exit, quit, q  - Exit the application\n"
                    "  help           - Show this help message",
                    title="[bold]Help[/bold]",
                    style="blue"
                ))
                continue
            
            console.print()
            with console.status("[bold green]Processing...[/bold green]", spinner="dots"):
                result = await agent.ainvoke({"messages": [{"role": "user", "content": query}]})
            
            console.print("\n[bold green]Response:[/bold green]\n")
            
            for message in result["messages"]:
                role = getattr(message, 'type', 'unknown').upper()
                content = getattr(message, 'content', str(message))
                formatted_content = format_message_content(content)
                
                if role == 'HUMAN':
                    console.print(Panel(formatted_content, title="[cyan]User[/cyan]", style="cyan"))
                elif role == 'AI':
                    console.print(Panel(formatted_content, title="[green]Agent[/green]", style="green"))
                else:
                    console.print(Panel(formatted_content, title=f"[yellow]{role}[/yellow]", style="yellow"))
            
            console.print("\n[dim]Papers downloaded at: C:\\arxiv_storage[/dim]\n")
            console.print()
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user.[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            if args.verbose:
                console.print_exception()

if __name__ == "__main__":
    asyncio.run(main())