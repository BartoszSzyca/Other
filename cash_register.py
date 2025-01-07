class CashRegister:
    def __init__(self):
        self.products_prices = self.load_products_prices()
        self.selected_products = []

    def __str__(self):
        title = (f"||Lp.|"
                 f"{'Dostępne Produkty'.ljust(20)}|"
                 f"{'Cena Netto'.ljust(11)}|"
                 f"{'Cena Brutto'.ljust(11)}|"
                 f"VAT||\n"
                 )
        separator = "=" * len(title) + "\n"
        result = separator
        result += title
        result += "-" * len(title) + "\n"
        for lp, (product, details) in enumerate(self.products_prices.items(),
                                                start=1):
            netto = details['netto']
            vat = details['vat']
            gross = self.calculate_gross(netto, vat)
            result += (f"||{str(lp) + '.'.ljust(2)}|"
                       f"{product.ljust(20)}|"
                       f"{f'{netto:.2f}'.rjust(9)}zł|"
                       f"{f'{gross:.2f}'.rjust(9)}zł|"
                       f"{str(vat).rjust(2)}%||\n"
                       )
        result += separator
        return result

    def products_from_user(self):
        print("Podaj nazwy produktów "
              "(po jednym na linię, wpisz 'KONIEC' aby zakończyć):")
        while True:
            product = input("Produkt: ").capitalize()
            if product.upper() == "KONIEC":
                self.save_receipt_to_file()
                break
            if product not in self.products_prices:
                print("Nie ma takiego produktu")
                continue
            self.selected_products.append(product)

    def calculate_gross(self, netto, vat):
        return netto + (netto * vat / 100)

    def calculate_summary(self):
        summary = {}
        for product in self.selected_products:
            if product in summary:
                summary[product] += 1
            else:
                summary[product] = 1
        return summary

    def generate_receipt(self):
        total = 0
        summary = self.calculate_summary()
        title = (f"Lp.|"
                 f"{'Produkt'.ljust(20)}|"
                 f"{'Ilość'.ljust(5)}|"
                 f"{'Cena Brutto'.ljust(11)}|\n"
                 )
        separator = "-" * len(title) + "\n"
        receipt = "=" * (len(title) // 2 - 4) + " Paragon " + "=" * (len(title)
                                                                     // 2 - 4
                    ) + "\n"
        receipt += title
        receipt += separator
        for lp, (product, quantity) in enumerate(summary.items(), start=1):
            netto = self.products_prices[product]["netto"]
            vat = self.products_prices[product]["vat"]
            gross = self.calculate_gross(netto, vat)
            receipt += (f"{str(lp) + '.'.ljust(2)}|"
                        f"{product.ljust(20)}|"
                        f"{str(quantity).rjust(5)}|"
                        f"{f'{quantity*gross:.2f}'.rjust(9)}zł|\n"
                        )
            total += gross*quantity
        receipt += separator
        receipt += f"Razem: {total}zł".rjust(len(title))
        return receipt

    def save_receipt_to_file(self):
        receipt = self.show_receipt()
        with open("receipt.txt", "w", encoding="utf-8") as file:
            file.write(receipt)
        print(f"\nParagon zapisany do pliku: 'receipt.txt'. Oto jego zawartość:\n\n"
              f"{receipt}")

    def show_receipt(self):
        return self.generate_receipt()

    def load_products_prices(self):
        with open("products_prices.txt" , 'r', encoding="utf-8") as file:
            products_prices = {}
            for line in file:
                product, netto ,vat = line.strip().split(',')
                products_prices[product] = {"netto": float(netto), 'vat': int(vat)}
        return products_prices


if __name__ == "__main__":
    print()
    CR = CashRegister()
    print(CR)
    CR.products_from_user()
