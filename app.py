

from flask import Flask, render_template_string, abort, url_for, send_from_directory, request, redirect

from pathlib import Path

import csv

from datetime import datetime

from html import escape



app = Flask(__name__)





# ==============================

# 商品圖片路徑

# ==============================



@app.route("/product-images/<path:filename>")

def product_image(filename):

    """從常見圖片資料夾位置提供產品圖片。"""



    project_dir = Path(__file__).resolve().parent



    possible_dirs = [

        project_dir / "static" / "images",

        project_dir / "static",

        project_dir / "images",

    ]



    for image_dir in possible_dirs:

        image_path = image_dir / filename



        if image_path.is_file():

            return send_from_directory(str(image_dir), filename)



    abort(

        404,

        description=f"找不到圖片：{filename}。請確認圖片位於 static/images 資料夾。"

    )





# ==============================

# 商品資料

# ==============================



PRODUCTS = {

    "black-garlic": {

        "name": "黑蒜頭",

        "subtitle": "熟成蒜頭產品介紹",

        "description": "本競賽作品以黑蒜頭為介紹主題，整理其製作背景、特色與相關研究資訊。",

        "image_note": "黑蒜頭產品照片",

        "image": "black-garlic.png",

        "price": 450,

        "unit": "份",

        "ingredients": "黑蒜頭",

        "weight": "180公克",

        "shelf life": "常溫下18個月",

        "origin": "台灣",

    },



    "black-garlic-extract": {

        "name": "黑蒜精",

        "subtitle": "黑蒜精產品介紹",

        "description": "本頁介紹競賽作品中的黑蒜精。產品型態、製作方式與規格請依實際產品資料補充。",

        "image_note": "黑蒜精產品照片",

        "image": "black-garlic-extract.png",

        "price": 560,

        "unit": "6入／組",

        "ingredients": "水、黑蒜、黑糖",

        "weight": "65毫升",

        "shelf life": "常溫下兩年（未拆封）",

        "origin": "台灣",

    },



    "black-garlic-wine": {

        "name": "黑蒜酒",

        "subtitle": "黑蒜酒產品介紹",

        "description": "本頁介紹競賽作品中的黑蒜酒。原料、酒精濃度與產品規格請依實際標示補充。",

        "image_note": "黑蒜酒產品照片",

        "image": "black-garlic-wine.png",

        "price": 1500,

        "unit": "瓶",

        "ingredients": "黑蒜、高粱酒糟",

        "weight": "待補",

        "shelf life": "待補",

        "origin": "待補",

    },

}





# ==============================

# 網站共用版型

# ==============================



