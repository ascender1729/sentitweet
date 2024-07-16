import sys
from src.cli import run_cli
from src.web_app import run_web_app
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama

def print_cool_intro():
    ascii_art = r"""
 ____                   __        ______                           __      
/\  _`\                /\ \__  __/\__  _\                         /\ \__   
\ \,\L\_\     __    ___\ \ ,_\/\_\/_/\ \/ __  __  __     __     __\ \ ,_\  
 \/_\__ \   /'__`\/' _ `\ \ \/\/\ \ \ \ \/\ \/\ \/\ \  /'__`\ /'__`\ \ \/  
   /\ \L\ \/\  __//\ \/\ \ \ \_\ \ \ \ \ \ \ \_/ \_/ \/\  __//\  __/\ \ \_ 
   \ `\____\ \____\ \_\ \_\ \__\\ \_\ \ \_\ \___x___/'\ \____\ \____\\ \__\
    \/_____/\/____/\/_/\/_/\/__/ \/_/  \/_/\/__//__/   \/____/\/____/ \/__/
"""
    print(Fore.CYAN + ascii_art)
    print(Fore.GREEN + "Welcome to SentiTweet - Advanced Sentiment Analysis Tool!" + Style.RESET_ALL)
    print(Fore.YELLOW + "Version: 0.1.0" + Style.RESET_ALL)
    print(Fore.MAGENTA + "Created by: Pavan Kumar" + Style.RESET_ALL)
    print("\n" + Fore.WHITE + "Analyzing sentiments with the power of AWS Comprehend and TextBlob!" + Style.RESET_ALL)
    print("\n" + Fore.BLUE + "=" * 60 + Style.RESET_ALL)

def main():
    print_cool_intro()
    
    if len(sys.argv) > 1:
        print(Fore.GREEN + "Running in CLI mode..." + Style.RESET_ALL)
        run_cli()
    else:
        print(Fore.GREEN + "Starting web application..." + Style.RESET_ALL)
        run_web_app()

if __name__ == "__main__":
    main()