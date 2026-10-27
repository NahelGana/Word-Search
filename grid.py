import json
import random
import string
import unicodedata

# ---------------------------------------------------------------
# THÈMES : les 3 d'origine + les 109 nouveaux (112 thèmes = 224 grilles)
# Les mots sont écrits sans accents, en majuscules, sans espaces.
# ---------------------------------------------------------------
THEMES = {
    "Animaux": ["CHIEN", "CHAT", "ELEPHANT", "SINGE", "LION", "TIGRE", "LAPIN", "OISEAU", "CHEVAL", "LOUP", "GAZELLE", "OURS", "GIRAFE", "DAUPHIN", "PINGOUIN", "ZEBRE", "REQUIN", "AIGLE", "PANDA", "KOALA", "PANTHERE", "CORBEAU", "LAMA", "RENARD"],
    "Voyages": ["AVION", "VALISE", "PASSEPORT", "PLAGE", "NAVIRE", "BAGAGE", "CAMPING", "SAFARI", "VOYAGEUR", "GARE", "HOTEL", "ESCALE", "BATEAU", "ILE", "CARTE", "GUIDE", "SOLEIL", "CROISIERE", "VOLCAN", "DESERT", "MONTAGNE"],
    "Histoire": ["ROI", "REINE", "CHATEAU", "EMPIRE", "GUERRE", "TRAITE", "EPOQUE", "SIECLE", "ARMEE", "BLASON", "CHEVALIER", "MUSEE", "ARCHIVE", "PYRAMIDE", "PHARAON", "ROMAN", "GLADIATEUR", "NAPOLEON", "REVOLUTION"],
    "Cuisine": ["CASSEROLE", "POELE", "MARMITE", "LOUCHE", "FOUR", "RECETTE", "CUISSON", "MIJOTER", "GRILLER", "FRIRE", "BOUILLIR", "ROTIR", "SAUCE", "BOUILLON", "FOUET", "COUTEAU", "PLANCHE", "TABLIER", "PASSOIRE", "CHEF", "MARINADE"],
    "Fruits": ["POMME", "POIRE", "BANANE", "ORANGE", "CITRON", "FRAISE", "CERISE", "PECHE", "ABRICOT", "PRUNE", "RAISIN", "MELON", "PASTEQUE", "ANANAS", "MANGUE", "KIWI", "FRAMBOISE", "MYRTILLE", "FIGUE", "GRENADE", "LITCHI"],
    "Légumes": ["CAROTTE", "POIREAU", "TOMATE", "COURGETTE", "AUBERGINE", "POIVRON", "CHOU", "RADIS", "NAVET", "OIGNON", "AIL", "EPINARD", "SALADE", "CONCOMBRE", "BROCOLI", "CELERI", "BETTERAVE", "ASPERGE", "ARTICHAUT", "POIS", "FENOUIL"],
    "Fromages": ["CAMEMBERT", "BRIE", "ROQUEFORT", "COMTE", "CHEVRE", "EMMENTAL", "MUNSTER", "REBLOCHON", "CANTAL", "MIMOLETTE", "GRUYERE", "PARMESAN", "MOZZARELLA", "FETA", "RACLETTE", "MORBIER", "BLEU", "MAROILLES", "BEAUFORT", "TOMME"],
    "Desserts": ["TIRAMISU", "MOUSSE", "FLAN", "CREME", "GLACE", "SORBET", "COMPOTE", "CLAFOUTIS", "CREPE", "GAUFRE", "BEIGNET", "FONDANT", "CARAMEL", "CHANTILLY", "MERINGUE", "PUDDING", "CHARLOTTE", "TARTE", "YAOURT"],
    "Pâtisseries": ["ECLAIR", "MACARON", "CROISSANT", "BRIOCHE", "TARTELETTE", "CHOUX", "FINANCIER", "MADELEINE", "CANELE", "SABLE", "PALMIER", "RELIGIEUSE", "SAVARIN", "GALETTE", "FRAISIER", "OPERA", "BABA", "CHAUSSON", "BUCHE"],
    "Boissons": ["EAU", "JUS", "CAFE", "THE", "LAIT", "VIN", "BIERE", "CIDRE", "SODA", "LIMONADE", "SIROP", "TISANE", "CHOCOLAT", "CHAMPAGNE", "COCKTAIL", "WHISKY", "RHUM", "VODKA", "INFUSION", "SMOOTHIE", "NECTAR"],
    "Épices": ["POIVRE", "CANNELLE", "CURRY", "PAPRIKA", "CUMIN", "SAFRAN", "GINGEMBRE", "CLOU", "MUSCADE", "CURCUMA", "ANIS", "VANILLE", "PIMENT", "CARDAMOME", "FENUGREC", "CORIANDRE", "SESAME", "SUMAC", "CARVI", "BADIANE"],
    "Céréales": ["BLE", "RIZ", "MAIS", "AVOINE", "ORGE", "SEIGLE", "MILLET", "SORGHO", "EPEAUTRE", "QUINOA", "SARRASIN", "FARINE", "SEMOULE", "BOULGOUR", "MUESLI", "GRAIN", "EPI", "MOISSON", "FLOCONS", "GRUAU", "CHAPELURE"],
    "Légumineuses": ["LENTILLE", "HARICOT", "POIS", "SOJA", "FEVE", "LUPIN", "ARACHIDE", "CACAHUETE", "ALFALFA", "GOUSSE", "POISCHICHE", "FLAGEOLET", "MOGETTE", "NIEBE", "ADZUKI", "TREFLE", "LUZERNE", "CAROUBE", "REGLISSE", "TAMARIN"],
    "Fleurs": ["ROSE", "TULIPE", "LILAS", "MUGUET", "PIVOINE", "ORCHIDEE", "IRIS", "LYS", "JASMIN", "VIOLETTE", "PENSEE", "COQUELICOT", "MARGUERITE", "TOURNESOL", "DAHLIA", "OEILLET", "JONQUILLE", "GLYCINE", "HORTENSIA", "PETUNIA"],
    "Arbres": ["CHENE", "HETRE", "BOULEAU", "SAPIN", "PIN", "CEDRE", "ERABLE", "TILLEUL", "PEUPLIER", "SAULE", "FRENE", "OLIVIER", "PALMIER", "NOYER", "MELEZE", "CYPRES", "PLATANE", "ORME", "ACACIA", "SEQUOIA"],
    "Plantes": ["FOUGERE", "LIERRE", "MOUSSE", "CACTUS", "BAMBOU", "ALOES", "BASILIC", "MENTHE", "THYM", "ROMARIN", "PERSIL", "CIBOULETTE", "LAURIER", "LAVANDE", "ORTIE", "FEUILLE", "TIGE", "RACINE", "BOURGEON", "GRAINE"],
    "Jardins": ["POTAGER", "PELOUSE", "ALLEE", "BASSIN", "TERRASSE", "PERGOLA", "TONNELLE", "CLOTURE", "HAIE", "MASSIF", "PARTERRE", "SERRE", "FONTAINE", "STATUE", "BANC", "GAZON", "VERGER", "ROSERAIE", "ROCAILLE", "SENTIER"],
    "Forêts": ["CLAIRIERE", "SENTIER", "FOUGERE", "CHAMPIGNON", "GIBIER", "BUCHERON", "FEUILLAGE", "MOUSSE", "RESINE", "BRANCHE", "ECUREUIL", "CERF", "SANGLIER", "HIBOU", "TRONC", "SOUCHE", "CANOPEE", "TAILLIS", "FUTAIE"],
    "Montagnes": ["SOMMET", "GLACIER", "ALPES", "PYRENEES", "COL", "VALLEE", "PIC", "CRETE", "ALTITUDE", "SKI", "RANDONNEE", "REFUGE", "VERSANT", "FALAISE", "CASCADE", "ALPINISTE", "EVEREST", "MASSIF", "ROCHER", "NEIGE", "AVALANCHE"],
    "Océans": ["ATLANTIQUE", "PACIFIQUE", "INDIEN", "ARCTIQUE", "VAGUE", "MAREE", "CORAIL", "ABYSSE", "FOSSE", "COURANT", "BALEINE", "ECUME", "RECIF", "TEMPETE", "HORIZON", "SALE", "PLANCTON", "DAUPHIN", "RIVAGE", "HOULE", "ILOT"],
    "Rivières": ["SEINE", "LOIRE", "RHONE", "GARONNE", "MEUSE", "MARNE", "OISE", "DORDOGNE", "SOURCE", "AFFLUENT", "MEANDRE", "GUE", "PONT", "BERGE", "CRUE", "COURS", "EMBOUCHURE", "CASCADE", "TORRENT", "RUISSEAU", "LIT"],
    "Lacs": ["LEMAN", "ANNECY", "BOURGET", "GARDE", "TITICACA", "BAIKAL", "VICTORIA", "TCHAD", "LOCH", "ONTARIO", "ERIE", "HURON", "ETANG", "MARE", "RIVE", "NENUPHAR", "CYGNE", "PONTON", "BARQUE", "REFLET", "LAGUNE"],
    "Déserts": ["SAHARA", "GOBI", "KALAHARI", "ATACAMA", "SABLE", "DUNE", "OASIS", "CHAMEAU", "CACTUS", "MIRAGE", "DROMADAIRE", "NOMADE", "TOUAREG", "SCORPION", "ARIDE", "SECHERESSE", "CARAVANE", "CANYON", "ROCHE", "SOIF"],
    "Volcans": ["ETNA", "VESUVE", "ERUPTION", "LAVE", "CRATERE", "MAGMA", "CENDRE", "FUMEE", "CHEMINEE", "CALDEIRA", "PONCE", "BASALTE", "GEYSER", "SEISME", "FUMEROLLE", "STROMBOLI", "FUJI", "PELEE", "VOLCANIQUE", "FOSSE"],
    "Météo": ["PLUIE", "VENT", "NUAGE", "ORAGE", "BROUILLARD", "NEIGE", "GRELE", "ECLAIR", "TONNERRE", "SOLEIL", "BRUME", "GIVRE", "RAFALE", "VERGLAS", "BAROMETRE", "HUMIDITE", "ECLAIRCIE", "AVERSE", "TEMPETE", "CIEL"],
    "Climat": ["TROPICAL", "POLAIRE", "TEMPERE", "ARIDE", "OCEANIQUE", "EQUATORIAL", "MOUSSON", "CHALEUR", "FROID", "SECHERESSE", "HUMIDE", "ZONE", "LATITUDE", "BIOME", "GLACE", "CARBONE", "EMISSION", "OZONE", "SERRE", "MONTAGNARD"],
    "Saisons": ["PRINTEMPS", "ETE", "AUTOMNE", "HIVER", "SOLSTICE", "EQUINOXE", "VENDANGES", "MOISSON", "FLORAISON", "FEUILLES", "NEIGE", "CANICULE", "FRIMAS", "BOURGEON", "RECOLTE", "VACANCES", "SOLEIL", "GELEE", "BRUINE", "SEMIS"],
    "Couleurs": ["ROUGE", "BLEU", "VERT", "JAUNE", "ORANGE", "VIOLET", "ROSE", "NOIR", "BLANC", "GRIS", "MARRON", "BEIGE", "TURQUOISE", "INDIGO", "ECARLATE", "CARMIN", "OCRE", "AZUR", "EMERAUDE", "LILAS", "SAUMON"],
    "Formes": ["CERCLE", "CARRE", "TRIANGLE", "LOSANGE", "OVALE", "RECTANGLE", "ETOILE", "CROIX", "SPIRALE", "CUBE", "SPHERE", "CONE", "CYLINDRE", "PYRAMIDE", "ARC", "HEXAGONE", "OCTOGONE", "PENTAGONE", "CROISSANT", "COEUR"],
    "Matières": ["BOIS", "PLASTIQUE", "VERRE", "PAPIER", "CARTON", "CUIR", "LAINE", "COTON", "SOIE", "LIN", "CAOUTCHOUC", "CERAMIQUE", "BETON", "ACIER", "MARBRE", "ARGILE", "PLATRE", "BRIQUE", "FER", "RESINE"],
    "Métaux": ["OR", "ARGENT", "CUIVRE", "FER", "ZINC", "ETAIN", "PLOMB", "NICKEL", "TITANE", "ALUMINIUM", "CHROME", "MERCURE", "PLATINE", "COBALT", "BRONZE", "LAITON", "ACIER", "FONTE", "MAGNESIUM", "TUNGSTENE"],
    "Minéraux": ["QUARTZ", "MICA", "CALCITE", "GYPSE", "TALC", "FELDSPATH", "PYRITE", "FLUORINE", "GALENE", "HEMATITE", "BAUXITE", "SOUFRE", "GRAPHITE", "HALITE", "CORINDON", "OPALE", "JADE", "AGATE", "ONYX", "TOPAZE"],
    "Pierres": ["GRANIT", "MARBRE", "SILEX", "GALET", "ARDOISE", "CALCAIRE", "GRES", "BASALTE", "PIERRE", "ROCHE", "CAILLOU", "MENHIR", "DOLMEN", "MOELLON", "PAVE", "TUFFEAU", "LAVE", "SCHISTE", "MEULE", "CARRIERE"],
    "Bijoux": ["BAGUE", "COLLIER", "BRACELET", "BROCHE", "PENDENTIF", "DIAMANT", "PERLE", "RUBIS", "SAPHIR", "EMERAUDE", "ALLIANCE", "CREOLE", "MEDAILLON", "PARURE", "CAMEE", "DIADEME", "CHAINE", "GOURMETTE", "SOLITAIRE", "BOUCLES"],
    "Vêtements": ["PANTALON", "ROBE", "JUPE", "CHEMISE", "VESTE", "MANTEAU", "PULL", "GILET", "JEAN", "SHORT", "COSTUME", "CRAVATE", "ECHARPE", "CHAUSSETTE", "MAILLOT", "BLOUSON", "ANORAK", "PYJAMA", "TUNIQUE", "CAPE"],
    "Chaussures": ["BOTTE", "BASKET", "SANDALE", "MOCASSIN", "ESCARPIN", "BALLERINE", "TONG", "SABOT", "PANTOUFLE", "MULE", "DERBY", "SOULIER", "SEMELLE", "TALON", "LACET", "CHAUSSON", "TENNIS", "BOTTINE", "RANGER", "CLAQUETTE"],
    "Accessoires": ["SAC", "CEINTURE", "CHAPEAU", "BONNET", "GANT", "ECHARPE", "LUNETTES", "MONTRE", "PARAPLUIE", "FOULARD", "BERET", "CASQUETTE", "BRETELLES", "NOEUD", "CRAVATE", "MITAINE", "BANDEAU", "SACOCHE", "BIJOU", "EVENTAIL"],
    "Coiffures": ["CHIGNON", "TRESSE", "NATTE", "FRANGE", "CARRE", "DEGRADE", "MECHE", "BOUCLE", "PERMANENTE", "BRUSHING", "COUPE", "COULEUR", "SHAMPOING", "PEIGNE", "BROSSE", "CISEAUX", "RASOIR", "TONDEUSE", "LAQUE", "GEL", "COIFFEUR"],
    "Maquillage": ["ROUGE", "FARD", "MASCARA", "EYELINER", "CRAYON", "POUDRE", "VERNIS", "BLUSH", "GLOSS", "PINCEAU", "ECLAT", "PAILLETTE", "BASE", "CONCEALER", "CILS", "PAUPIERE", "LEVRES", "TEINT", "RIMMEL", "FIXATEUR"],
    "Parfums": ["EAU", "ESSENCE", "FLACON", "SENTEUR", "AROME", "MUSC", "AMBRE", "VANILLE", "JASMIN", "VIOLETTE", "BERGAMOTE", "CITRON", "SANTAL", "ENCENS", "FRAGRANCE", "BOUQUET", "NOTE", "SILLAGE", "ATOMISEUR", "PATCHOULI", "LAVANDE"],
    "Tissus": ["SOIE", "COTON", "LIN", "LAINE", "VELOURS", "SATIN", "DENTELLE", "TWEED", "JEAN", "DRAP", "FLANELLE", "TULLE", "TAFFETAS", "FEUTRE", "NYLON", "POLYESTER", "VISCOSE", "LYCRA", "MOUSSELINE", "CACHEMIRE", "DAMAS"],
    "Couture": ["AIGUILLE", "FIL", "DEDALE", "PATRON", "COUTURIERE", "MACHINE", "BOUTON", "FERMETURE", "OURLET", "BRODERIE", "POINT", "SURJET", "CISEAUX", "EPINGLE", "RUBAN", "MESURE", "COUPE", "TISSU", "ESSAYAGE", "RETOUCHE"],
    "Mobilier": ["TABLE", "CHAISE", "CANAPE", "FAUTEUIL", "ARMOIRE", "COMMODE", "BUFFET", "ETAGERE", "LIT", "BUREAU", "TABOURET", "BANC", "CONSOLE", "VITRINE", "PUPITRE", "SOMMIER", "GUERIDON", "COFFRE", "SECRETAIRE", "BAHUT"],
    "Décoration": ["TABLEAU", "CADRE", "MIROIR", "VASE", "BOUGIE", "COUSSIN", "RIDEAU", "TAPIS", "LAMPE", "POSTER", "TENTURE", "STATUETTE", "HORLOGE", "GUIRLANDE", "PLAID", "BIBELOT", "DECOR", "OBJET", "STYLE", "FRESQUE", "CHEMINEE"],
    "Vaisselle": ["ASSIETTE", "TASSE", "BOL", "VERRE", "COUPE", "PLAT", "SAUCIERE", "THEIERE", "CARAFE", "SOUPIERE", "RAMEQUIN", "FOURCHETTE", "COUTEAU", "CUILLERE", "SOUCOUPE", "BEURRIER", "SALIERE", "PLATEAU", "PORCELAINE", "FAIENCE"],
    "Ustensiles": ["LOUCHE", "SPATULE", "FOUET", "PASSOIRE", "RAPE", "ECUMOIRE", "EPLUCHEUR", "ENTONNOIR", "CISEAUX", "MORTIER", "PILON", "RAMEQUIN", "CHINOIS", "MOULE", "ROULEAU", "PINCE", "MINUTEUR", "COUTEAU", "BALANCE", "TAMIS"],
    "Électroménager": ["FRIGO", "FOUR", "MIXEUR", "BLENDER", "ASPIRATEUR", "TOASTER", "BOUILLOIRE", "CAFETIERE", "HOTTE", "RADIATEUR", "FER", "ROBOT", "FRITEUSE", "CUISINIERE", "PLAQUE", "LAVOIR", "SECHOIR", "HACHOIR"],
    "Nettoyage": ["BALAI", "SERPILLERE", "EPONGE", "SAVON", "LESSIVE", "ASPIRATEUR", "DETERGEN", "TBROSSE", "SEAU", "CHIFFON", "LAVAGE", "RINCER", "FROTTER", "ESSUYER", "JAVEL", "VINAIGRE", "POUSSIERE", "TORCHON", "DEGRAISSER", "BALAYER", "LUSTRER"],
    "Bricolage": ["MARTEAU", "CLOU", "VIS", "TOURNEVIS", "PERCEUSE", "SCIE", "PINCE", "COLLE", "PONCER", "VISSER", "CLE", "NIVEAU", "METRE", "MECHE", "ETABLI", "RABOT", "CHEVILLE", "EQUERRE", "LIME", "VERNIS"],
    "Jardinage": ["BECHE", "RATEAU", "SERFOUETTE", "ARROSOIR", "SECATEUR", "TONDEUSE", "SEMER", "PLANTER", "ARROSER", "BINER", "TAILLER", "COMPOST", "ENGRAIS", "TERREAU", "POT", "PLANTOIR", "SARCLER", "GREFFE", "BOUTURE", "PAILLIS"],
    "Outillage": ["MARTEAU", "TOURNEVIS", "CLEF", "PINCE", "SCIE", "TENAILLE", "LIME", "RABOT", "BURIN", "CISEAU", "MAILLET", "ETAU", "PERCEUSE", "PONCEUSE", "TRUELLE", "NIVEAU", "EQUERRE", "MASSE", "ENCLUME", "VISSEUSE"],
    "Peinture": ["PINCEAU", "ROULEAU", "TOILE", "CHEVALET", "PALETTE", "HUILE", "AQUARELLE", "GOUACHE", "FUSAIN", "PASTEL", "FRESQUE", "PORTRAIT", "PAYSAGE", "LAQUE", "ENDUIT", "PEINTRE", "VERNIS", "COULEUR", "TEINTE", "ESQUISSE"],
    "Architecture": ["ARCHE", "VOUTE", "COLONNE", "FACADE", "DOME", "FLECHE", "BASILIQUE", "CATHEDRALE", "GOTHIQUE", "ROMAN", "BAROQUE", "PILIER", "ARCADE", "PLAN", "CHARPENTE", "FONDATION", "TOIT", "ARCHITECTE", "PORTIQUE", "PAVILLON", "LUCARNE"],
    "Bâtiments": ["ECOLE", "MAIRIE", "EGLISE", "GARE", "HOPITAL", "USINE", "MUSEE", "THEATRE", "GYMNASE", "CASERNE", "PRISON", "BANQUE", "POSTE", "STADE", "HANGAR", "ENTREPOT", "TOUR", "PHARE", "MOULIN", "PALAIS"],
    "Maisons": ["VILLA", "CHALET", "CHAUMIERE", "MANOIR", "CABANE", "BUNGALOW", "PAVILLON", "FERME", "MAS", "LOFT", "STUDIO", "DUPLEX", "IGLOO", "CHATEAU", "ROULOTTE", "COTTAGE", "MAISON", "MANSARDE", "GITE"],
    "Pièces": ["SALON", "CUISINE", "CHAMBRE", "BUREAU", "GARAGE", "CAVE", "GRENIER", "COULOIR", "ENTREE", "SEJOUR", "TOILETTES", "BUANDERIE", "VERANDA", "DRESSING", "CELLIER", "PALIER", "MEZZANINE", "ATELIER", "TERRASSE", "BALCON"],
    "Immobilier": ["LOYER", "BAIL", "AGENCE", "VENTE", "ACHAT", "NOTAIRE", "HYPOTHEQUE", "CREDIT", "SURFACE", "TERRAIN", "LOCATION", "PROPRIETE", "BAILLEUR", "LOCATAIRE", "CAUTION", "CADASTRE", "VISITE", "DIAGNOSTIC", "CHARGES", "TAXE"],
    "Transport": ["TRAIN", "METRO", "BUS", "TRAM", "TAXI", "AVION", "BATEAU", "VELO", "CAMION", "FERRY", "CAR", "NAVETTE", "DIRIGEABLE", "FIACRE", "CALECHE", "VOITURE", "SCOOTER", "MOTO", "PENICHE"],
    "Automobile": ["MOTEUR", "VOLANT", "PNEU", "FREIN", "PHARE", "CAPOT", "COFFRE", "PORTIERE", "PARECHOC", "EMBRAYAGE", "ESSENCE", "DIESEL", "BATTERIE", "RETRO", "CLIGNOTANT", "CHASSIS", "PEDALE", "KLAXON", "JANTE", "SIEGE"],
    "Motocyclettes": ["MOTO", "SCOOTER", "GUIDON", "CASQUE", "SELLE", "CYLINDREE", "CARENAGE", "PNEU", "FREIN", "CHOPPER", "ROADSTER", "SIDECAR", "BLOUSON", "GANTS", "PILOTE", "CIRCUIT", "BEQUILLE", "MOTARD", "TRAIL", "CROSS", "VITESSE"],
    "Aviation": ["AVION", "PILOTE", "AILE", "HELICE", "REACTEUR", "PISTE", "DECOLLAGE", "ATTERRIR", "HANGAR", "AEROPORT", "COCKPIT", "ALTITUDE", "VOL", "TURBINE", "FUSELAGE", "ESCALE", "HUBLOT", "PLANEUR", "CABINE", "RADAR"],
    "Navigation": ["BARRE", "VOILE", "MAT", "PROUE", "POUPE", "TRIBORD", "BABORD", "ANCRE", "CAP", "BOUSSOLE", "EQUIPAGE", "CAPITAINE", "PORT", "QUAI", "CARTE", "LOCH", "SEXTANT", "VOILIER", "AMARRE", "NAVIGUER", "BALISE"],
    "Ferroviaire": ["RAIL", "TRAIN", "GARE", "QUAI", "WAGON", "LOCOMOTIVE", "TGV", "AIGUILLAGE", "VOIE", "SIGNAL", "TUNNEL", "CONTROLEUR", "BILLET", "RAME", "TRACTION", "MACHINISTE", "BALLAST", "TRAVERSE", "CATENAIRE", "DEPART", "TERMINUS"],
    "Cyclisme": ["VELO", "PEDALE", "CHAINE", "SELLE", "GUIDON", "ROUE", "PNEU", "CASQUE", "MAILLOT", "PELOTON", "SPRINT", "ECHAPPEE", "COL", "ETAPE", "TOUR", "PEDALER", "FREIN", "DEVIATEUR", "MONTEE", "DESCENTE", "PISTE"],
    "Circulation": ["ROUTE", "FEU", "STOP", "CARREFOUR", "AUTOROUTE", "PEAGE", "RADAR", "PIETON", "TROTTOIR", "BOUCHON", "PERMIS", "CODE", "VITESSE", "CHAUSSEE", "TRAFIC", "RALENTIR", "DOUBLER", "STATIONNER", "VOIE", "SENS"],
    "Signalisation": ["PANNEAU", "STOP", "CEDER", "FEU", "BALISE", "FLECHE", "LIGNE", "SENS", "INTERDIT", "DANGER", "VITESSE", "PASSAGE", "PIETON", "RADAR", "LIMITE", "MARQUAGE", "DEVIATION", "TRIANGLE", "ZEBRA", "CONE"],
    "Mécanique": ["MOTEUR", "PISTON", "BIELLE", "CYLINDRE", "ENGRENAGE", "PIGNON", "COURROIE", "ROULEMENT", "ARBRE", "CAME", "SOUPAPE", "BOULON", "ECROU", "JOINT", "LEVIER", "RESSORT", "TURBO", "GRAISSE", "HUILE", "VIS"],
    "Électricité": ["COURANT", "TENSION", "VOLT", "AMPERE", "WATT", "FIL", "PRISE", "FUSIBLE", "CIRCUIT", "CABLE", "RESISTANCE", "PILE", "CHARGE", "COMPTEUR", "ECLAIRAGE", "AMPOULE", "MASSE", "OHM", "ENERGIE", "CONDUCTEUR"],
    "Électronique": ["PUCE", "TRANSISTOR", "DIODE", "CIRCUIT", "CAPACITE", "RESISTANCE", "CARTE", "SOUDURE", "SIGNAL", "ECRAN", "CAPTEUR", "PROCESSEUR", "LED", "RELAIS", "BORNE", "PLATINE", "MICROPUCE", "ANTENNE", "BOBINE", "QUARTZ"],
    "Informatique": ["CLAVIER", "SOURIS", "ECRAN", "LOGICIEL", "FICHIER", "DOSSIER", "PROGRAMME", "MEMOIRE", "DISQUE", "PROCESSEUR", "PIXEL", "BUG", "CODE", "PORTABLE", "SERVEUR", "TABLETTE", "IMPRIMANTE", "REPERTOIRE", "SAUVEGARDE", "ALGORITHME", "CLOUD"],
    "Internet": ["SITE", "PAGE", "LIEN", "WEB", "MAIL", "RESEAU", "NAVIGATEUR", "MOTEUR", "BLOG", "FORUM", "ONLINE", "CLIC", "COOKIE", "WIFI", "SERVEUR", "ADRESSE", "COURRIEL", "MESSAGERIE", "STREAMING", "PSEUDO", "PIRATE", "VIRUS"],
    "Téléphonie": ["ALLO", "APPEL", "SONNERIE", "FORFAIT", "RESEAU", "ANTENNE", "MOBILE", "PORTABLE", "SMS", "MESSAGE", "REPONDEUR", "CABINE", "OPERATEUR", "COMBINE", "CADRAN", "NUMERO", "CONTACT", "RAPPEL", "FIXE", "ECOUTEUR", "ECRAN", "VIBREUR"],
    "Robotique": ["ROBOT", "CAPTEUR", "MOTEUR", "BRAS", "PINCE", "ANDROIDE", "CIRCUIT", "PROGRAMME", "AUTOMATE", "CYBORG", "SERVO", "ALGORITHME", "ROUE", "ENGRENAGE", "COMMANDE", "DRONE", "ARTIFICIEL", "ACTIONNEUR", "MACHINE", "VISION"],
    "Astronomie": ["TELESCOPE", "LUNETTE", "ORBITE", "COMETE", "ECLIPSE", "METEORITE", "ASTEROIDE", "COSMOS", "UNIVERS", "NEBULEUSE", "ZENITH", "PULSAR", "QUASAR", "ASTRONOME", "LUNE", "SOLEIL", "AXE", "AURORE", "ETOILE", "PLANETE"],
    "Planètes": ["MERCURE", "VENUS", "TERRE", "MARS", "JUPITER", "SATURNE", "URANUS", "NEPTUNE", "PLUTON", "LUNE", "CERES", "TITAN", "ANNEAU", "ORBITE", "ATMOSPHERE", "SATELLITE", "GEANTE", "TELLURIQUE", "CRATERE"],
    "Étoiles": ["SOLEIL", "SIRIUS", "POLAIRE", "VEGA", "RIGEL", "ANTARES", "BETELGEUSE", "NOVA", "SUPERNOVA", "NAINE", "GEANTE", "PULSAR", "QUASAR", "ASTRE", "FILANTE", "ORION", "CASSIOPEE", "ETINCELLE", "ECLAT", "LUEUR"],
    "Galaxies": ["SPIRALE", "ELLIPTIQUE", "ANDROMEDE", "NEBULEUSE", "COSMOS", "UNIVERS", "AMAS", "TROU", "NOIR", "MATIERE", "ENERGIE", "ETOILE", "HUBBLE", "QUASAR", "HALO", "NOYAU", "BRAS", "DISQUE", "LUMIERE", "PARSEC", "VIDE"],
    "Sciences": ["EXPERIENCE", "THEORIE", "HYPOTHESE", "CHERCHEUR", "MICROSCOPE", "DECOUVERTE", "OBSERVER", "ANALYSE", "FORMULE", "SAVANT", "ETUDE", "METHODE", "PREUVE", "RESULTAT", "MESURE", "ENERGIE", "MATIERE", "INVENTION", "CELLULE", "ATOME"],
    "Chimie": ["ATOME", "MOLECULE", "ACIDE", "BASE", "SEL", "OXYGENE", "HYDROGENE", "CARBONE", "AZOTE", "REACTION", "ELEMENT", "PROTON", "NEUTRON", "ELECTRON", "SOLUTION", "MELANGE", "ALCOOL", "CATALYSEUR", "TABLEAU", "LIAISON", "ENZYME"],
    "Physique": ["FORCE", "ENERGIE", "MASSE", "VITESSE", "GRAVITE", "OPTIQUE", "LUMIERE", "ONDE", "PHOTON", "QUANTUM", "NEWTON", "JOULE", "WATT", "PRESSION", "FRICTION", "CHALEUR", "MAGNETISME", "MOUVEMENT", "RELATIVITE", "FUSION", "AIMANT"],
    "Biologie": ["CELLULE", "ADN", "GENE", "ENZYME", "ORGANE", "TISSU", "ESPECE", "EVOLUTION", "BACTERIE", "VIRUS", "NOYAU", "PROTEINE", "CHROMOSOME", "MUTATION", "ECOSYSTEME", "HEREDITE", "CROISSANCE", "MEMBRANE", "ORGANISME", "NEURONE", "SANG"],
    "Géologie": ["FAILLE", "STRATE", "FOSSILE", "MINERAL", "ROCHE", "SEISME", "MAGMA", "CRISTAL", "SEDIMENT", "ERUPTION", "TECTONIQUE", "GRANITE", "ARGILE", "CALCAIRE", "CRATON", "GISEMENT", "MANTEAU", "NOYAU", "CROUTE", "SILICATE", "GEODE", "DOLINE"],
    "Mathématiques": ["ADDITION", "MULTIPLIER", "DIVISION", "FRACTION", "EQUATION", "ALGEBRE", "NOMBRE", "CHIFFRE", "PRODUIT", "SOMME", "RACINE", "PUISSANCE", "THEOREME", "LOGIQUE", "PREUVE", "FONCTION", "MOYENNE", "ENTIER", "PREMIER", "DECIMAL", "VARIABLE"],
    "Géométrie": ["ANGLE", "DROITE", "POINT", "SEGMENT", "CERCLE", "TRIANGLE", "CARRE", "RAYON", "DIAMETRE", "PARALLELE", "AIRE", "VOLUME", "SURFACE", "SYMETRIE", "DIAGONALE", "POLYGONE", "COMPAS", "EQUERRE", "RAPPORTEUR", "TANGENTE", "CORDE", "ARC", "CUBE", "PRISME"],
    "Calcul": ["ADDITION", "SOMME", "PRODUIT", "QUOTIENT", "RESTE", "REPORT", "CHIFFRE", "NOMBRE", "DIVISER", "MULTIPLIER", "CALCULER", "RESULTAT", "TOTAL", "MENTAL", "POSER", "OPERATION", "TABLE", "ERREUR", "VIRGULE", "DIXIEME", "UNITE", "DIZAINE", "CENTAINE", "RETENUE"],
    "Mesures": ["METRE", "LITRE", "GRAMME", "KILO", "MILLIMETRE", "CENTIMETRE", "KILOMETRE", "TONNE", "POIDS", "LONGUEUR", "LARGEUR", "HAUTEUR", "VOLUME", "SURFACE", "BALANCE", "JAUGE", "REGLE", "CAPACITE", "MASSE", "DEGRE", "ECHELLE", "MESURER"],
    "Temps": ["HEURE", "MINUTE", "SECONDE", "JOUR", "SEMAINE", "MOIS", "ANNEE", "SIECLE", "EPOQUE", "DECENNIE", "PASSE", "FUTUR", "PRESENT", "AUJOURDHUI", "HIER", "DEMAIN", "MATIN", "SOIR", "NUIT", "MIDI", "MINUIT", "ETERNITE", "DUREE", "INSTANT"],
    "Calendrier": ["JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE", "LUNDI", "MARDI", "MERCREDI", "JEUDI", "VENDREDI", "SAMEDI", "DIMANCHE", "FERIE"],
    "Horlogerie": ["MONTRE", "HORLOGE", "PENDULE", "BALANCIER", "RESSORT", "AIGUILLE", "CADRAN", "BOITIER", "COUCOU", "REVEIL", "SABLIER", "COURONNE", "BRACELET", "MECANISME", "ENGRENAGE", "QUARTZ", "CARILLON", "LUNETTE", "HORLOGER", "REMONTER", "RUBIS"],
    "Musique": ["NOTE", "MELODIE", "RYTHME", "HARMONIE", "CHANT", "CHANSON", "ACCORD", "GAMME", "CONCERT", "OPERA", "ORCHESTRE", "CHORALE", "SOLO", "DUO", "REFRAIN", "PARTITION", "TEMPO", "CLEF", "DIESE", "BEMOL", "SYMPHONIE", "JAZZ", "ROCK"],
    "Instruments": ["PIANO", "GUITARE", "VIOLON", "FLUTE", "HARPE", "TROMPETTE", "TROMBONE", "SAXOPHONE", "CLARINETTE", "HAUTBOIS", "BASSON", "TAMBOUR", "CYMBALES", "BATTERIE", "ACCORDEON", "ORGUE", "BANJO", "UKULELE", "XYLOPHONE", "TRIANGLE", "TUBA", "CORNEMUSE", "HARMONICA"],
    "Danse": ["BALLET", "VALSE", "TANGO", "SALSA", "FLAMENCO", "CLASSIQUE", "MODERNE", "JAZZ", "RUMBA", "SAMBA", "POLKA", "CANCAN", "BOLERO", "PIROUETTE", "DANSEUR", "DANSEUSE", "TUTU", "BARRE", "SCENE", "SWING", "TWIST", "MAZURKA", "GAVOTTE"],
    "Théâtre": ["SCENE", "RIDEAU", "ACTEUR", "ACTRICE", "COMEDIE", "TRAGEDIE", "DRAME", "ROLE", "REPLIQUE", "COULISSE", "DECOR", "PARTERRE", "BALCON", "LOGE", "ENTRACTE", "PIECE", "MONOLOGUE", "COSTUME", "PUBLIC", "SOUFFLEUR", "AFFICHE", "COMEDIEN", "TROUPE", "ACTE"],
    "Cinéma": ["FILM", "ECRAN", "SALLE", "ACTEUR", "SCENARIO", "CAMERA", "TOURNAGE", "PELLICULE", "PROJECTION", "AFFICHE", "TRAILER", "POPCORN", "SEANCE", "SEQUENCE", "CLAP", "DECOR", "COMEDIE", "WESTERN", "THRILLER", "HORREUR", "MONTAGE", "FESTIVAL", "OSCAR"],
    "Photographie": ["APPAREIL", "OBJECTIF", "FLASH", "CLICHE", "PHOTO", "PORTRAIT", "PAYSAGE", "ZOOM", "DIAPHRAGME", "OBTURATEUR", "PELLICULE", "NUMERIQUE", "CADRAGE", "FOCALE", "TIRAGE", "NEGATIF", "ALBUM", "RETOUCHE", "TRIPODE", "EXPOSITION", "LUMIERE"],
    "Sculpture": ["STATUE", "BUSTE", "MARBRE", "BRONZE", "ARGILE", "PLATRE", "CISEAU", "BURIN", "MAILLET", "MODELER", "SCULPTEUR", "RELIEF", "SOCLE", "FONTE", "MOULAGE", "TAILLE", "ATELIER", "RODIN", "STATUETTE", "FIGURINE", "MONUMENT", "GRANIT"],
    "Littérature": ["ROMAN", "NOUVELLE", "POEME", "ESSAI", "AUTEUR", "PAGE", "CHAPITRE", "LIVRE", "FABLE", "CONTE", "RECIT", "EDITEUR", "PRIX", "CRITIQUE", "BIOGRAPHIE", "THEATRE", "STYLE", "PROSE", "INTRIGUE", "PERSONNAGE", "LECTEUR", "HUGO", "ZOLA", "MOLIERE", "BALZAC"],
    "Poésie": ["POEME", "VERS", "STROPHE", "RIME", "SONNET", "ODE", "BALLADE", "REFRAIN", "METRE", "POETE", "IMAGE", "LYRIQUE", "ELEGIE", "HAIKU", "RECUEIL", "SYLLABE", "HEMISTICHE", "CESURE", "QUATRAIN", "TERCET", "MUSE", "RIMER"],
    "Grammaire": ["NOM", "VERBE", "ADJECTIF", "ADVERBE", "SUJET", "COMPLEMENT", "PRONOM", "ARTICLE", "PHRASE", "ACCORD", "TEMPS", "MODE", "CONJUGUER", "PLURIEL", "SINGULIER", "GENRE", "LOCUTION", "SYNTAXE", "PASSIF", "ACTIF", "FEMININ", "MASCULIN", "VIRGULE", "POINT", "ANALYSE"],
    "Langues": ["FRANCAIS", "ANGLAIS", "ESPAGNOL", "ALLEMAND", "ITALIEN", "RUSSE", "CHINOIS", "ARABE", "JAPONAIS", "LATIN", "GREC", "PORTUGAIS", "POLONAIS", "TURC", "HINDI", "COREEN", "DIALECTE", "ACCENT", "TRADUIRE", "LANGAGE", "IDIOME"],
    "Écriture": ["STYLO", "PLUME", "CRAYON", "ENCRE", "PAPIER", "CAHIER", "LETTRE", "MOT", "PHRASE", "PAGE", "RATURE", "ALPHABET", "MANUSCRIT", "DICTEE", "REDIGER", "ECRIRE", "NOTES", "BROUILLON", "GOMME", "SIGNATURE", "PARAGRAPHE", "CARNET", "TEXTE"],
    "Lecture": ["LIRE", "LIVRE", "PAGE", "ROMAN", "LIBRAIRIE", "LECTEUR", "CHAPITRE", "SIGNET", "COUVERTURE", "TITRE", "RESUME", "EDITION", "FEUILLETER", "LUNETTES", "FAUTEUIL", "HISTOIRE", "MANGA", "POCHE", "INTRIGUE", "AVENTURE", "ALBUM"],
    "Mythologie": ["ZEUS", "HERA", "ATHENA", "APOLLON", "ARTEMIS", "HERMES", "POSEIDON", "HADES", "ARES", "APHRODITE", "DIONYSOS", "TITAN", "CYCLOPE", "MINOTAURE", "HYDRE", "SIRENE", "CENTAURE", "PEGASE", "MEDUSE", "OLYMPE", "HERCULE", "ODYSSEE", "ORACLE", "DRAGON", "ODIN", "THOR"],
    "Archéologie": ["FOUILLE", "VESTIGE", "RUINES", "FOSSILE", "TOMBEAU", "MOMIE", "POTERIE", "STRATE", "SITE", "ARTEFACT", "DATATION", "AMPHORE", "MOSAIQUE", "SARCOPHAGE", "CHANTIER", "MUSEE", "RELIQUE", "OSSEMENTS", "TERTRE", "NECROPOLE", "STELE", "CAVERNE"],
    "Histoire antique": ["ROME", "ATHENES", "EGYPTE", "SPARTE", "CESAR", "PHARAON", "LEGION", "FORUM", "CITE", "SENAT", "ESCLAVE", "TEMPLE", "AQUEDUC", "COLISEE", "AGORA", "GLADIATEUR", "EMPEREUR", "BABYLONE", "CARTHAGE", "PERSE", "TROIE", "HANNIBAL", "ALEXANDRE", "ACROPOLE", "GAULOIS"],
    "Métiers": ["BOULANGER", "BOUCHER", "MACON", "PLOMBIER", "MENUISIER", "COIFFEUR", "FLEURISTE", "TAILLEUR", "FORGERON", "TISSERAND", "POTIER", "VITRIER", "CORDONNIER", "PEINTRE", "MARECHAL", "JARDINIER", "PECHEUR", "BERGER", "FERMIER", "SELLIER"],
    "Professions": ["MEDECIN", "AVOCAT", "JUGE", "NOTAIRE", "PILOTE", "INFIRMIER", "DENTISTE", "ARCHITECTE", "INGENIEUR", "PROFESSEUR", "POLICIER", "POMPIER", "CHIRURGIEN", "PHARMACIEN", "COMPTABLE", "CHERCHEUR", "ENSEIGNANT", "SECRETAIRE", "MAGISTRAT"],
    "Commerce": ["MAGASIN", "BOUTIQUE", "ACHAT", "VENTE", "CLIENT", "PRIX", "CAISSE", "REMISE", "SOLDES", "MARCHE", "VITRINE", "ETALAGE", "COMMERCANT", "PANIER", "FACTURE", "TICKET", "RAYON", "STOCK", "LIVRAISON", "GROSSISTE", "VENDEUR", "COMMANDE", "ENSEIGNE"],
    "Entreprise": ["SOCIETE", "PATRON", "EMPLOYE", "SALARIE", "BUREAU", "REUNION", "EQUIPE", "DIRECTEUR", "CONTRAT", "USINE", "ATELIER", "STAGIAIRE", "PROJET", "CLIENT", "SERVICE", "BUDGET", "OBJECTIF", "GERANT", "FILIALE", "CADRE", "SIEGE"],
    "Finance": ["BOURSE", "ACTION", "OBLIGATION", "CAPITAL", "DIVIDENDE", "PROFIT", "INTERET", "CREDIT", "EPARGNE", "PLACEMENT", "FONDS", "RENDEMENT", "INVESTIR", "TAUX", "COURS", "ACTIF", "PASSIF", "BILAN", "DETTE", "RISQUE", "GAIN", "TRADER"],
    "Banque": ["COMPTE", "CHEQUE", "CARTE", "VIREMENT", "RETRAIT", "DEPOT", "PRET", "CREDIT", "EPARGNE", "GUICHET", "CONSEILLER", "CODE", "SOLDE", "AGENCE", "TAUX", "LIVRET", "COFFRE", "DECOUVERT", "IBAN", "RELEVE", "VERSEMENT", "TRESOR", "MONNAIE"],
    "Économie": ["MARCHE", "OFFRE", "DEMANDE", "PRIX", "INFLATION", "CROISSANCE", "CHOMAGE", "SALAIRE", "IMPOT", "TAXE", "PIB", "DETTE", "DEFICIT", "BUDGET", "RICHESSE", "PRODUCTION", "EXPORT", "IMPORT", "TARIF", "CRISE", "COMMERCE", "MONNAIE"],
}

