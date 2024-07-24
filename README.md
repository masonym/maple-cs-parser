# maple-cs-parser
Simple tool to scrape upcoming cash shop sales in MapleStory

## [View the live site here!](https://masonym.dev/ms-upcoming-sales)

This project involves datamining files for the MMORPG MapleStory developed by Nexon. The purpose of the project is to extract upcoming sales data for the in-game store, and display it on a reactive website for members of the community to be able to view before they are officially available. 

# Usage

This tool relies on some method of dumping WZ files, such as [HaRepacker](https://github.com/lastbattle/Harepacker-resurrected), [WzComparerR2](https://github.com/Kagamia/WzComparerR2), or [WZ-Dumper](https://github.com/Xterminatorz/WZ-Dumper). Depending on the method used, you will likely need to modify the global variables in `item_matcher.py` to fit your file structure. 

### To Update Cloudflare KV:

1. Dump updated WZ via method of choice, as seen above.
2. Run `python main.py` in `/item-info-generator` (this generates `item_data.json`)
3. Run `node src/update_kv.js` in `/item-info-worker`
4. Deploy worker with `wrangler deploy` in `/item-info-worker`

### To view site locally:

1. Run `npm start` in `/upcoming-sales-website`


---

# Technology used

* [WZ-Dumper](https://github.com/Xterminatorz/WZ-Dumper) for extracting wz files
* Python for XML parsing
* Wrangler for generating an API via Cloudflare worker
* React for displaying data from api to static site
    * Axios for HTTP requests

# Some useful information regarding .wz file structure:

* Strings for Pets, Cash Items, and Equips are contained in String.wz. These include names and descriptions for given item IDs. The relevant files are `Pet.img`, `Cash.img`, and `Eqp.img`
* Sales data and cash shop package contents are contained in `Etc.wz`. Sales data is stored in `Commodity.img`, and cash packages are stored in `CashPackage.img`
* Names and descriptions of cash packages are stored in `Item.wz`, specifically in `Special/0910.img`

# Eventual Features:

* I would like to figure out how to read WZ files in order to make this more efficient - dumping the entire game into XML files is quite time consuming, though for now I'm not worried about it because updates come seldomly anyways.
* Search function for front end
* World filtering for front end 
