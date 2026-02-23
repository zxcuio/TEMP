import csv
import sys

# Define lists of proper nouns to capitalize
months = {
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec"
}

days = {
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "mon", "tue", "wed", "thu", "fri", "sat", "sun"
}

holidays = {
    "christmas", "easter", "thanksgiving", "halloween", "valentine",
    "new year", "good friday", "labor day", "memorial day", "veterans day",
    "independence day", "hanukkah", "passover", "ramadan", "diwali",
    "kwanzaa", "boxing day", "epiphany", "lent", "advent", "pentecost"
}

countries_regions = {
    "africa", "antarctica", "asia", "australia", "europe", "north america", "south america",
    "afghanistan", "albania", "algeria", "andorra", "angola", "antigua", "argentina", "armenia",
    "austria", "azerbaijan", "bahamas", "bahrain", "bangladesh", "barbados", "belarus",
    "belgium", "belize", "benin", "bhutan", "bolivia", "bosnia", "botswana", "brazil", "brunei",
    "bulgaria", "burkina", "burundi", "cambodia", "cameroon", "canada", "cape verde", "central african republic",
    "chad", "chile", "china", "colombia", "comoros", "congo", "costa rica", "croatia", "cuba",
    "cyprus", "czech", "denmark", "djibouti", "dominica", "dominican republic", "east timor", "ecuador",
    "egypt", "el salvador", "equatorial guinea", "eritrea", "estonia", "ethiopia", "fiji", "finland",
    "france", "gabon", "gambia", "georgia", "germany", "ghana", "greece", "grenada", "guatemala",
    "guinea", "guinea-bissau", "guyana", "haiti", "honduras", "hungary", "iceland", "india", "indonesia",
    "iran", "iraq", "ireland", "israel", "italy", "ivory coast", "jamaica", "japan", "jordan",
    "kazakhstan", "kenya", "kiribati", "korea", "kosovo", "kuwait", "kyrgyzstan", "laos", "latvia",
    "lebanon", "lesotho", "liberia", "libya", "liechtenstein", "lithuania", "luxembourg", "macedonia",
    "madagascar", "malawi", "malaysia", "maldives", "mali", "malta", "marshall islands", "mauritania",
    "mauritius", "mexico", "micronesia", "moldova", "monaco", "mongolia", "montenegro", "morocco",
    "mozambique", "myanmar", "namibia", "nauru", "nepal", "netherlands", "new zealand", "nicaragua",
    "niger", "nigeria", "norway", "oman", "pakistan", "palau", "panama", "papua new guinea", "paraguay",
    "peru", "philippines", "poland", "portugal", "qatar", "romania", "russia", "rwanda", "saint kitts",
    "saint lucia", "saint vincent", "samoa", "san marino", "sao tome", "saudi arabia", "senegal",
    "serbia", "seychelles", "sierra leone", "singapore", "slovakia", "slovenia", "solomon islands",
    "somalia", "south africa", "spain", "sri lanka", "sudan", "suriname", "swaziland", "sweden",
    "switzerland", "syria", "taiwan", "tajikistan", "tanzania", "thailand", "togo", "tonga",
    "trinidad", "tunisia", "turkey", "turkmenistan", "tuvalu", "uganda", "ukraine", "united arab emirates",
    "united kingdom", "united states", "uruguay", "uzbekistan", "vanuatu", "vatican", "venezuela",
    "vietnam", "yemen", "zambia", "zimbabwe", "usa", "uk", "ussr", "eu", "un", "nato", "asean",
    "american", "british", "english", "french", "german", "italian", "japanese", "chinese", "russian",
    "spanish", "indian", "arabic", "portuguese", "dutch", "greek", "latin", "hebrew", "hindi",
    "swahili", "persian", "korean", "vietnamese", "thai", "turkish", "swedish", "danish", "norwegian",
    "finnish", "polish", "hungarian", "czech", "slovak", "romanian", "bulgarian", "serbian", "croatian",
    "bosnian", "albanian", "macedonian", "slovenian", "ukrainian", "belarusian", "estonian", "latvian",
    "lithuanian", "georgian", "armenian", "azerbaijani", "kazakh", "uzbek", "turkmen", "tajik", "kyrgyz",
    "mongolian", "tibetan", "nepali", "bengali", "tamil", "telugu", "kannada", "malayalam", "sinhala",
    "urdu", "punjabi", "gujarati", "marathi", "odia", "assamese", "maithili", "santali", "bodo", "dogri",
    "kashmiri", "konkani", "manipuri", "sanskrit", "sindhi"
}

