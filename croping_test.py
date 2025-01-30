from extractor import Extractor

if __name__ == "__main__":
  extractor = Extractor()
  

  # croped_dealer_zone_p1 = extractor.crop_zone(extractor.PLAYER_ZONES[2]["pot"], ofp="zones/p2/pot.png", ifp="screenshots/p1.png")

  print(extractor.define_card_suit("zones/board/4.png"))
    # print(extractor.get_most_frequent_non_white_color("zones/total_pot.png"))

