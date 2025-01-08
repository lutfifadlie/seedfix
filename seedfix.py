import os
import asyncio
import aiohttp
import requests
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
from urllib.parse import unquote, quote
import time
from datetime import datetime
from colorama import Fore, Style, init
import sys
import pytz
sys.stdout.reconfigure(encoding='utf-8')

init(autoreset=True)

# Warna output
merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
magenta = Fore.LIGHTMAGENTA_EX
aqua = Fore.LIGHTCYAN_EX 


#####################################################
API_ID = '25353483'                                 #
API_HASH = 'b44c3864933f1e8d956073420f180e1a'       #
WORKDIR = 'sessions'                                #
ref_bot = '1638836725'                              #
#####################################################



if not os.path.exists(WORKDIR):
    print(f"Folder {WORKDIR} tidak ditemukan!")
    exit(1)

def format_decimal(value, decimals=6):
    try:
        value = float(value)
        return f"{value / 1000000000:.{decimals}f}"
    except (ValueError, TypeError):
        print(f"Error: Nilai '{value}' bukan angka yang valid.")
        return "N/A"
        
def convert_to_wib(utc_time_str):
    # Parsing waktu UTC
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
    # Mengatur zona waktu ke UTC
    utc_time = utc_time.replace(tzinfo=pytz.UTC)
    # Konversi ke WIB (UTC+7)
    wib_time = utc_time.astimezone(pytz.timezone("Asia/Jakarta"))
    return wib_time.strftime("%H:%M")


async def execute_session(session_file):
    full_path = os.path.join(WORKDIR, session_file)
    print(f"=======================================")
    
    if not os.path.exists(full_path + '.session'):
        print(f"File sesi {full_path}.session tidak ditemukan!")
        return
    
    app = Client(
        name=session_file,
        api_id=API_ID,
        api_hash=API_HASH,
        workdir=WORKDIR
    )
    
    try:
        await app.start()
        peer = await app.resolve_peer('seed_coin_bot')
        web_view = await app.invoke(RequestAppWebView(
            peer=peer,
            app=InputBotAppShortName(bot_id=peer, short_name="app"),
            platform='android',
            write_allowed=True,
            start_param=ref_bot
        ))

        auth_url = web_view.url
        init_data = unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                     
        await app.stop()
        await login(init_data)
        await benefit(init_data)
        #await holy(init_data)
        await streak(init_data)
        await inventory(init_data)
        await cacing(init_data)
        await leader(init_data)
        #await egg_merge(init_data)
        await task(init_data)
        await balance(init_data)

    except Exception as e:
        print(f"Terjadi kesalahan pada sesi {full_path}: {e}")