PAGE = """

<!doctype html>

<html lang="zh-Hant">



<head>

    <meta charset="utf-8">

    <meta name="viewport" content="width=device-width, initial-scale=1">



    <title>{{ title }}｜一蒜釀百味</title>


    <style>



        :root {

            --wine: #4b1f1c;

            --red: #8d3027;

            --gold: #d8a34a;

            --cream: #f8f3e9;

            --ink: #2d2925;

            --muted: #766c62;

        }



        * {

            box-sizing: border-box;

        }



        body {

            margin: 0;

            font-family: "Microsoft JhengHei", "Noto Sans TC", sans-serif;

            background: var(--cream);

            color: var(--ink);

            line-height: 1.75;

        }



        header {

            background: var(--wine);

            color: white;

            padding: 20px 5%;

        }



        .nav {

            max-width: 1120px;

            margin: auto;

            display: flex;

            align-items: center;

            justify-content: space-between;

            gap: 20px;

            flex-wrap: wrap;

        }



        .brand {

            font-size: 22px;

            font-weight: 800;

        }



        nav {

            display: flex;

            flex-wrap: wrap;

            gap: 18px;

        }



        nav a {

            color: white;

            text-decoration: none;

        }



        nav a:hover {

            color: #f4ce82;

        }



        .hero {

            background: linear-gradient(120deg, #4b1f1c, #8d3027);

            color: white;

            padding: 65px 20px;

        }



        .hero-inner {

            max-width: 1120px;

            margin: auto;

        }



        .eyebrow {

            color: #f4ce82;

            letter-spacing: 2px;

            font-weight: bold;

        }



        h1 {

            font-size: clamp(32px, 5vw, 54px);

            line-height: 1.25;

            margin: 12px 0;

        }



        .hero p {

            max-width: 700px;

            font-size: 18px;

        }



        main {

            max-width: 1120px;

            margin: 36px auto;

            padding: 0 20px;

        }



        .section-title {

            margin-bottom: 18px;

        }



        .section-title h2 {

            margin-bottom: 4px;

            color: var(--wine);

        }



        .section-title p {

            margin-top: 0;

            color: var(--muted);

        }



        .grid {

            display: grid;

            grid-template-columns: repeat(

                auto-fit,

                minmax(230px, 1fr)

            );

            gap: 20px;

        }



        .card {

            background: white;

            border: 1px solid #eee3d5;

            border-radius: 14px;

            padding: 22px;

            box-shadow: 0 6px 18px #40251a0c;

        }



        .card h3 {

            color: var(--wine);

            margin-top: 18px;

        }



        .card h3:first-child {

            margin-top: 0;

        }



        .activity-card {

            padding: 16px 18px;

            margin: 16px 0;

            border: 1px solid #eee3d5;

            border-radius: 10px;

            background: #fffdf9;

        }



        .activity-card h3 {

            margin: 0 0 8px;

        }



        .activity-card p {

            margin: 0;

        }



        .product-image {

            min-height: 150px;

            display: grid;

            place-items: center;

            text-align: center;

            border-radius: 10px;

            background: #f1e5d5;

            color: #7b5b3b;

            font-size: 18px;

            font-weight: bold;

            margin-bottom: 16px;

        }



        .button {

            display: inline-block;

            background: var(--red);

            color: white;

            text-decoration: none;

            padding: 10px 17px;

            border-radius: 7px;

            margin-top: 8px;

            border: none;

            cursor: pointer;

        }



        .button:hover {

            background: var(--wine);

        }



        .button.secondary {

            background: #eee4d8;

            color: var(--wine);

        }



        .notice {

            background: #fff8e8;

            border-left: 4px solid var(--gold);

            padding: 14px 18px;

            border-radius: 8px;

            margin-top: 20px;

        }



        .detail-list {

            padding: 0;

            list-style: none;

        }



        .detail-list li {

            padding: 10px 0;

            border-bottom: 1px solid #eee6dd;

        }



        .small {

            color: var(--muted);

            font-size: 14px;

            overflow-wrap: anywhere;

        }



        footer {

            background: #33231f;

            color: #eee1d2;

            text-align: center;

            padding: 25px 15px;

            margin-top: 50px;

        }



        /* 線上訂購商品區 */



        .shop-grid {

            display: grid;

            grid-template-columns: repeat(

                auto-fit,

                minmax(230px, 1fr)

            );

            gap: 20px;

        }



        .shop-card {

            background: white;

            border: 1px solid #eee3d5;

            border-radius: 14px;

            padding: 18px;

            box-shadow: 0 6px 18px #40251a0c;

        }



        .shop-card img {

            width: 100%;

            height: 210px;

            object-fit: contain;

            background: #f8f3e9;

            border-radius: 10px;

        }



        .shop-price {

            color: var(--red);

            font-size: 25px;

            font-weight: 800;

            margin: 8px 0;

        }



        .order-panel {

            margin-top: 28px;

            background: white;

            border: 1px solid #eee3d5;

            border-radius: 14px;

            padding: 24px;

        }



        .order-form-grid {

            display: grid;

            grid-template-columns: repeat(

                auto-fit,

                minmax(220px, 1fr)

            );

            gap: 16px;

        }



        .form-field label {

            display: block;

            font-weight: 700;

            margin-bottom: 6px;

        }



        .form-field input,

        .form-field textarea {

            width: 100%;

            padding: 11px;

            border: 1px solid #d9cfc3;

            border-radius: 7px;

            font: inherit;

        }



        .quantity-input {

            width: 90px;

            padding: 8px;

            border: 1px solid #d9cfc3;

            border-radius: 7px;

            font: inherit;

        }



        .total-hint {

            background: #fff8e8;

            padding: 14px;

            border-radius: 8px;

            margin: 18px 0;

        }



        @media (max-width: 620px) {



            nav {

                gap: 10px;

            }



            .nav {

                align-items: flex-start;

            }



            .brand {

                width: 100%;

            }



        }



    </style>

</head>



<body>



<header>

    <div class="nav">



        <div class="brand">

            黑蒜頭｜競賽展示

        </div>



        <nav>

            <a href="/">首頁</a>

            <a href="/black-garlic">認識黑蒜頭</a>

            <a href="/shop">線上訂購</a>

            <a href="/#products">產品介紹</a>
        </nav>
    </div>
</header>
{{ content|safe }}
<footer>

    <div>金門黑蒜｜一蒜釀百味</div>

    <div class="small">

        產品資訊與研究內容以正式資料及產品標示為準

    </div>

</footer>



</body>

</html>

"""





