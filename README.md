# maple-cs-parser
Simple tool to scrape upcoming cash shop sales in MapleStory


# Usage

This tool is very primitive for now. I don't know how to parse WZ files yet, so this relies on other tools such as HaRepacker or WzComparerR2 to extract XML data from WZ images.

From String.wz, we must extract the `Cash`, `Pet`, and `Equip` images. These are placed into the `strings` folder so we can match Item IDs to strings.
From Etc.wz, we must extract the `Commodity` and `CashPackage` images. `Commodity.img` contains upcoming sale data, and `CashPackage` contains package sub-item IDs.
From Item.wz, we must extract `Special.910.img` - this is where the names and descriptions of cash packages are stored.

Item IDs are acquired from extracting `Commodity.img` from `Etc.wz` and filtering down to sales starting in the current month onwards.

# Todo:

* Automate WZ IMG extracting/XML dumping
* Clean up and refactor code.
	* Global variables for XML dirs
	* Dedicated function for parsing XML files 
	* Pass qualifying_dirs instead of writing to file
* Potentially add Markdown formatting to output
* Automatically post to a website somewhere
* Eventually add images