async def login(init_data):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Telegram-Data": init_data,
        "Origin": "https://cf.seeddao.org",
        "Referer": "https://cf.seeddao.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Mobile Safari/537.36"
    }

    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get("https://alb.seeddao.org/api/v1/profile/balance", headers=headers) as balance_response:
                if balance_response.status == 200:
                    databalance = await balance_response.json()
                    balance = databalance.get('data', 0)
                    print(f"{hijau}Balance: {aqua}{format_decimal(balance)}")
                else:
                    print(f"{kuning}gagal mengambil balance")
                    
            async with session.get("https://alb.seeddao.org/api/v1/profile2", headers=headers) as profil2_response:
                if profil2_response.status == 200:
                    data = await profil2_response.json()
                    userdata = data.get('data', {})
                    name = userdata.get('name', 'Unknown user')
                    wallet = userdata.get('wallet_address_ton') if userdata.get('wallet_address_ton') else "No wallet linked"
                    age = userdata.get('age', 0)
                    bonus_claimed = userdata.get('bonus_claimed')
        
                    print(f"{hijau}Login: {aqua}{name} Age: {age}")
                    print(f"{hijau}Wallet address: {aqua}{wallet}")
                else:
                    print(f"{kuning}Login Gagal")
                    
            async with session.post("https://alb.seeddao.org/api/v1/seed/claim", headers=headers) as seedclaim_response:
                if seedclaim_response.status == 200:
                    seed = await seedclaim_response.json()
                    seed_data = seed.get('data', {})
                    jumlah = seed_data.get('amount', 0)
                    print(f"{hijau}Claim seed sukses: {aqua}+{format_decimal(jumlah)}")
                else:
                    print(f"{kuning}mining masih berjalan")
                    
            async with session.get("https://alb.seeddao.org/api/v1/worms", headers=headers) as worm_response:
                if worm_response.status == 200:
                    worm = await worm_response.json()
                    worm_data = worm.get('data', {})
                    worm_reward = worm_data.get('reward', 0)
                    ended_at = worm_data.get('ended_at')
                    next_worm = worm_data.get('next_worm')
                    is_caught = worm_data.get('is_caught', False)
                    
                    ended_wib = convert_to_wib(ended_at)
                    next_worm_wib = convert_to_wib(next_worm)
                    
                    if not is_caught:
                        async with session.post("https://alb.seeddao.org/api/v1/worms/catch", headers=headers) as cacing_response:
                            if cacing_response.status == 200:
                                cacing = await cacing_response.json()
                                cacing_data = cacing.get('data', {})
                                cacing_type = cacing_data.get('type')
                                cacing_status = cacing_data.get('status')
                                cacing_reward = cacing_data.get('reward', 0)
                                print(f"{putih}claim cacing {hijau}{cacing_status} : {cacing_type} {aqua}+{format_decimal(cacing_reward)} Next Cacing: {next_worm_wib} WIB")
                            else:
                                print(f"{kuning}cacing wes minggat Next Cacing: {next_worm_wib} WIB")
                        
                    else:
                        print(f"{kuning}Cacing sudah di klaim:{hijau}Next Cacing: {next_worm_wib} WIB")
                        
                else:
                    print(f"{kuning}Gagal mengambil data cacing")
                    
            async with session.post("https://alb.seeddao.org/api/v1/login-bonuses", headers=headers) as loginbonus_response:
                if loginbonus_response.status == 200:
                    bonus = await loginbonus_response.json()
                    checkin_data = bonus.get('data', {})
                    checkin_number = checkin_data.get('no', 0)
                    checkin_reward = checkin_data.get('amount', 0)
                    print(f"{hijau}Check in sukses day: {checkin_number} {aqua}+{format_decimal(checkin_reward)}")
                    
                elif loginbonus_response.status == 400:
                    print(f"{kuning}Sudah check in")
                    
                else:
                    print(f"{kuning}Sudah check in")
                    
            async with session.post("https://alb.seeddao.org/api/v1/gift-of-encounter", headers=headers) as gift_response:
                if gift_response.status == 200:
                    async with session.get("https://alb.seeddao.org/api/v1/gift-of-encounter", headers=headers) as cekgift_response:
                        if cekgift_response.status == 200:
                            cekgift = await cekgift_response.json()
                            datagift = cekgift.get('data', {})
                            nextclaim = datagift.get('next_claim_to')
                            
                            nextclaim_wib = convert_to_wib(nextclaim)
                            print(f"{hijau}Sukses Claim BREWOK NEXT {nextclaim_wib}")
                        else:
                            print(f"{kuning}{cekgift_response.status}")
                    
                elif gift_response.status == 400:
                    async with session.get("https://alb.seeddao.org/api/v1/gift-of-encounter", headers=headers) as cekgift_response:
                        if cekgift_response.status == 200:
                            cekgift = await cekgift_response.json()
                            datagift = cekgift.get('data', {})
                            nextclaim = datagift.get('next_claim_to')
                            
                            nextclaim_wib = convert_to_wib(nextclaim)
                            print(f"{kuning}BREWOK tersedia besok : {nextclaim_wib} WIB")
                        else:
                            print(f"{kuning}{cekgift_response.status}")
                else:
                    print(f"{kuning}{gift_response.status}")
                    
            async with session.get("https://alb.seeddao.org/api/v1/guild/member/detail", headers=headers) as guild_response:
                if guild_response.status == 200:
                    guild = await guild_response.json()
                    guild_data = guild.get('data')

                    if guild_data is None:
                        print(f"{kuning}tidak ada klan sedang bergabung ...")
                        async with session.post("https://alb.seeddao.org/api/v1/guild/join", json={"guild_id": "e652cf56-b9a1-43c1-a91e-a07d3de77fa2"}, headers=headers) as join_response:
                            if join_response.status == 200:
                                print(f"{hijau}sukses join")
                                async with session.get("https://alb.seeddao.org/api/v1/guild/detail?guild_id=e652cf56-b9a1-43c1-a91e-a07d3de77fa2&sort_by=total_hunted", headers=headers) as guild_info_response:
                                    if guild_info_response.status == 200:
                                        guild_info = await guild_info_response.json()
                                        guild_info_data = guild_info.get('data', {})
                                        guild_info_name = guild_info_data.get('name')
                                        guild_info_hunted = guild_info_data.get('hunted', 0)
                                        guild_info_member = guild_info_data.get('number_member', 0)
                                        guild_info_rate = guild_info_data.get('distribution_rate', 0)
                                        guild_info_size = guild_info_data.get('size', 0)
                                        guild_info_rank = guild_info_data.get('rank_index')
                                        print(f"{putih}{guild_info_name} Hunted: {format_decimal(guild_info_hunted)} Member : {guild_info_member}/{guild_info_size} Rate: {guild_info_rate} Rank : {guild_info_rank}")
                                    else:
                                        print(f"{kuning}Gagal mendapat data guild setelah join")
                            else:
                                print(f"{kuning}Gagal join guild")
        
                    else:
                        guild_id = guild_data.get('guild_id')
                        async with session.get(f"https://alb.seeddao.org/api/v1/guild/detail?guild_id={guild_id}&sort_by=total_hunted", headers=headers) as guild_info_response:
                            if guild_info_response.status == 200:
                                guild_info = await guild_info_response.json()
                                guild_info_data = guild_info.get('data', {})
                                guild_info_name = guild_info_data.get('name')
                                guild_info_rank = guild_info_data.get('rank_index')
                                print(f"{hijau}Guild {guild_info_name} Rank : {guild_info_rank}")
                            else:
                                print(f"{kuning}Gagal mendapat data guild yang ada")
                else:
                    print(f"{kuning}Gagal mendapat data member guild")
                    
            async with session.get("https://alb.seeddao.org/api/v1/spin-ticket", headers=headers) as spin_response:
                if spin_response.status == 200:
                    spin = await spin_response.json()
                    spin_data = spin.get('data', [])

                    if not spin_data:
                        print(f"{kuning}Tiket spin 0")
                    else:
                        for spin_ticket in spin_data:
                            spin_id = spin_ticket.get('id')
                            payload = {"ticket_id": spin_id}

                            async with session.post("https://alb.seeddao.org/api/v1/spin-reward", json=payload, headers=headers) as putar_response:
                                if putar_response.status == 200:
                                    putar = await putar_response.json()
                                    putar_data = putar.get('data', {})
                                    putar_status = putar_data.get('status')
                                    putar_type = putar_data.get('type')
                                    print(f"{hijau}Spin status {putar_status} {aqua}Reward {putar_type}")
                                else:
                                    print(f"{kuning}Gagal memutar spin untuk tiket ID: {spin_id}")

                            await asyncio.sleep(1)
                else:
                    print(f"{kuning}Gagal mengambil data Tiket")
                    
        except Exception as e:
            print(f"{putih}server lemot gagal mendapat data")

