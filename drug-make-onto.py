from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, OWL
from urllib.parse import quote

# Initialize the RDF Graph
g = Graph()

# Define your namespaces
dw = Namespace("http://darkwebisspooky/")
g.bind("dw", dw)

# Define the Drug class (if not already defined)
drug_class = dw.Drug
g.add((drug_class, RDF.type, RDFS.Class))
g.add((drug_class, RDFS.label, Literal("Drug")))

# Function to add a drug and its slang terms to the graph, linking them as the same entity
def add_drug_with_slang(drug_name, slang_terms_str):
    # Create the primary drug entity
    drug_uri = dw[quote(drug_name.replace(" ", "_"))]
    g.add((drug_uri, RDF.type, drug_class))
    g.add((drug_uri, RDFS.label, Literal(drug_name)))

    # Add slang terms for the drug and link them as owl:sameAs the primary drug entity
    slang_terms_list = slang_terms_str.split("; ")
    for term in slang_terms_list:
        term = term.strip()  # Remove leading and trailing whitespace
        term_uri = dw[quote(term.replace(" ", "_"))]  # Create a valid URI for the term
        g.add((term_uri, RDF.type, OWL.NamedIndividual))
        g.add((term_uri, RDFS.label, Literal(term)))
        g.add((term_uri, OWL.sameAs, drug_uri))  # Indicate the slang term is the same as the drug



# Example usage: Add "Marijuana" and its slang terms
marijuana_slang_terms = """420; Acapulco Gold; Acapulco Red; Ace; African Black; African Bush; Airplane; Alfombra; Alice B Toklas; AllStar; Angola; Animal Cookies (hydroponic); Arizona; Ashes; Aunt Mary; Baby; Bale; Bambalachacha; Barbara
Jean; Bareta; Bash; BC Budd; Bernie; Bhang; Big Pillows; Biggy; Black Bart; Black Gold; Black Maria; Blondie;
Blue Cheese; Blue Crush; Blue Jeans; Blue Sage; Blueberry; Bobo Bush; Boo; Boom; Broccoli; Bud; Budda;
Burritos Verdes; Bush; Cabbage; Cali; Canadian Black; Catnip; Cheeba; Chernobyl; Cheese; Chicago Black;
Chicago Green; Chippie; Chistosa; Christmas Tree; Chronic; Churo; Cigars; Citrol; Cola; Colorado Cocktail;
Cookie (hydroponic); Cotorritos; Crazy Weed; Creeper Bud; Crippy; Crying Weed; Culican; Dank; Dew; Diesel;
Dimba; Dinkie Dow; Dirt Grass; Ditch Weed; Dizz; Djamba; Dody; Dojo; Domestic; Donna Juana; Doobie;
Downtown Brown; Drag Weed; Dro (hydroponic); Droski (hydroponic); Dry High; Endo; Fine Stuff; Fire;
Flower; Flower Tops; Fluffy; Fuzzy Lady; Gallito; Garden; Gauge; Gangster; Ganja; Gash; Gato; Ghana; Gigi
(hydroponic) Giggle Smoke; Giggle Weed; Girl Scout Cookies (hydroponic); Gloria; Gold; Gold Leaf; Gold Star;
Gong; Good Giggles; Gorilla; Gorilla Glue; Grand Daddy Purp; Grass; Grasshopper; Green; Green-Eyed Girl;
Green Eyes; Green Goblin; Green Goddess; Green Mercedes Benz; Green Paint; Green Skunk; Grenuda;
Greta; Guardada; Gummy Bears; Gunga; Hairy Ones; Hash; Hawaiian; Hay; Hemp; Herb; Hierba; Holy
Grail; Homegrown; Hooch; Humo; Hydro; Indian Boy; Indian Hay; Jamaican Gold; Jamaican Red; Jane; Jive;
Jolly Green; Jon-Jem; Joy Smoke; Juan Valdez; Juanita; Jungle Juice; Kaff; Kali; Kaya; KB; Kentucky Blue;
KGB; Khalifa; Kiff; Killa; Kilter; King Louie; Kona Gold; Kumba; Kush; Laughing Grass; Laughing Weed; Leaf;
Lechuga; Lemon-Lime; Liamba; Lime Pillows; Little Green Friends; Little Smoke; Loaf; Lobo; Loco Weed; Love
Nuggets; Love Weed; M.J.; Machinery; Macoña; Mafafa; Magic Smoke; Manhattan Silver; Maracachafa; Maria;
Marimba; Mariquita; Mary Ann; Mary Jane; Mary Jones; Mary Warner; Mary Weaver; Matchbox; Matraca; Maui
Wowie; Meg; Method; Mexican Brown; Mexican Green; Mexican Red; Mochie (hydroponic); Moña; Monte;
Moocah; Mootie; Mora; Morisqueta; Mostaza; Mota; Mother; Mowing the Lawn; Muggie; Narizona; Northern
Lights; O-Boy; O.J.; Owl; Paja; Panama Cut; Panama Gold; Panama Red; Pakalolo; Palm; Paloma; Parsley;
Pelosa; Phoenix; Pillow; Pine; Platinum Cookies (hydroponic); Platinum Jack; Pocket Rocket; Popcorn; Pot;
Pretendo; Puff; Purple Haze; Queen Ann’s Lace; Ragweed; Railroad Weed; Rainy Day Woman; Rasta Weed;
Red Cross; Red Dirt; Reefer; Reggie; Repollo; Righteous Bush; Root; Rope; Rosa Maria; Salt & Pepper;
Santa Marta; Sasafras; Sativa; Sinsemilla; Shmagma; Shora; Shrimp; Shwag; Skunk; Skywalker (hydroponic);
Smoke; Smoochy Woochy Poochy; Smoke; Smoke Canada; Spliff; Stems; Stink Weed; Sugar Weed; Sweet
Lucy; Tahoe (hydroponic); Tex-Mex; Texas Tea; Tila; Tims; Tosca; Trees; Tweeds; Wacky Tobacky; Wake and
Bake; Weed; Weed Tea; Wet (mixed with PCP); Wheat; White-Haired Lady; Wooz; Yellow Submarine; Yen
Pop; Yerba; Yesca; Young Girls; Zacate; Zacatecas; Zambi; Zoom (mixed with PCP)."""
add_drug_with_slang("Marijuana", marijuana_slang_terms)

