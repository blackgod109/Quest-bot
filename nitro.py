import asyncio, os, random, requests, time, string
import zendriver as zd
from colorama import Fore, init
from pystyle import System, Center, Colorate, Colors

init(autoreset=True)

def log(token, tag, message, color=Fore.CYAN):
    t_short = f"{token[:10]}***"
    print(f"{Fore.WHITE}[INSAAN] {Fore.MAGENTA}{t_short} | {color}{tag.upper()} â€¢ {Fore.WHITE}{message}")

async def smog_trial_engine(token, semaphore):
    async with semaphore:
        headers = {
            "Authorization": token, 
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        v_check = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if v_check.status_code != 200:
            log(token, "INVALID", "Token is dead or locked", Fore.RED)
            return
        
        browser = await zd.start(headless=True)
        try:
            page = await browser.get("https://discord.com/login")
            await page.evaluate(f"window.localStorage.setItem('token', '\"{token}\"');")
            
            trigger_paths = [
                "https://discord.com/settings/nitro",
                "https://discord.com/settings/billing",
                "https://discord.com/settings/subscriptions",
                "https://discord.com/settings/gift-inventory",
                "https://discord.com/settings/appearance",
                "https://discord.com/settings/accessibility",
                "https://discord.com/settings/hypesquad-online",
                "https://discord.com/settings/profile",
                "https://discord.com/settings/friend-requests"
            ]
            
            for url in trigger_paths:
                await page.get(url)
                await asyncio.sleep(random.uniform(3.1, 6.4))
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight / random)")
                await page.evaluate("window.scrollTo(0, 0)")

            invites = ["discord-developers", "discord-testers", "discord-townhall"]
            target = random.choice(invites)
            await page.evaluate(f"""
                fetch('https://discord.com/api/v9/invites/{target}', {{
                    method: 'POST', headers: {{ 'Authorization': '{token}' }}
                }})
            """)

            requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json={"explicit_content_filter": 1, "render_embeds": True, "animate_emoji": True})
            requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers=headers)
            requests.get("https://discord.com/api/v9/users/@me/affinities/users", headers=headers)

            log(token, "SUCCESS", "25+ Signals Sent. Success Probability: 40-60%", Fore.GREEN)

        except Exception:
            log(token, "ERROR", "Process failed", Fore.RED)
        finally:
            await browser.stop()

async def main():
    System.Clear()
    banner = """
    â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ•—   â–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—  â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— 
    â–ˆâ–ˆâ•”â•â•â•â•â•â–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•”â•â•â•â•â• 
    â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ•”â–ˆâ–ˆâ–ˆâ–ˆâ•”â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ–ˆâ•—
    â•šâ•â•â•â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â•šâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘
    â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘ â•šâ•â• â–ˆâ–ˆâ•‘â•šâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•â•šâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•
    â•šâ•â•â•â•â•â•â•â•šâ•â•     â•šâ•â• â•šâ•â•â•â•â•â•  â•šâ•â•â•â•â•â• 
    TRIAL TRIGGER | MADE BY INSAAN
    """
    print(Colorate.Vertical(Colors.blue_to_purple, Center.XCenter(banner)))
    print(f"\n{Fore.RED}{Center.XCenter('!!! ATTENTION: MAKE SURE UR TOKENS ARE HUMANISED BEFORE TRIGGERING TRIALS !!!')}\n")

    if not os.path.exists("tokens.txt") or os.stat("tokens.txt").st_size == 0:
        print(f"{Fore.RED}tokens.txt")
        return

    tokens = open("tokens.txt").read().splitlines()
    sem = asyncio.Semaphore(2)
    
    tasks = [smog_trial_engine(t, sem) for t in tokens]
    await asyncio.gather(*tasks)
    
    print(f"\n{Fore.CYAN}[INSAAN] Done. Check accounts in 24-48 hours.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        os._exit(0)