async def benefit(init_data):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Telegram-Data": init_data,
        "Origin": "https://cf.seeddao.org",
        "Referer": "https://cf.seeddao.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Mobile Safari/537.36"
    }

    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get("https://alb.seeddao.org/api/v1/guild/user-benefit", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    jumlah = data.get('data', {}).get('amount', 0)
                    
                    if jumlah > 0:
                        async with session.post("https://alb.seeddao.org/api/v1/guild/user-benefit-claim", headers=headers) as claim_response:
                            if claim_response.status == 200:
                                print(f"{hijau}Bonus Guild claimed : {aqua}+{format_decimal(jumlah)}")
                            else:
                                print(f"{kuning}you claim too soon {claim_response.status}")
                else:
                    print(f"{kuning}gagal {response.status}")
                    
        except Exception as e:
            print(f"{putih}server lemot gagal mendapat data")
            
async def holy(init_data):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Telegram-Data": init_data,
        "Origin": "https://cf.seeddao.org",
        "Referer": "https://cf.seeddao.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Mobile Safari/537.36"
    }

    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.post("https://alb.seeddao.org/api/v1/upgrades/tasks/23f889c8-4fa3-4743-b624-88fc7784f9e6", headers=headers) as retweet_response:
                if retweet_response.status == 200:
                    dataretweet = await retweet_response.json()
                    data_retweet = dataretweet.get('data')
                    await asyncio.sleep(2)
                    if data_retweet:
                        async with session.get(f"https://alb.seeddao.org/api/v1/tasks/notification/{data_retweet}", headers=headers) as notif_response:
                            if notif_response.status == 200:
                                print(f"{hijau}retweet done")
                            else:
                                print(f"{merah}gagal {notif_response.status}")
                else:
                    print(f"{kuning}gagal {retweet_response.status}")
                    
            await asyncio.sleep(2)
            async with session.post("https://alb.seeddao.org/api/v1/upgrades/tasks/23f889c8-4fa3-4743-b624-88fc7784f9e6", headers=headers) as retweets_response:
                if retweets_response.status == 200:
                    dataretweets = await retweets_response.json()
                    data_retweets = dataretweets.get('data')
                    await asyncio.sleep(2)
                    if data_retweets:
                        async with session.get(f"https://alb.seeddao.org/api/v1/tasks/notification/{data_retweets}", headers=headers) as notifs_response:
                            if notifs_response.status == 200:
                                print(f"{hijau}like retweet done")
                            else:
                                print(f"{merah}gagal {notifs_response.status}")
                else:
                    print(f"{kuning}gagal {retweets_response.status}")
                    
            await asyncio.sleep(2)
            async with session.post("https://alb.seeddao.org/api/v1/upgrades/tasks/699f87d7-a332-464f-9fdb-6f81a778713f", headers=headers) as cekin2_response:
                if cekin2_response.status == 200:
                    datacekin2 = await cekin2_response.json()
                    data_cekin2 = datacekin2.get('data')
                    await asyncio.sleep(2)
                    if data_cekin2:
                        async with session.get(f"https://alb.seeddao.org/api/v1/tasks/notification/{data_cekin2}", headers=headers) as notifcekin2_response:
                            if notifcekin2_response.status == 200:
                                print(f"{hijau}cekin 2 done")
                            else:
                                print(f"{merah}gagal {notifcekin2_response.status}")
                else:
                    print(f"{kuning}gagal {cekin2_response.status}")
                    
            await asyncio.sleep(2)
            async with session.post("https://alb.seeddao.org/api/v1/upgrades/tasks/16ae487a-8608-4d66-94ce-1329f8f250d1", headers=headers) as cekin5_response:
                if cekin5_response.status == 200:
                    datacekin5 = await cekin5_response.json()
                    data_cekin5 = datacekin5.get('data')
                    await asyncio.sleep(2)
                    if data_cekin5:
                        async with session.get(f"https://alb.seeddao.org/api/v1/tasks/notification/{data_cekin5}", headers=headers) as notifcekin5_response:
                            if notifcekin5_response.status == 200:
                                print(f"{hijau}cekin 5 done")
                            else:
                                print(f"{merah}gagal {notifcekin5_response.status}")
                else:
                    print(f"{kuning}gagal {cekin5_response.status}")
                    
            await asyncio.sleep(2)
            async with session.post("https://alb.seeddao.org/api/v1/upgrades/holy-water", headers=headers) as holy2_response:
                if holy2_response.status == 200:
                    print(f"{hijau}holy 2 done")
                else:
                    print(f"{kuning}gagal up 2 holy {holy2_response.status}")
                    
            await asyncio.sleep(2)
            async with session.post("https://alb.seeddao.org/api/v1/upgrades/holy-water", headers=headers) as holy3_response:
                if holy3_response.status == 200:
                    print(f"{hijau}holy 3 done")
                else:
                    print(f"{kuning}gagal up 3 holy {holy3_response.status}")
                    
            await asyncio.sleep(2)
            async with session.post("https://alb.seeddao.org/api/v1/upgrades/holy-water", headers=headers) as holy4_response:
                if holy4_response.status == 200:
                    print(f"{hijau}holy 4 done")
                else:
                    print(f"{kuning}gagal up 4 holy {holy4_response.status}")
                    
        except Exception as e:
            print(f"{putih}server lemot gagal mendapat data")
            