# Example usage: Add "Acid" and its slang terms
lsd_slang_terms = """Aceite; Acid; Acido; Alice; Angels in a Sky; Animal; Backbreaker (mixed with strychnine); Barrel; Bart Simpson;
Battery Acid; Beast; Big D; Black Acid (mixed with PCP); Black Star; Black Sunshine; Black Tabs; Blotter
Acid; Blotter Cube; Blue Acid; Blue Barrel; Blue Chair; Blue Cheer; Blue Heaven; Blue Microdots; Blue Mist;
Blue Moon; Blue Sky; Blue Star; Blue Tabs; Brown Bomber; Brown Dots; California Sunshine; Cherry Dome;
Chief; Chinese Dragons; Coffee; Conductor; Contact Lens; Crackers; Crystal Tea; Cupcakes; Dental Floss;
Dinosaurs; Domes; Dots; Double Dome; El Cid; Electric Kool Aid; Ellis Day; Fields; Flash; Flat Blues; Ghost;
Golden Dragon; Golf Balls; Goofy; Gota; Grape Parfait; Green Wedge; Grey Shields; Hats; Hawaiian Sunshine;
Hawk; Haze; Headlights; Heavenly Blue; Hits; Instant Zen; Jesus Christ Acid; Kaleidoscope; Leary; Lens;
Lime Acid; Live, Spit & Die; Lucy in the Sky with Diamonds; Mellow Yellow; Mica; Microdot; Mighty Quinn;
Mind Detergent; Mother of God; Newspapers; Orange Barrels; Orange Cubes; Orange Haze; Orange Micros;
Orange Wedges; Owsley; Paper Acid; Pearly Gates; Pellets; Phoenix; Pink Blotters; Pink Panthers; Pink
Robots; Pink Wedges; Pink Witches; Pizza; Potato; Pure Love; Purple Barrels; Purple Haze; Purple Hearts;
Purple Flats; Recycle; Royal Blues; Russian Sickles; Sacrament; Sandoz; Smears; Square Dancing Tickets;
Strawberry Fields; Sugar Cubes; Sugar Lumps; Sunshine; Tabs; Tacatosa; Tail Lights; Teddy Bears; Ticket;
Uncle Sid; Valley Dolls; Vodka Acid; Wedding Bells; Wedge; White Dust; White Fluff; White Lightening; White
Owsley; Window Glass; Window Pane; Yellow Dimples; Yellow Sunshine; Zen."""
add_drug_with_slang("LSD", lsd_slang_terms)