# ==============================

# 首頁

# ==============================



@app.route("/")

def home():



    product_cards = ""



    for product_id, product in PRODUCTS.items():



        product_cards += f"""

        <article class="card">



            <div class="product-image">



                <img

                    src="{url_for('product_image', filename=product['image'])}"

                    alt="{product['name']}"

                    style="

                        width:100%;

                        height:220px;

                        object-fit:contain;

                        border-radius:10px;

                    "

                >



            </div>



            <h3>{product["name"]}</h3>



            <p>{product["description"]}</p>



            <a class="button" href="/product/{product_id}">

                查看產品

            </a>



        </article>

        """



    content = f"""



    <section class="hero">



        <div class="hero-inner">



            <div class="eyebrow">

                競賽作品介紹

            </div>



            <h1>

                從黑蒜頭出發<br>

                認識多元食品應用

            </h1>



            <p>

                本網站以黑蒜頭為主題，介紹黑蒜頭、黑蒜精與黑蒜酒，

                並整理產品資訊、研究背景與安全說明，方便評審快速瀏覽。

            </p>



            <a class="button" href="#products">

                查看產品

            </a>



        </div>



    </section>





    <main>



        <section class="section-title">



            <h2>認識黑蒜頭</h2>



            <p>

                從原料、熟成概念到產品應用，逐步了解本競賽作品。

            </p>



        </section>





        <section class="card">



            <p>

                黑蒜頭是本網站的介紹主題。熟成條件、原料來源與作品特色，

                將依競賽資料及實際製作紀錄補充。

            </p>



            <a class="button" href="/black-garlic">

                閱讀黑蒜頭介紹

            </a>



        </section>





        <section

            id="products"

            class="section-title"

            style="margin-top:38px"

        >



            <h2>產品介紹</h2>



            <p>

                選擇產品查看詳細介紹與產品資訊。

            </p>



        </section>





        <section class="grid">

            {product_cards}

        </section>





        <section

            class="section-title"

            style="margin-top:38px"

        >



            <h2>線上訂購</h2>



            <p>

                喜歡黑蒜系列產品嗎？歡迎直接選購。

            </p>



        </section>





        <section class="card">



            <p>

                黑蒜頭、黑蒜精及黑蒜酒皆可於線上選擇數量，

                填寫聯絡與收件資料後送出訂單。

            </p>



            <a class="button" href="/shop">

                立即前往訂購

            </a>



        </section>



    </main>



    """



    return render_template_string(

        PAGE,

        title="首頁",

        content=content

    )





# ==============================

# 黑蒜頭生理活性介紹

# ==============================



@app.route("/black-garlic")