async def streak(init_data):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Telegram-Data": init_data,
        "Origin": "https://cf.seeddao.org",
        "Referer": "https://cf.seeddao.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Mobile Safari/537.36"
    }

    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get("https://alb.seeddao.org/api/v1/streak-reward", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
            
                    # Mengambil semua ID dari data
                    streak_reward_ids = [item.get("id") for item in data.get("data", []) if item.get("id")]

                    if streak_reward_ids:
                        # Membuat payload
                        payload = {"streak_reward_ids": streak_reward_ids}

                        # Mengirim POST request
                        async with session.post("https://alb.seeddao.org/api/v1/streak-reward", json=payload, headers=headers) as post_response:
                            if post_response.status == 200:
                                result = await post_response.json()
                                print(f"{hijau}Berhasil klaim streak reward: {result}")
                            else:
                                print(f"{kuning}Gagal klaim streak reward: {post_response.status}")
                    else:
                        print(f"{kuning}Tidak ada ID streak reward tersedia")
                else:
                    print(f"{kuning}Gagal mengambil data streak reward: {response.status}")
                    
        except Exception as e:
            print(f"{putih}server lemot gagal mendapat data")
            
async def egg_merge(init_data):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Telegram-Data": init_data,
        "Origin": "https://cf.seeddao.org",
        "Referer": "https://cf.seeddao.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Mobile Safari/537.36"
    }

    timeout = aiohttp.ClientTimeout(total=30)
    print(f"{magenta}Checking merge...")

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get("https://alb.seeddao.org/api/v1/egg-piece", headers=headers) as response:
                if response.status == 200:
                    response_data = await response.json()
                    egg_pieces = response_data.get('data', [])

                    categorized_ids = {
                        'common': [],
                        'uncommon': [],
                        'rare': [],
                        'epic': [],
                        'legendary': []
                    }

                    for item in egg_pieces:
                        tipe = item.get('type')
                        if tipe in categorized_ids:
                            categorized_ids[tipe].append(item['id'])

                    for tipe, ids in categorized_ids.items():
                        print(f"{putih}Tiket {tipe} = {aqua}{len(ids)}")

                    for tipe in categorized_ids:
                        print(f"{magenta}Checking Free fusion ...")
                        async with session.get(f"https://alb.seeddao.org/api/v1/fusion-seed-fee?type={tipe}", headers=headers) as fee_response:
                            if fee_response.status == 200:
                                fee_data = await fee_response.json()

                                if fee_data.get('data') < 18800000000:
                                    if len(categorized_ids[tipe]) < 5:
                                        pass
                                    else:
                                        selected_ids = categorized_ids[tipe][:5]
                                        merge_payload = {"egg_piece_ids": selected_ids}

                                        for id in selected_ids:
                                            pass

                                        async with session.post("https://alb.seeddao.org/api/v1/egg-piece-merge", json=merge_payload, headers=headers) as merge_response:
                                            if merge_response.status == 200:
                                                merge_result = await merge_response.json()
                                                if merge_result.get('data'):
                                                    print(f"{hijau}Sukses menukar tiket menjadi NDOG")
                                                    egg_id = merge_result['data']['id']
                                                    sell_payload = {"egg_id": egg_id,"price":37000000000}
                                                    async with session.post("https://alb.seeddao.org/api/v1/market-item/add", json=sell_payload, headers=headers) as hatch_response:
                                                        if hatch_response.status == 200:
                                                            hatch_result = await hatch_response.json()
                                                            if hatch_result.get('data'):
                                                                bird_type = hatch_result['data']['egg_type']
                                                                price_net = hatch_result['data']['price_net']
                                                                print(f"{hijau}Sukses sell telur di pasar harga 37. fee 3 | NET {format_decimal(price_net)}")
                                                        else:
                                                            print(f"{putih}Gagal menetaskan telur, status: {hatch_response.status}")
                                                else:
                                                    print(f"{kuning}Gagal menukar tiket menjadi NDOG")
                                            else:
                                                print(f"{putih}Gagal melakukan merge untuk '{tipe}', status: {merge_response.status}")
                                else:
                                    pass
                            else:
                                pass
                else:
                    print(f"{putih}Gagal mendapatkan tiket merge, status: {response.status}")

        except Exception as e:
            print(f"{putih}Server lemot gagal mendapat data: {e}")
            