cities = {
    "london", "paris", "new york", "tokyo", "beijing", "moscow", "rome", "berlin", "madrid", "cairo",
    "delhi", "mumbai", "shanghai", "hong kong", "singapore", "dubai", "toronto", "sydney", "melbourne",
    "los angeles", "chicago", "houston", "phoenix", "philadelphia", "san antonio", "san diego", "dallas",
    "san jose", "austin", "jacksonville", "fort worth", "columbus", "san francisco", "charlotte", "indianapolis",
    "seattle", "denver", "washington", "boston", "el paso", "nashville", "detroit", "oklahoma city", "portland",
    "las vegas", "memphis", "louisville", "baltimore", "milwaukee", "albuquerque", "tucson", "fresno", "sacramento",
    "kansas city", "mesa", "atlanta", "omaha", "colorado springs", "raleigh", "miami", "virginia beach", "oakland",
    "minneapolis", "tulsa", "arlington", "tampa", "new orleans", "wichita", "cleveland", "bakersfield", "aurora",
    "anaheim", "honolulu", "santa ana", "riverside", "corpus christi", "lexington", "stockton", "henderson",
    "saint paul", "st. louis", "cincinnati", "pittsburgh", "greensboro", "anchorage", "plano", "lincoln", "orlando",
    "irvine", "newark", "toledo", "durham", "chula vista", "fort wayne", "jersey city", "st. petersburg", "laredo",
    "madison", "chandler", "buffalo", "lubbock", "scottsdale", "reno", "glendale", "gilbert", "winston-salem",
    "north las vegas", "norfolk", "chesapeake", "garland", "irving", "hialeah", "fremont", "boise", "richmond",
    "baton rouge", "spokane", "des moines", "tacoma", "san bernardino", "modesto", "fontana", "santa clarita",
    "birmingham", "oxnard", "fayetteville", "rochester", "moreno valley", "salt lake city", "amarillo", "tallahassee",
    "worcester", "grand rapids", "little rock", "augusta", "columbus", "akron", "shreveport", "montgomery", "mobile",
    "untsville", "knoxville", "chattanooga", "providence", "sioux falls", "overland park", "tempe", "peoria", "salem",
    "cape coral", "fort lauderdale", "vancouver", "calgary", "ottawa", "montreal", "quebec", "hamilton", "winnipeg",
    "edmonton", "halifax", "victoria", "regina", "saskatoon", "st. john's", "barcelona", "milan", "munich", "hamburg",
    "frankfurt", "vienna", "zurich", "geneva", "brussels", "amsterdam", "copenhagen", "stockholm", "oslo", "helsinki",
    "warsaw", "prague", "budapest", "bucharest", "athens", "istanbul", "jerusalem", "tel aviv", "tehran", "baghdad",
    "riyadh", "jeddah", "mecca", "medina", "karachi", "lahore", "islamabad", "dhaka", "kathmandu", "colombo", "bangkok",
    "jakarta", "kuala lumpur", "manila", "hanoi", "ho chi minh city", "taipei", "seoul", "pyongyang", "osaka", "kyoto"
}

religions = {
    "christianity", "islam", "judaism", "buddhism", "hinduism", "sikhism", "jainism", "shinto", "taoism",
    "christian", "muslim", "jew", "jewish", "buddhist", "hindu", "sikh", "jain", "bible", "quran", "koran",
    "torah", "talmud", "vedas", "upanishads", "bhagavad gita", "tripitaka", "god", "allah", "yahweh", "jehova",
    "jesus", "christ", "muhammad", "mohammed", "buddha", "krishna", "rama", "shiva", "vishnu", "brahma",
    "catholic", "protestant", "orthodox", "sunni", "shia", "sufi"
}

planets = {
    "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto",
    "sun", "moon", "milky way", "andromeda"
}

