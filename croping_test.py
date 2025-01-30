from extractor import Extractor

if __name__ == "__main__":
  extractor = Extractor()
  
  first_card = (1070, 440, 1110, 489)
  second_card = (1122, 440, 1165, 489)
  p_n = 7

  extractor.crop_zone(first_card, f'zones/p{p_n}/first_card.png', "screenshots\p6.png")
  extractor.crop_zone(second_card, f'zones/p{p_n}/second_card.png', "screenshots\p6.png")

  # print(extractor.tesseract_number_recognition("zones/p2/pot.png"))
    # print(extractor.get_most_frequent_non_white_color("zones/total_pot.png"))