async def inventory(init_data):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Telegram-Data": init_data,
        "Origin": "https://cf.seeddao.org",
        "Referer": "https://cf.seeddao.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Mobile Safari/537.36"
    }

    timeout = aiohttp.ClientTimeout(total=30)
    output = f"{putih}Checking Inventory..."
    print(output, end=' ', flush=True)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get("https://alb.seeddao.org/api/v1/egg/me?page=1", headers=headers) as ndog_response:
                if ndog_response.status == 200:
                    ndog = await ndog_response.json()
                    ndog_balance = ndog.get('data', {}).get('total', 0)
                    output += f"{hijau} | Ndog: {aqua}{ndog_balance}"
                            
                else:
                    output += f" | {kuning}Ndog: Null"
            
            async with session.get("https://alb.seeddao.org/api/v1/worms/me?page=1", headers=headers) as cacing_response:
                if cacing_response.status == 200:
                    cacing = await cacing_response.json()
                    cacing_balance = cacing.get('data', {}).get('total', 0)
                    output += f"{hijau} | Cacing: {aqua}{cacing_balance}"
                else:
                    output += f" | {kuning}Cacing: Null"
            
            async with session.get("https://alb.seeddao.org/api/v1/bird/me?page=1", headers=headers) as manuk_response:
                if manuk_response.status == 200:
                    manuk = await manuk_response.json()
                    manuk_balance = manuk.get('data', {}).get('total', 0)
                    output += f"{hijau} | Manuk: {aqua}{manuk_balance}"
                else:
                    output += f" | {kuning}Manuk: Null"
            
            print(f"\r{output}", flush=True)
        
        except Exception as e:
            print(f"{putih}server lemot gagal mendapat data: {e}")
            