names = {
    "john", "mary", "james", "robert", "michael", "william", "david", "richard", "joseph", "thomas",
    "charles", "christopher", "daniel", "matthew", "anthony", "donald", "mark", "paul", "steven", "andrew",
    "kenneth", "joshua", "kevin", "brian", "george", "edward", "ronald", "timothy", "jason", "jeffrey",
    "ryan", "jacob", "gary", "nicholas", "eric", "jonathan", "stephen", "larry", "justin", "scott",
    "brandon", "benjamin", "samuel", "frank", "gregory", "raymond", "alexander", "patrick", "jack", "dennis",
    "jerry", "tyler", "aaron", "jose", "adam", "nathan", "henry", "douglas", "zachary", "peter",
    "kyle", "walter", "ethan", "jeremy", "harold", "keith", "christian", "roger", "noah", "gerald",
    "carl", "terry", "sean", "austin", "arthur", "lawrence", "jesse", "dylan", "bryan", "joe",
    "jordan", "billy", "bruce", "albert", "willie", "gabriel", "logan", "alan", "juan", "wayne",
    "roy", "ralph", "randy", "eugene", "vincent", "russell", "elijah", "louis", "bobby", "philip",
    "johnny", "elizabeth", "patricia", "jennifer", "linda", "barbara", "susan", "jessica", "sarah", "karen",
    "nancy", "lisa", "betty", "margaret", "sandra", "ashley", "kimberly", "emily", "donna", "michelle",
    "dorothy", "carol", "amanda", "melissa", "deborah", "stephanie", "rebecca", "sharon", "laura", "cynthia",
    "kathleen", "amy", "shirley", "angela", "helen", "anna", "brenda", "pamela", "nicole", "samantha",
    "katherine", "emma", "ruth", "christine", "maria", "debra", "rachel", "catherine", "carolyn", "janet",
    "virginia", "joyce", "diane", "alice", "julie", "heather", "teresa", "doris", "gloria", "evelyn",
    "jean", "cheryl", "mildred", "joan", "judith", "rose", "janice", "kelly",
    "lillian", "kathy", "theresa", "beverly", "denise", "tammy", "irene", "jane", "lori"
}

blacklist = {
    "may", "will", "bill", "mark", "rose", "amber", "frank", "jack", "pat", "bob", "dick", "harry",
    "sue", "tom", "jim", "joe", "dan", "ken", "ben", "don", "sam", "max", "rob", "tim", "phil",
    "ted", "ed", "al", "les", "len", "nat", "ray", "vic", "cal", "sal", "hal", "val", "mal",
    "mel", "sid", "sol", "gil", "gus", "kip", "ned", "zeb", "bud", "doc", "mac", "guy", "lad",
    "tot", "mam", "dad", "sis", "bro", "sun", "moon", "earth", "spring", "summer", "autumn", "winter"
}

# Combine all lists
proper_nouns = months | days | holidays | countries_regions | cities | religions | planets | names

def should_capitalize(word, pos):
    word_lower = word.lower()

    # Check POS
    if "proper noun" in pos.lower():
        return True

    # Check "I"
    if word_lower == "i" and "pronoun" in pos.lower():
        return True

    # Check manual list
    if word_lower in proper_nouns:
        if word_lower in blacklist:
            return False
        return True

    return False

def process_file(filepath):
    output_rows = []

    # First pass: read and process
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames

            for row in reader:
                word = row['Word']
                pos = row['POS']
                headword = row['Headword']

                # Normalize to lower first to ensure idempotency and correct re-processing
                word_lower = word.lower()
                headword_lower = headword.lower()

                # Check Word
                if should_capitalize(word_lower, pos):
                    new_word = word_lower.capitalize()
                    if "'" in new_word:
                        parts = new_word.split("'")
                        new_word = "'".join([p.capitalize() for p in parts])
                    row['Word'] = new_word
                else:
                    row['Word'] = word_lower # Revert to lowercase if not proper noun

                # Check Headword
                if should_capitalize(headword_lower, pos):
                    new_headword = headword_lower.capitalize()
                    if "'" in new_headword:
                        parts = new_headword.split("'")
                        new_headword = "'".join([p.capitalize() for p in parts])
                    row['Headword'] = new_headword
                else:
                    row['Headword'] = headword_lower # Revert to lowercase if not proper noun

                output_rows.append(row)

    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        sys.exit(1)

    # Write back
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Successfully processed {len(output_rows)} rows.")

if __name__ == "__main__":
    process_file("basewords_all_pos.csv")