GRID_SIZE = 10
NUM_PUZZLES = 224
DIRECTIONS = {
    "H":  (0, 1),    # Horizontal
    "V":  (1, 0),    # Vertical
    "DD": (1, 1),    # Diagonale descendante
    "DG": (1, -1),   # Diagonale montante
}


def normalize(word):
    """Majuscules, sans accents, sans espaces ni tirets."""
    word = unicodedata.normalize("NFD", word.upper())
    word = "".join(c for c in word if unicodedata.category(c) != "Mn")
    return "".join(c for c in word if c in string.ascii_uppercase)


def split_theme(theme_words):
    # Nettoyer et supprimer les doublons
    words = list(dict.fromkeys(normalize(w) for w in theme_words))

    # Les mots de plus de 10 lettres ne peuvent pas être placés
    words = [w for w in words if 1 <= len(w) <= GRID_SIZE]

    random.shuffle(words)

    # Répartition en deux groupes distincts
    middle = (len(words) + 1) // 2
    return words[:middle], words[middle:]


def create_grid():
    return [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def place_word(grid, word, max_attempts=500):
    word = normalize(word)

    if not word or len(word) > GRID_SIZE:
        return None

    directions = list(DIRECTIONS.values())

    for _ in range(max_attempts):
        dr, dc = random.choice(directions)
        row = random.randrange(GRID_SIZE)
        col = random.randrange(GRID_SIZE)

        end_row = row + (len(word) - 1) * dr
        end_col = col + (len(word) - 1) * dc

        if not (0 <= end_row < GRID_SIZE and 0 <= end_col < GRID_SIZE):
            continue

        if all(
            grid[row + i * dr][col + i * dc] in ("", letter)
            for i, letter in enumerate(word)
        ):
            for i, letter in enumerate(word):
                grid[row + i * dr][col + i * dc] = letter

            return {
                "word": word,
                "start": (row, col),
                "direction": (dr, dc),
                "length": len(word),
            }

    return None


def fill_grid(grid, theme):
    # Les mots les plus longs d'abord : bien plus facile à placer
    words = sorted(theme, key=len, reverse=True)

    placed_words = []
    for word in words:
        placement = place_word(grid, word)
        if placement is not None:
            placed_words.append(placement)

    # Remplir les cases restantes avec des lettres aléatoires
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == "":
                grid[row][col] = random.choice(string.ascii_uppercase)

    return grid, placed_words


def build_grid(words, max_tries=100):
    """Regénère la grille jusqu'à ce que TOUS les mots soient placés."""
    best = None
    for _ in range(max_tries):
        grid, placed = fill_grid(create_grid(), words)
        if best is None or len(placed) > len(best[1]):
            best = (grid, placed)
        if len(placed) == len(words):
            break
    return best


def generate_all_puzzles():
    puzzles = []
    number = 1
    for theme, theme_words in THEMES.items():
        words1, words2 = split_theme(theme_words)
        for words in (words1, words2):
            grid, placed = build_grid(words)
            puzzles.append({
                "number": number,
                "theme": theme,
                "grid": grid,
                "words": placed,
                "missing": sorted(set(words) - {p["word"] for p in placed}),
            })
            number += 1
    return puzzles


if __name__ == "__main__":
    print(f"{len(THEMES)} thèmes -> {len(THEMES) * 2} grilles "
          f"(objectif : {NUM_PUZZLES})")

    # Mots ignorés car trop longs (> 10 lettres)
    for theme, words in THEMES.items():
        too_long = [w for w in words if len(normalize(w)) > GRID_SIZE]
        if too_long:
            print(f"  [{theme}] mots trop longs ignorés : {too_long}")

    puzzles = generate_all_puzzles()

    incomplete = [p for p in puzzles if p["missing"]]
    print(f"{len(puzzles)} grilles générées, "
          f"{len(incomplete)} avec des mots non placés")
    for p in incomplete:
        print(f"  Grille {p['number']} ({p['theme']}) : {p['missing']}")

    # Aperçu de la première grille
    first = puzzles[0]
    print(f"\nGrille {first['number']} - {first['theme']}")
    for row in first["grid"]:
        print(" ".join(row))
    print("Mots :", [p["word"] for p in first["words"]])

    # Export pour la mise en page du livre
    with open("grilles.json", "w", encoding="utf-8") as f:
        json.dump(puzzles, f, ensure_ascii=False, indent=2)
    print("\nExport : grilles.json")