async def cacing(init_data):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Telegram-Data": init_data,
        "Origin": "https://cf.seeddao.org",
        "Referer": "https://cf.seeddao.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Mobile Safari/537.36"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get("https://alb.seeddao.org/api/v1/worms/me?page=1", headers=headers) as response:
            if response.status == 200:
                data = await response.json()

                type_counts = {}
                items_to_sell = []

                for item in data["data"]["items"]:
                    item_type = item["type"]
                    if item_type in type_counts:
                        type_counts[item_type] += 1
                    else:
                        type_counts[item_type] = 1

                    if item_type == "rare":
                        items_to_sell.append({"worm_id": item["id"], "price": 15000000000})#RARE harga 3 SEED
                    elif item_type == "epic":
                        items_to_sell.append({"worm_id": item["id"], "price": 66000000000})#EPIC harga 10 SEED

                for item_type, count in type_counts.items():
                    print(f"{kuning}Cacing {item_type.capitalize()}: {hijau}{count}")
                
                total_items = data["data"]["total"]
                print(f"{putih}Total cacing: {total_items}")

                for item in items_to_sell:
                    payload = {
                        "worm_id": item["worm_id"],
                        "price": item["price"]
                    }
                    async with session.post("https://alb.seeddao.org/api/v1/market-item/add", headers=headers, json=payload) as sell_response:
                        if sell_response.status == 200:
                            print(f"{putih}Item {item['worm_id']} {hijau}berhasil dijual dengan harga {item['price']}")
                        else:
                            print(f"Gagal menjual item {item['worm_id']}, status code: {sell_response.status}")
            else:
                print(f"Failed to fetch data, status code: {response.status}")
            
async def leader(init_data):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Telegram-Data": init_data,
        "Origin": "https://cf.seeddao.org",
        "Referer": "https://cf.seeddao.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Mobile Safari/537.36"
    }

    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get("https://alb.seeddao.org/api/v1/bird/is-leader", headers=headers) as bird_response:
                if bird_response.status == 200:
                    bird = await bird_response.json()
                    bird_data = bird.get('data', {})
                    bird_id = bird_data.get('id')
                    bird_task = bird_data.get('task_level')
                    bird_status = bird_data.get('status')
                    
                    if bird_status == 'hunting':
                        payload_hunt_complete = {"bird_id": bird_id}
                        async with session.post("https://alb.seeddao.org/api/v1/bird-hunt/complete", json=payload_hunt_complete, headers=headers) as claim_hunt_response:
                            if claim_hunt_response.status == 200:
                                claim_hunt = await claim_hunt_response.json()
                                claim_hunt_amount = claim_hunt.get('data', {}).get('seed_amount', 0)
                                print(f"{hijau}Sukses claim hunting {aqua}+{format_decimal(claim_hunt_amount)}")
                                
                                await prepare_bird_for_hunting(session, bird_id, bird_task, headers)
                            else:
                                print(f"{kuning}manuk masih hunting")
                    
                    elif bird_status == 'in-inventory':
                        await prepare_bird_for_hunting(session, bird_id, bird_task, headers)
                else:
                    print(f"{kuning}Gagal memuat data burung")
                    
        except Exception as e:
            print(f"{putih}Server lambat, gagal mendapat data: {e}")

