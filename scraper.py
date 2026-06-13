import pandas as pd

from playwright.sync_api import sync_playwright


def scrape_twingos():
    with sync_playwright() as p:
        print("Connecting to the running Chrome instance...")
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        default_context = browser.contexts[0]
        page = default_context.pages[0]

        print("Navigating to Hasznaltauto.hu...")
        page.goto("https://www.hasznaltauto.hu/talalatilista/PCOHKVG3R2NTAEH5C57UDAFEXP2T5NVKCSUYV6WUK42ICCLRWA6ZC3OQEZI75PLDEBMYHURHIZT65R3HABM3ZS43S5MS4RILAENXECTW3CFQ7RRSFH6BKDPKBN2ICBTIFUC6Q6PAN3BI7SWVDDIPOUEDX6FI7PK4JVCXVBRVXDJCQG4LVSSBASYPPSTJ5DIU3C4XFFVXPPSYQ2OP73ONLAQO4UEZZ2MGHJJGJQ7XJWFAMHGYJKAVN7SFIAPDOBKN62CY667O2GQT4YVAC7XO6UXQPTSFLQAQZJDZWJJN6QFU4AKOB6OBOPPQAZGNJNVGBHFZ4WFSOAFD5FXFNUOPUTQHD4D6BUPTZUYMT67SBV7HQ5YYKNZK4U3VH2IPTLL47DR4QUCQMS37L2H6G2YPO553TM3FXCJJU6XMV2QIVZI3MKJLWILKWQHOVMSPZX6NYMMHALMUVKHMKCVGFNNUOK7SIU2WUPLZTCRKZWAUMLGAT2W47EJ6VBKOWBT6EIOMRF4YECJRVXVPSIPUCTCNYHCYXEQ3IZRJX2MWXJR6D2YGHVMDXVAPHLALLLBZTAXYAC4ZCNZVJJ5ZBAES3FUOPUOOI65YQ5RR3LVWRL2HTMP6VTQGWNYUJW5A5NOFQDRW67G66ISSPYFNJFRMKYBV6S3WDI644UC6QJM5I2FO2TDKCOPKGYIBYL6ZICAPJJJZTC6L7NVM6I3MKWIWZLJUC7NGMDDCQ2TMIMKJCL3BV5QZMFD35CHEK26VAIHGRTVR66WNU4DZ5B5HK3OJL35NJR2MUA7S6BXNZHJJCHBVFH7DN7SJ7D2FFFAPW7K4VTCWRW7QF3UG62BL4PEQNNAJWZGO7NEDEH6DJ6VDVAZWDH3P4DYQAWPRI")

        # Várunk picit, hogy az oldal biztosan betöltsön
        page.wait_for_timeout(3000)

        print("Extracting data from all ads on the page...")

        # 1. Lekérjük az ÖSSZES hirdetés kártyáját egy listába
        ad_cards = page.locator(".talalati-sor").all()
        print(f"Found {len(ad_cards)} ads on this page.")

        # Üres lista a szótáraknak
        cars_data = []

        # 2. Végigmegyünk a kártyákon egy ciklussal
        for card in ad_cards:
            try:
                # Robusztus kinyerés a .first használatával
                title = card.locator(".cim-kontener h3 a").first.inner_text()

                # A href attribútum kinyerése a linkhez
                link = card.locator(".cim-kontener h3 a").first.get_attribute("href")

                price = card.locator(".pricefield-primary").first.inner_text()

                # Hozzáadjuk az adatokat a listához egy dictionary formájában
                cars_data.append({
                    "Title": title,
                    "Price": price,
                    "Link": link
                })
            except Exception as e:
                # Ha egy kártya nagyon törött, nem áll le a kód, csak megy a következőre
                print(f"Skipped an ad due to missing data. Error: {e}")

        # 3. Pandas integráció és export
        if cars_data:
            df = pd.DataFrame(cars_data)
            df.to_csv("raw_cars_data.csv", index=False, encoding='utf-8')
            print("\n--- SCRAPING SUCCESSFUL ---")
            print(f"Exported {len(df)} cars to raw_cars_data.csv")
            print(df.head())  # Kiírjuk az első 5 sort a konzolba ellenőrzésképp
        else:
            print("No data was extracted. Check your selectors.")


if __name__ == "__main__":
    scrape_twingos()