def black_garlic():



    content = """



    <main>



        <section class="section-title">



            <h2>黑蒜頭生理活性介紹</h2>



            <p>

                黑蒜頭的形成機制、主要活性成分與潛在生理保健功效

            </p>



        </section>





        <section class="card">



            <h3>黑蒜頭是如何形成的？</h3>



            <p>

                黑蒜頭是一種利用高溫、高濕環境，將新鮮大蒜進行熟成轉化的加工產品。

                在熟成過程中，大蒜原本不穩定且具有刺激性氣味的化合物會產生轉變，

                形成較穩定且氣味較溫和的成分，例如 S-烯丙基半胱胺酸

                （S-Allylcysteine, SAC）。同時，熟成過程也會促使多種具有潛在

                生理活性的成分生成，因此黑蒜頭具有進一步開發及驗證保健功效的研究價值。

            </p>





            <h3>黑蒜頭的主要生理活性</h3>





            <div class="activity-card">



                <h3>1. 抗氧化作用</h3>



                <p>

                    黑蒜頭經過生物轉化後，其總酚、類黃酮及 SOD-like 活性等指標

                    可能高於新鮮大蒜。此外，熟成過程會改變大蒜中的含硫化合物組成，

                    進而提升其抗氧化相關活性，顯示黑蒜頭具有潛在的抗氧化能力。

                </p>



            </div>





            <div class="activity-card">



                <h3>2. 降血糖作用</h3>



                <p>

                    在第二型糖尿病動物實驗中，研究發現餵食黑蒜頭的實驗組，

                    其肝臟相關抗氧化酵素活性及抗氧化物質表現有所提升。

                    研究推測黑蒜頭可能具有改善氧化壓力的作用，

                    並有助於降低糖尿病相關併發症的風險。

                </p>



            </div>





            <div class="activity-card">



                <h3>3. 改善動脈粥狀硬化</h3>



                <p>

                    研究指出，黑蒜頭的氯仿萃取物具有潛在的血管保護作用，

                    可作為抑制或改善動脈粥狀硬化相關疾病的研究方向，

                    顯示黑蒜頭在心血管保健領域具有進一步研究的價值。

                </p>



            </div>





            <div class="activity-card">



                <h3>4. 抗腫瘤作用</h3>



                <p>

                    在胃癌動物實驗中，研究發現餵食黑蒜頭可能具有抑制腫瘤生長的效果，

                    且呈現一定的劑量效應。此外，研究也觀察到血清中 SOD 活性提升，

                    推測可能與黑蒜頭的抗氧化能力及免疫調節作用有關。

                </p>



            </div>





            <div class="activity-card">



                <h3>5. 改善肥胖作用</h3>



                <p>

                    研究發現，黑蒜甲醇萃取物具有抑制脂肪細胞增生及分化的潛力，

                    並可能影響脂質生合成與脂肪細胞激素相關基因的表現。

                    相關細胞及動物研究顯示，黑蒜頭可能具有調節脂質代謝、

                    抑制脂肪堆積的作用。

                </p>



            </div>





            <div class="activity-card">



                <h3>6. 護肝作用</h3>



                <p>

                    在酒精性肝氧化損傷的動物實驗中，研究發現連續四週餵食黑蒜頭，

                    可降低實驗動物肝臟中的脂肪堆積。推測黑蒜頭可能透過其抗氧化能力，

                    減少氧化壓力，並對慢性酒精性肝損傷產生一定的保護作用。

                </p>



            </div>





            <div class="notice">



                <strong>研究提醒：</strong>



                上述生理活性主要來自文獻中的動物及細胞實驗結果。



            </div>





            <p>



                <a

                    class="button"

                    href="/product/black-garlic"

                >

                    查看黑蒜頭產品

                </a>



                <a

                    class="button secondary"

                    href="/research"

                >

                    查看研究與安全說明

                </a>



            </p>



        </section>



    </main>



    """



    return render_template_string(

        PAGE,

        title="黑蒜頭生理活性介紹",

        content=content

    )





# ==============================

# 舊研究頁面轉址

# ==============================



@app.route("/research")

def research():



    return redirect(url_for("shop"))





# ==============================

# 線上訂購頁面

# ==============================



@app.route("/shop")