async def prepare_bird_for_hunting(session, bird_id, bird_task, headers):
    async with session.get("https://alb.seeddao.org/api/v1/worms/me-all", headers=headers) as worm_response:
        if worm_response.status == 200:
            worms_data = await worm_response.json()
            worm_ids = [worm.get('id') for worm in worms_data.get('data', []) if worm.get('id')]

            if worm_ids:
                for i in range(2):  # Ulangi hingga 2 kali memberi makan
                    if not worm_ids:
                        print(f"{kuning}Tidak ada cacing tersisa")
                        break

                    worm_id = worm_ids.pop(0)  # Ambil worm_id pertama
                    payload_feed = {"bird_id": bird_id, "worm_ids": [worm_id]}
                    async with session.post("https://alb.seeddao.org/api/v1/bird-feed", json=payload_feed, headers=headers) as feed_response:
                        if feed_response.status == 200:
                            feed_result = await feed_response.json()
                            energy_level = feed_result.get('data', {}).get('energy_level', 0)
                            print(f"{hijau}Sukses makani manuk {format_decimal(energy_level)} energi")
                            
                            # Jika worm_id baru diberikan dalam respons, tambahkan ke daftar
                            new_worm_ids = feed_result.get('data', {}).get('available_worms', [])
                            worm_ids.extend(new_worm_ids)
                        elif feed_response.status == 400:
                            print(f"{kuning}Energi manuk sudah maksimal")
                            break  # Hentikan jika energi sudah penuh
                        else:
                            print(f"{kuning}Gagal memberi makan burung")
            else:
                print(f"{kuning}Tidak ada cacing tersedia")
        else:
            print(f"{kuning}Gagal mengambil data cacing")
    
    payload_happy = {"bird_id": bird_id, "happiness_rate": 10000}
    async with session.post("https://alb.seeddao.org/api/v1/bird-feed", json=payload_happy, headers=headers) as happy_response:
        if happy_response.status == 200:
            happy_result = await happy_response.json()
            happy_level = happy_result.get('data', {}).get('happiness_level', 0)
            print(f"{hijau}Manuk sukses happy {happy_level}")
        elif happy_response.status == 400:
            print(f"{kuning}Manuk sudah sangat happy")
        else:
            print(f"{kuning}Gagal membuat manuk happy")

    await start_hunting(session, bird_id, bird_task, headers)

async def start_hunting(session, bird_id, bird_task, headers):
    payload_start_hunt = {"bird_id": bird_id, "task_level": bird_task}
    async with session.post("https://alb.seeddao.org/api/v1/bird-hunt/start", json=payload_start_hunt, headers=headers) as hunt_response:
        if hunt_response.status == 200:
            hunt_data = await hunt_response.json()
            hunt_status = hunt_data.get('data', {}).get('status')
            print(f"{hijau}Manuk sukses mulai hunting {hunt_status}")
        elif hunt_response.status == 400:
            print(f"{kuning}Energi atau happy level burung masih kurang untuk hunting")
        else:
            print(f"{kuning}manuk masih hunting")
            
async def get_academy_answers():
    url = "https://raw.githubusercontent.com/lutfifadlie/seedfix/refs/heads/main/data.txt"  # Sesuaikan URL GitHub Anda
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                text_data = await response.text()
                answer_dict = {}
                for line in text_data.splitlines():
                    if ';' in line:
                        task_name, answer = line.split(';', 1)
                        answer_dict[task_name.strip()] = answer.strip()
                return answer_dict
            else:
                print("Gagal mengambil data dari GitHub.")
                return {}

async def retry_request(session, method, url, headers, task_name, max_retries=3, retry_interval=2, json_data=None):
    for attempt in range(max_retries):
        try:
            if method == 'GET':
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        response_json = await response.json()

                        if "error" in response_json.get("data", {}):
                            error_message = response_json["data"]["error"]
                            if error_message == "incomplete task":
                                print(f"{putih}{task_name} {merah}Coba lagi nanti")
                                break
                            else:
                                pass
                        else:
                            return response_json
                    elif response.status == 404:
                        print(f"{putih}{task_name} {magenta}retrying... ")
                    else:
                        pass
            elif method == 'POST':
                async with session.post(url, headers=headers, json=json_data) as response:
                    if response.status == 200:
                        response_json = await response.json()

                        if "error" in response_json.get("data", {}):
                            error_message = response_json["data"]["error"]
                            if error_message == "incomplete task":
                                print(f"{putih}{task_name} {merah}Coba lagi nanti")
                                break
                            else:
                                pass
                        else:
                            return response_json
                    elif response.status == 404:
                        print(f"{putih}{task_name} {magenta}retrying...")
                    else:
                        pass

            await asyncio.sleep(retry_interval)

        except Exception as e:
            print(f"Error: {e}, retrying... ({attempt + 1}/{max_retries})")
            await asyncio.sleep(retry_interval)

    return None

