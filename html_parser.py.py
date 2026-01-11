import pandas as pd
import re 
from bs4 import BeautifulSoup
import os
from bs4 import Tag
import html

phones = []

base = r"path/to/your/html_files"

for file in os.listdir(base):

    with open(os.path.join(base, file), "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    name_tag = soup.select_one("h1.font-figtree")
    name = name_tag.get_text(strip=True) if name_tag else None

    description_tag = soup.select_one("p")
    description = description_tag.get_text(strip=True) if description_tag else None

    beebom_tag= soup.select_one("p.beebom-score")
    beebom_score = beebom_tag.get_text(strip=True) if beebom_tag else None

    span_tag = soup.find_all("span")

    rating = None

    for span in span_tag:
        text = span.get_text(strip=True)
        if text.replace('.','',1).isdigit():
            value = float(text)
            if 0 <= value <= 5:
                rating = value
                break

    rating_count_tag = soup.select_one('p.hidden.sm\\:block',string = lambda x:x and 'Ratings' in x)
    rating_count = rating_count_tag.get_text(strip=True) if rating_count_tag else None

    market_status = None

    for p in soup.find_all('p'):

        if 'Market Status:' in p:
            span = p.find('span')
            market_status = span.get_text(strip=True) if span else None
            break


    launch_date = None

    for p in soup.find_all('p'):
        p_text = p.get_text(strip=True)

        if "Launched On" in p_text:
            span = p.find('span')
            launch_date = span.get_text(strip=True) if span else None
            break

    segment_tag = soup.select_one('#mobile-usp') or soup.find(id='mobile-usp')
    unique_seling_point = segment_tag.get_text(strip=True) if segment_tag else None

    intro_tag = soup.select_one('div[dbe] p')
    price_in_india = intro_tag.get_text(strip=True) if intro_tag else None
   
    blocks = soup.select('div.mt-1.text-start')

    text = []

    for b in blocks:

        text_tag = b.find_all('span')

        for t in text_tag:
            text.append(t.get_text(strip=True))

    raw_text = ' '.join(text) if text else None

    competitors = []

    for card in soup.select('div.bg-white'):
            
            info = card.select_one('div.text-center')
            if not info:
                 continue

            comp_tag = card.select_one('p.font-medium')
            if not comp_tag:
                continue

            comp_name = comp_tag.get_text(strip=True)

            if comp_name and comp_name != 'Beebom Score':
                competitors.append(comp_name)            

    competitors = competitors or None
    
    
    price = None

    for div in soup.select('div.flex.flex-col'):
        p = div.find('p')

        if p:
            text = p.get_text(strip=True)
            if text.startswith("₹"):
                price = text
                break

    
    review = None

    p = soup.select_one("div.flex.items-start div.w-full > p")

    if p:
        text = p.get_text(" ", strip=True) 
        if len(text) > 50:
            review = text

    pros = []

    pros_heading = soup.find("p", string=lambda x: x and x.strip() == "Pros")

    if pros_heading:
    # Step 2: go to inner div → then outer wrapper div
        inner_div = pros_heading.find_parent("div")
        wrapper_div = inner_div.find_parent("div") if inner_div else None

        # Step 3: find UL inside wrapper div
        ul = wrapper_div.find("ul") if wrapper_div else None

        # Step 4: extract LI text
        for li in ul.find_all("li", recursive=False) if ul else []:
            span = li.find("span")
            if span:
                span.decompose()

            text = li.get_text(" ", strip=True)
            if text:
                pros.append(text)

    pros = pros or None

    cons = []

    cons_heading = soup.find("p", string=lambda x: x and x.strip() == "Cons")

    if cons_heading:
    # Step 2: go to inner div → then outer wrapper div
        inner_div = cons_heading.find_parent("div")
        wrapper_div = inner_div.find_parent("div") if inner_div else None

        # Step 3: find UL inside wrapper div
        ul = wrapper_div.find("ul") if wrapper_div else None

        # Step 4: extract LI text
        for li in ul.find_all("li", recursive=False) if ul else []:
            span = li.find("span")
            if span:
                span.decompose()

            text = li.get_text(" ", strip=True)
            if text:
                cons.append(text)

    cons = cons or None
    
    box_content = None
    
    heading = soup.find("p", string = lambda x: x and x.strip() == 'Box Contents')

    value_p = heading.find_next('p') if heading else None

    box_content = value_p.get_text(strip=True) if value_p else None

    colors = None

    for li in soup.find_all('li'):

        p_tags = li.find_all('p')

        if len(p_tags) < 2:
            continue

        label = p_tags[0].get_text(strip=True)

        if label == "Colors":

            colors = p_tags[1].get_text(strip=True)
            break

    
    stores = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        store = p_tag[0].get_text(strip=True)

        if store == 'Stores':

            stores = p_tag[1].get_text(strip=True)
            break

    origin = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Origin Country':

            origin = p_tag[1].get_text(strip=True)
            break

    launch_price = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Launch Price':

            launch_price = p_tag[1].get_text(strip=True)
            break

    display_type = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Type':

            display_type = p_tag[1].get_text(strip=True)
            break
    display_type = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Type':

            display_type = p_tag[1].get_text(strip=True)
            break

    display_size = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Size':

            display_size = p_tag[1].get_text(strip=True)
            break

    display_res = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Resolution':

            display_res = p_tag[1].get_text(strip=True)
            break

    body_dimension = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Dimensions':

            body_dimension = p_tag[1].get_text(strip=True)
            break

    body_weight = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Weight':

            body_weight = p_tag[1].get_text(strip=True)
            break

    body_front = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Front':

            body_front = p_tag[1].get_text(strip=True)
            break

    body_back = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Back':

            body_back = p_tag[1].get_text(strip=True)
            break

    body_side = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Side':

            body_side = p_tag[1].get_text(strip=True)
            break

    body_quality = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Build Quality':

            body_quality = p_tag[1].get_text(strip=True)
            break

    body_ports = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Ports':

            body_ports = p_tag[1].get_text(strip=True)
            break

    ip_rating = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'IP Rating':

            ip_rating = p_tag[1].get_text(strip=True)
            break

    speaker = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Speaker':

            speaker = p_tag[1].get_text(strip=True)
            break

    chipset = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Chipset':

            chipset = p_tag[1].get_text(strip=True)
            break

    cpu = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'CPU':

            cpu = p_tag[1].get_text(strip=True)
            break

    gpu = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'GPU':

            gpu = p_tag[1].get_text(strip=True)
            break

    camera1 = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Main Camera':

            camera1 = p_tag[1].get_text(strip=True)
            break

    camera2 = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Main Camera #2':

            camera2 = p_tag[1].get_text(strip=True)
            break

    camera3 = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Main Camera #3':

            camera3 = p_tag[1].get_text(strip=True)
            break

    camera_features = None

    main_div = soup.find('div', id='main-camera')

    if main_div:

        for li in main_div.find_all('li'):

            p_tag = li.find_all('p')

            if len(p_tag) < 2:
                continue

            text = p_tag[0].get_text(strip=True)

            if text == 'Features':

                camera_features = p_tag[1].get_text(strip=True)
                break

    video = None

    main_video_div = soup.find('div', id='main-camera')

    if main_video_div:

        for li in main_video_div.find_all('li'):

            p_tag = li.find_all('p')

            if len(p_tag) < 2:
                continue

            text = p_tag[0].get_text(strip=True)

            if text == 'Video':

                video = p_tag[1].get_text(strip=True)
                break

    operating_system = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Operating System':

            operating_system = p_tag[1].get_text(strip=True)
            break

    software_updates = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Software Updates':

            software_updates = p_tag[1].get_text(strip=True)
            break

    ai_features = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'AI Features':

            ai_features = p_tag[1].get_text(strip=True)
            break

    front_cam = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Front Camera':

            front_cam = p_tag[1].get_text(strip=True)
            break

    front_cam_features = None

    selfie_div = soup.find('div', id='selfie-camera')

    if selfie_div:

        for li in selfie_div.find_all('li'):
            p_tag = li.find_all('p')

            if len(p_tag) < 2:
                continue

            text = p_tag[0].get_text(strip=True)

            if text == 'Features':

                front_cam_features = p_tag[1].get_text(strip=True)
                break

    front_video = None

    front_main_video_div = soup.find('div', id='selfie-camera')

    if front_main_video_div:

        for li in front_main_video_div.find_all('li'):

            p_tag = li.find_all('p')

            if len(p_tag) < 2:
                continue

            text = p_tag[0].get_text(strip=True)

            if text == 'Video':

                front_video = p_tag[1].get_text(strip=True)
                break

    battery = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Capacity':

            battery = p_tag[1].get_text(strip=True)
            break

    charging = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Charging':

            charging = p_tag[1].get_text(strip=True)
            break

    storage = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Storage':

            storage = p_tag[1].get_text(strip=True)
            break

    ram = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'RAM':

            ram = p_tag[1].get_text(strip=True)
            break

    sim = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'SIM':

            sim= p_tag[1].get_text(strip=True)
            break

    tech = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Technology':

            tech = p_tag[1].get_text(strip=True)
            break

    g2 = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == '2G Bands':

            g2 = p_tag[1].get_text(strip=True)
            break

    g3 = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == '3G Bands':

            g3 = p_tag[1].get_text(strip=True)
            break

    g4 = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == '4G Bands':

            g4 = p_tag[1].get_text(strip=True)
            break

    g5 = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == '5G Bands':

            g5 = p_tag[1].get_text(strip=True)
            break

    speed = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Speed':

            speed = p_tag[1].get_text(strip=True)
            break

    wlan = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'WLAN':

            wlan = p_tag[1].get_text(strip=True)
            break

    bluetooth = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Bluetooth':

            bluetooth = p_tag[1].get_text(strip=True)
            break

    pos = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Positioning':

            pos = p_tag[1].get_text(strip=True)
            break

    nfc = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'NFC':

            nfc = p_tag[1].get_text(strip=True)
            break

    finger = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Fingerprint Scanner':

            finger = p_tag[1].get_text(strip=True)
            break

    sensors = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Sensors':

            sensors = p_tag[1].get_text(strip=True)
            break

    add_fea = None

    for li in soup.find_all('li'):

        p_tag = li.find_all('p')

        if len(p_tag) < 2:
            continue

        text = p_tag[0].get_text(strip=True)

        if text == 'Additional Features':

            add_fea = p_tag[1].get_text(strip=True)
            break
    
    flipkart_buy = None


    for tag in soup.find_all(attrs={"data-href": True}):

        url = html.unescape(tag["data-href"])

        if "flipkart.com" in url:
            flipkart_buy = url

    
    amazon_buy = None

    for tag in soup.find_all(attrs={"data-href": True}):

        url = html.unescape(tag["data-href"])

        if "amazon.in" in url or "amzn.to" in url:
            amazon_buy = url

    BRAND_OFFICIAL_DOMAINS = {
    "realme": ["realme.com"],
    "samsung": ["samsung.com"],
    "vivo": ["vivo.com"],
    "oppo": ["oppo.com"],
    "redmi": ["mi.com", "xiaomi.com"],
    "iqoo": ["iqoo.com"],
    "poco": ["po.co", "mi.com"],
    "infinix": ["infinixmobility.com"],
    "oneplus": ["oneplus.in", "oneplus.com"],
    "apple": ["apple.com"],
    "motorola": ["motorola.in", "motorola.com"],
    "moto": ["motorola.in", "motorola.com"],
    "google": ["store.google.com"],
    "nothing": ["nothing.tech"],
    "xiaomi": ["mi.com", "xiaomi.com"],
    "honor": ["honor.com"],
    "asus": ["asus.com"],
    "cmf": ["cmf.tech", "nothing.tech"]
}

    results = None

    for tag in soup.find_all(attrs={"data-href": True}):
        url = html.unescape(tag["data-href"]).lower()

        for brand, domains in BRAND_OFFICIAL_DOMAINS.items():
            if any(domain in url for domain in domains):
                results = url

    print(results)

    phones.append({
        'model':name,
        'description':description,
        'beebome_score':beebom_score,
        'rating':rating,
        'rating_count':rating_count,
        'market_status':market_status,
        'launch_on':launch_date,
        'usp':unique_seling_point,
        'price_description':price_in_india,
        'old_price':raw_text,
        'competitors':competitors,
        'price':price,
        'review':review,
        'pros':pros,
        'cons':cons,
        'box_contents':box_content,
        'colors':colors,
        'stores':stores,
        'origin_country':origin,
        'launch_price':launch_price,
        'display_type':display_type,
        'display_size':display_size,
        'display_res':display_res,
        'body_dimension':body_dimension,
        'weight':body_weight,
        'body_front':body_front,
        'body_back':body_back,
        'body_side':body_side,
        'build_quality':body_quality,
        'ports':body_ports,
        'ip_rating':ip_rating,
        'speaker':speaker,
        'chipset':chipset,
        'cpu':cpu,
        'gpu':gpu,
        'main_cam':camera1,
        'main_cam2':camera2,
        'main_cam3':camera3,
        'main_cam_features':camera_features,
        'main_video':video,
        'os':operating_system,
        'software_updates':software_updates,
        'ai_features':ai_features,
        'front_cam':front_cam,
        'front_cam_features':front_cam_features,
        'front_video':front_video,
        'battery':battery,
        'charging':charging,
        'storage':storage,
        'ram':ram,
        'sim':sim,
        'tech':tech,
        '2g':g2,
        '3g':g3,
        '4g':g4,
        '5g':g5,
        'speed':speed,
        'wifi':wlan,
        'bluetooth':bluetooth,
        'positioning_system':pos,
        'nfc':nfc,
        'finger_print':finger,
        'sensors':sensors,
        'add_features':add_fea,
        'flipkart_buy_link':flipkart_buy,
        'amazon_buy_link':amazon_buy,
        'official_store_link':results
    })


df = pd.DataFrame(phones)


df['model_id'] = df.index + 1
df = df.set_index('model_id').reset_index()
print(df.sample(20))
df.info()

df.to_csv('4_jan_smartphones_all_details.csv',index=False)