def shop():



    shop_cards = ""



    for product_id, product in PRODUCTS.items():



        shop_cards += f"""



        <article class="shop-card">



            <img

                src="{url_for('product_image', filename=product['image'])}"

                alt="{product['name']}"

            >



            <h3>{product['name']}</h3>



            <div class="shop-price">

                NT${product['price']:,}

            </div>



            <p>

                {product['unit']}｜{product['description']}

            </p>



            <label for="qty-{product_id}">

                購買數量

            </label>



            <br>



            <input

                class="quantity-input"

                id="qty-{product_id}"

                type="number"

                name="quantity_{product_id}"

                form="order-form"

                min="0"

                max="99"

                value="0"

            >



        </article>



        """





    content = f"""



    <main>



        <section class="section-title">



            <h2>黑蒜系列｜線上訂購</h2>



            <p>

                嚴選黑蒜系列商品，選擇品項與數量即可填寫訂單。

            </p>



        </section>





        <form

            id="order-form"

            method="POST"

            action="/place-order"

        >



            <section class="shop-grid">



                {shop_cards}



            </section>





            <section class="order-panel">



                <h2>填寫訂購資料</h2>



                <p class="small">

                    請確認商品數量及聯絡資料，送出後系統會保存訂單紀錄。

                </p>





                <div class="order-form-grid">



                    <div class="form-field">



                        <label for="customer_name">

                            訂購人姓名 *

                        </label>



                        <input

                            id="customer_name"

                            name="customer_name"

                            required

                            maxlength="80"

                        >



                    </div>





                    <div class="form-field">



                        <label for="phone">

                            聯絡電話 *

                        </label>



                        <input

                            id="phone"

                            name="phone"

                            type="tel"

                            required

                            maxlength="30"

                        >



                    </div>





                    <div

                        class="form-field"

                        style="grid-column:1/-1"

                    >



                        <label for="address">

                            收件地址 *

                        </label>



                        <input

                            id="address"

                            name="address"

                            required

                            maxlength="250"

                        >



                    </div>





                    <div

                        class="form-field"

                        style="grid-column:1/-1"

                    >



                        <label for="note">

                            訂單備註

                        </label>



                        <textarea

                            id="note"

                            name="note"

                            rows="3"

                            maxlength="500"

                            placeholder="例如：方便收貨時段、其他需求（選填）"

                        ></textarea>



                    </div>



                </div>





                <p style="margin-top:18px">



                    <label>



                        <input

                            type="checkbox"

                            name="age_confirm"

                            value="yes"

                        >



                        若訂購黑蒜酒，我確認已符合所在地法定購買及飲酒年齡。



                    </label>



                </p>





                <div class="total-hint">



                    <strong>價格說明：</strong>



                    黑蒜頭 NT$450／份；

                    黑蒜精 NT$560／6入；

                    黑蒜酒 NT$1,500／瓶。



                    運費及付款方式請由賣方另行確認。



                </div>





                <button

                    class="button"

                    type="submit"

                    style="border:0;cursor:pointer;font:inherit"

                >

                    送出訂單

                </button>





                <a

                    class="button secondary"

                    href="/"

                >

                    返回首頁

                </a>



            </section>



        </form>



    </main>



    """



    return render_template_string(

        PAGE,

        title="線上訂購",

        content=content

    )





# ==============================

# 訂單處理

# ==============================



@app.route("/place-order", methods=["POST"])