# # Example usage: Add "Heroin" and its slang terms
heroin_slang_terms = """A-Bomb (mixed with marijuana); Achivia; Adormidera; Antifreeze; Aunt Hazel; Avocado; Azucar; Bad Seed;
Ballot; Basketball; Basura; Beast; Beyonce; Big Bag; Big H; Big Harry; Bird; Birdie Powder; Black; Black
Bitch; Black Goat; Black Olives; Black Paint; Black Pearl; Black Sheep; Black Tar; Blanco; Blue; Blow Dope;
Blue Hero; Bombita (mixed with cocaine); Bombs Away; Bonita; Boy; Bozo; Brea Negra; Brick Gum; Brown;
Brown Crystal; Brown Rhine; Brown Sugar; Bubble Gum; Burrito; Caballo; Caballo Negro; Caca; Café; Capital
H; Carga; Caro; Cement; Chapopote; Charlie; Charlie Horse; Cheese; Chicle; Chiclosa; China; China Cat;
China White; Chinese Food; Chinese Red; Chip; Chiva; Chiva Blanca; Chivones; Chocolate; Chocolate Balls;
Choko; Chorizo; Chutazo; Coco; Coffee; Comida; Crown Crap; Curley Hair; Dark; Dark Girl; Dead on Arrival
(DOA); Diesel; Diesel; Dirt; Dog Food; Doggie; Doojee; Dope; Dorado; Down; Downtown; Dreck; Dynamite;
Dyno; El Diablo; Engines; Fairy Dust; Flea Powder; Foolish Powder; Galloping Horse; Gamot; Gato; George; 
Girl; Golden Girl; Good & Plenty; Good H; Goma; Gorda; Gras; Grasin; Gravy; Gum; H; H-Caps; Hairy;
Hard Candy; Harry; Hats; Hazel; Heaven Dust; Heavy; Helen; Helicopter; Hell Dust; Henry; Hercules; Hero;
Him; Hombre; Horse; Hot Dope; Hummers; Jojee; Joy Flakes; Joy Powder; Junk; Kabayo; Karachi; Karate;
King’s Tickets; Lemonade; Lenta; Lifesaver; Manteca; Marias; Mayo; Mazpan; Meal; Menthol; Mexican Brown;
Mexican Horse; Mexican Mud; Mexican Treat; Modelo Negra; Mojo; Mole; Mongega; Morena; Morenita; Mortal
Combat; Motors; Mud; Mujer; Muzzle; Nanoo; Negra; Negra Tomasa; Negrita; Nice and Easy; Night; Noise;
Obama; Old Steve; Pants; Patty; Peg; P-Funk; Piezas; Plata; Poison; Polvo; Poppy; Powder; Prostituta Negra;
Puppy; Pure; Rambo; Red Chicken; Red Eagle; Reindeer Dust; Roofing Tar; Sack; Salt; Sand; Scag; Scat;
Schmeck; Sheep; Shirts; Shoes; Skag; Slime; Smack; Smeck; Snickers; Speedball (mixed with cocaine);
Spider Blue; Sticky Kind; Stufa; Sugar; Sweet Jesus; Tan; Tar; Tecata; Tires; Tootsie Roll; Tragic Magic; Trees;
Turtle; Vidrio; Whiskey; White; White Boy; White Girl; White Junk; White Lady; White Nurse; White Shirt; White
Stuff; Wings; Witch; Witch Hazel; Zapapote"""
add_drug_with_slang("Heroin", heroin_slang_terms)

