# maple-cs-parper
Simple tool to scrape upcoming cash shop sales in MapleStory


# Usage

This tool is very primitive and manual. I don't know how to parse WZ files yet, so this relies on other tools such as HaRepacker or WzComparerR2 to extract XML data from WZ images.

From String.wz, we must extract the `Cash`, `Pet`, `Equip`, and in the future, `Package` images. These are placed into the `strings` folder so we can match Item IDs to strings.

Item IDs are acquired from extracting `Commodity.img` from `Etc.wz` and filtering down to only certain term starts. This is very scuffed, I will hopefully come up with a better solution in the future.