def place_order():



    customer_name = request.form.get(

        "customer_name", ""

    ).strip()



    phone = request.form.get(

        "phone", ""

    ).strip()



    address = request.form.get(

        "address", ""

    ).strip()



    note = request.form.get(

        "note", ""

    ).strip()



    age_confirm = (

        request.form.get("age_confirm") == "yes"

    )





    if not customer_name or not phone or not address:



        return "請填寫姓名、電話及收件地址。", 400





    order_items = []

    total = 0





    for product_id, product in PRODUCTS.items():



        try:



            quantity = int(

                request.form.get(

                    f"quantity_{product_id}",

                    "0"

                )

            )



        except (TypeError, ValueError):



            quantity = 0





        if quantity < 0 or quantity > 99:



            return "商品數量請填寫 0 至 99。", 400





        if quantity:



            if (

                product_id == "black-garlic-wine"

                and not age_confirm

            ):



                return (

                    "訂購黑蒜酒前，請先確認符合所在地法定購買及飲酒年齡。",

                    400

                )





            subtotal = quantity * product["price"]



            total += subtotal



            order_items.append(

                f"{product['name']} x {quantity}（NT${subtotal:,}）"

            )





    if not order_items:



        return "請至少選擇一項商品及購買數量。", 400





    # 建立訂單編號



    order_id = datetime.now().strftime(

        "BG%Y%m%d%H%M%S"

    )





    # 儲存訂單 CSV



    order_file = (

        Path(__file__).resolve().parent / "orders.csv"

    )



    file_exists = order_file.exists()





    with order_file.open(

        "a",

        newline="",

        encoding="utf-8-sig"

    ) as file:



        writer = csv.writer(file)



        if not file_exists:



            writer.writerow([

                "訂單編號",

                "訂購時間",

                "姓名",

                "電話",

                "收件地址",

                "商品明細",

                "商品總額",

                "備註"

            ])





        writer.writerow([



            order_id,



            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            ),



            customer_name,



            phone,



            address,



            "；".join(order_items),



            total,



            note



        ])





    # 訂單完成頁面



    item_list = "".join(

        f"<li>{escape(item)}</li>"

        for item in order_items

    )



    safe_name = escape(customer_name)



    safe_phone = escape(phone)



    safe_address = escape(address)





    content = f"""



    <main>



        <section class="section-title">



            <h2>訂單已收到</h2>



            <p>

                感謝您的訂購，請保存以下訂單資訊。

            </p>



        </section>





        <section class="card">



            <h3>

                訂單編號：{order_id}

            </h3>





            <ul>

                {item_list}

            </ul>





            <h2 style="color:var(--red)">

                商品總額：NT${total:,}

            </h2>





            <p>

                <strong>訂購人：</strong>

                {safe_name}

            </p>





            <p>

                <strong>聯絡電話：</strong>

                {safe_phone}

            </p>





            <p>

                <strong>收件地址：</strong>

                {safe_address}

            </p>





            <p class="notice">



                訂單已記錄於網站主程式資料夾的 orders.csv。



                目前網站尚未串接線上金流、物流或自動通知功能；



                請由賣方聯絡買家確認庫存、運費、付款及出貨事宜。



            </p>





            <a

                class="button"

                href="/shop"

            >

                繼續選購

            </a>





            <a

                class="button secondary"

                href="/"

            >

                返回首頁

            </a>



        </section>



    </main>



    """





    return render_template_string(

        PAGE,

        title="訂單已收到",

        content=content

    )





# ==============================

# 商品詳細介紹

# ==============================



@app.route("/product/<product_id>")

def product_detail(product_id):



    product = PRODUCTS.get(product_id)



    if product is None:



        abort(404)





    details = [



        ("成分", product["ingredients"]),



        ("重量／容量", product["weight"]),



        ("保存期限", product["shelf life"]),



        ("產品資料來源", product["origin"]),



    ]





    detail_rows = "".join(



        f"<li><strong>{label}：</strong>{value}</li>"



        for label, value in details



    )





    content = f"""



    <main>



        <section class="section-title">



            <h2>

                {product["name"]}

            </h2>



            <p>

                {product["subtitle"]}

            </p>



        </section>





        <section class="card">



            <div class="product-image">



                <img



                    src="{url_for('product_image', filename=product['image'])}"



                    alt="{product['name']}"



                    style="

                        width:100%;

                        max-height:320px;

                        object-fit:contain;

                        border-radius:10px;

                    "



                    onerror="

                        this.style.display='none';

                        this.parentElement.innerHTML='圖片尚未找到：請確認圖片已放入 static/images 資料夾';

                    "



                >



            </div>





            <p>

                {product["description"]}

            </p>





            <h3>

                產品資訊

            </h3>





            <p class="shop-price">



                NT${product["price"]:,}／{product["unit"]}



            </p>





            <ul class="detail-list">



                {detail_rows}



            </ul>





            </p>





            <a

                class="button"

                href="/shop"

            >

                立即訂購

            </a>





            <a

                class="button secondary"

                href="/"

            >

                返回首頁

            </a>



        </section>



    </main>



    """





    return render_template_string(

        PAGE,

        title=product["name"],

        content=content

    )





# ==============================

# 啟動網站

# ==============================



if __name__ == "__main__":



    app.run(debug=True)