async def task(init_data):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Telegram-Data": init_data,
        "Origin": "https://cf.seeddao.org",
        "Referer": "https://cf.seeddao.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Mobile Safari/537.36"
    }
    timeout = aiohttp.ClientTimeout(total=30)
    print(f"{kuning}Checking Task...")

    answer_dict = await get_academy_answers()
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            task_data = await retry_request(session, 'GET', "https://alb.seeddao.org/api/v1/tasks/progresses", headers=headers, task_name="Mengambil daftar tugas")
            if task_data:
                tasks = task_data.get('data', [])
                for task in tasks:
                    task_type = task.get('type')
                    task_name = task.get('name')
                    
                    if task_type == "academy":
                        await academy_task(session, task, headers, answer_dict, task_name)
                    else:
                        await regular_task(session, task, headers, task_name)
            else:
                print("Gagal mengambil tugas setelah retry")
        except Exception as e:
            print(f"{putih}server lemot gagal mendapat data: {e}")

async def academy_task(session, task, headers, answer_dict, task_name):
    task_id = task.get('id')
    task_user = task.get('task_user')
    completed = task_user.get('completed', False) if task_user else False
    
    if task_name in answer_dict and (task_user is None or not completed):
        answer_payload = {"answer": answer_dict[task_name]}
        post_url = f"https://alb.seeddao.org/api/v1/tasks/{task_id}"
        post_response = await retry_request(session, 'POST', post_url, headers=headers, task_name=task_name, json_data=answer_payload)

        if post_response:
            task_key = post_response.get('data')
            if task_key:
                result_task = await retry_request(session, 'GET', f"https://alb.seeddao.org/api/v1/tasks/notification/{task_key}", headers=headers, task_name=task_name)
                
                if result_task:
                    result_data = result_task.get('data', {}).get('data', {})
                    completed_task = result_data.get('completed', False)
                    reward_task = result_data.get('reward_amount', 0)

                    if completed_task:
                        print(f"{putih}{task_name} {hijau}sukses {aqua} +{format_decimal(reward_task)}")
                else:
                    pass
            else:
                print("Tidak mendapatkan kunci tugas setelah retry")
        else:
            print("task data academy tidak ada yang baru")
            

async def regular_task(session, task, headers, task_name):
    task_id = task.get('id')
    task_user = task.get('task_user')
    completed = task_user.get('completed', False) if task_user else False
    
    if task_user is None or not completed:
        start_task = await retry_request(session, 'POST', f"https://alb.seeddao.org/api/v1/tasks/{task_id}", headers=headers, task_name=task_name)

        if start_task:
            task_key = start_task.get('data')
            if task_key:
                result_task = await retry_request(session, 'GET', f"https://alb.seeddao.org/api/v1/tasks/notification/{task_key}", headers=headers, task_name=task_name)
                
                if result_task:
                    result_data = result_task.get('data', {}).get('data', {})
                    completed_task = result_data.get('completed', False)
                    reward_task = result_data.get('reward_amount', 0)

                    if completed_task:
                        print(f"{putih}{task_name} {hijau}sukses {aqua} +{format_decimal(reward_task)}")
                else:
                    pass
            else:
                print("Tidak mendapatkan kunci tugas setelah retry")
        else:
            pass
            
async def balance(init_data):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Telegram-Data": init_data,
        "Origin": "https://cf.seeddao.org",
        "Referer": "https://cf.seeddao.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Mobile Safari/537.36"
    }

    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get("https://alb.seeddao.org/api/v1/profile/balance", headers=headers) as balance_response:
                if balance_response.status == 200:
                    databalance = await balance_response.json()
                    balance = databalance.get('data', 0)
                    print(f"{hijau}Balance: {aqua}{format_decimal(balance)}")
                else:
                    print(f"{kuning}gagal mengambil balance")
        except Exception as e:
            print(f"{putih}server lemot gagal mendapat data: {e}")
    
async def process_all_sessions(session_files):
    tasks = []
    for session_file in session_files:
        tasks.append(execute_session(session_file))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    print(f"""{aqua}
      
███╗░░░███╗██████╗ ░█████╗░██╗░░██╗
████╗░████║██╔══██╗██╔══██╗██║░░██║
██╔████╔██║██████╦╝███████║███████║
██║╚██╔╝██║██╔══██╗██╔══██║██╔══██║
██║░╚═╝░██║██████╦╝██║░░██║██║░░██║
╚═╝░░░░░╚═╝╚═════╝ ╚═╝░░╚═╝╚═╝░░╚═╝

""")
    session_files = [f.replace('.session', '') for f in os.listdir(WORKDIR) if f.endswith('.session')]

    batch_size = int(input("Masukkan Kecepatan Akun (contoh: 1 - 100 ): "))
    for i in range(0, len(session_files), batch_size):
        batch = session_files[i:i + batch_size]
        asyncio.run(process_all_sessions(batch))