ketamine_slang_terms = """Blind Squid; Cat Valium; Green; Honey Oil; Jet; K; Keller; Kelly’s Day; K-Hold; K-Ways; Special K; Super Acid;
Vitamin K"""
add_drug_with_slang("Heroin", ketamine_slang_terms)

mdma_slang_terms = """Adam; Baby Slits; Bean; Blue Kisses; Booty Juice (dissolved in liquid); Candy; Chocolate Chips; Clarity;
Dancing Shoes; Decadence; Doctor; Domex (mixed with PCP); E; E-Bomb; Ecstasy; Essence; Eve; Kleenex;
Love Doctor; Love Drug; Love Potion #9; Love Trip (mixed with mescaline); Molly; Moon Rock; Roll; Rolling;
Running; Scooby Snacks; Skittle; Slits; Smartees; Speed for Lovers; Sweets; Vitamin E; X; XTC"""
add_drug_with_slang("MDMA", ketamine_slang_terms)


meth_slang_terms = """Accordion; Aqua; Batu; Blue; Blue Bell Ice Cream; Beers; Bottles; Bud Light; Bump; Cajitas; Chalk;
Chavalones; Chicken; Chicken Powder; Christine; Christy; Clear; Clothing Cleaner; Colorado Rockies; Crank;
Cream; Cri-Cri; Crink; Crisco; Crypto; Crystal; Cuadros; Day; El Gata Diablo; Evil Sister; Eye Glasses; Fire;
Fizz; Flowers; Food; Frio; G-Funk; Gifts; Girls; Glass; Go-Fast; Groceries; Hard Ones; Hare; Hawaiian Salt;
Hielo; Hot Ice; Ice; Ice Cream; Jug of Water; L.A. Glass; L.A. Ice; Lemons; Lemon Drop; Light; Light Beige;
Livianas; Madera; Meth; Mexican Crack; Mexican Crank; Miss Girl; Montura; Motor; Muchacha; Nails; One Pot;
Pantalones; Peanut Butter Crank; Piñata; Pointy Ones; Pollito; Popsicle; Purple; Raspado; Rims; Salt; Shabu;
Shards; Shatter; Shaved Ice; Shiny Girl; Soap Dope; Soft Ones; Spicy Kind; Stove Top; Stuff; Super Ice; Table;
Tina; Truck; Tupperware; Ventanas; Vidrio; Walking Zombie; Water; White; Windows; Witches Teeth; Yellow
Barn; Yellow Kind; Zip"""
add_drug_with_slang("Methamphetamine", meth_slang_terms)

synthetic_cannabis_slang_terms = """4-20; Abyss; Ace of Spades; AK-47; Amnesia; Atomic Blast; Big Bang; Blaze; Black Magic Smoke; Black
Mamba; Blaze; Blue Cheese; Brain Freeze; Buzz Haze; Cherry Bomb; Chill; Chrome; Clockwork Orange;
Cloud 10; Cowboy Kush; Crystal Skull; Dead Man; Devil’s Venom; Dr. Feel Good; Dragon Eye; Earth Blend;
Exodus; Extreme; Fake Bake; Fruit Candy Flavors; Funky Buddha; Funky Monkey; G-Force; GI Joe; Green
Dream; Green Peace; Hammer Head; Helix; Hipster; Hysteria; Ice Dragon; Juicy Leaf; Jungle Juice; Just
Chill; K2; Kaos; Karma; Kong; Krazy Kandy; Kryp2nite; Kush; Layer Cake; Limitless; Mad Hatter; Mile High;
Mystique; Ninja; Odyssey; OMG; Pandora’s Box; Phoenix; Pineapple Express; Posh; Potpourri; Pow; Rapture;
Red Magic; Rewind; Scooby Snax; Sexy; Sky High; Snake Bite; Spice; Spike Diamond; Storm; Sweet Leaf;
Synthetic Marijuana; Time Traveler; Top Gear; Train Wreck; Ultimate; Viper; Voodoo Child; Wazabi; Wicked;
Wizard; Xtreme; Zero Gravity; Zombie"""
add_drug_with_slang("Synthetic Cannabinoids", meth_slang_terms)

# ... Add more drugs and their slang terms as needed ...

# Serialize the graph
g.serialize(destination='DrugOntology.ttl', format='turtle')