from aiohttp import ClientSession
from bs4 import BeautifulSoup

#Gplinks Bypass
async def gplinks(url):
    async with ClientSession() as session:
        res = await session.get(url, allow_redirects=False)
        dat = res.headers['location']
        ref = dat.split('?')[0]
        vid = dat.split('vid=')[-1]
        pid = dat.split('&')[1].split('=')[-1]        
        for s in range(1, 4):
            data = {'imps': 0,'request': 'setVisitor','status': s,'vid': vid}
            await session.post('https://gplinks.com/track/data.php',data=data, headers={'Referer': f"{ref}/"})            
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36','Accept-Language': 'en-US,en;q=0.9','Connection': 'keep-alive','Upgrade-Insecure-Requests': '1','Referer': f'{ref}/'}        
        resp = await session.get(f'{url}/?pid={pid}&vid={vid}',headers=headers)
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        input_data = {inp.get('name'): inp.get('value') for inp in soup.find_all('input')}
        await asleep(3)
        response = await session.post('https://gplinks.co/links/go', data=input_data, headers={'Referer': f"{resp.url}", 'X-Requested-With': 'XMLHttpRequest'}, cookies=resp.cookies)
        return (await response.json())['url']

#Thank You 💀
